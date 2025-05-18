import os
from urllib import request

import boto3
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
import logging
from langchain.prompts import FewShotPromptTemplate
from training_data import examples
import random



logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG)

class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

def get_api_keys():
    if os.getenv('AWS_LAMBDA_FUNCTION_NAME'):  # In Lambda
        try:
            session = boto3.session.Session()
            client = boto3.client('secretsmanager')
            secret_value = client.get_secret_value(SecretId='builder-pattern-service-secrets')
            secret_dict = json.loads(secret_value['SecretString'])
            return {
                'openai': secret_dict['OPENAI_API_KEY'],
                'anthropic': secret_dict['ANTHROPIC_API_KEY']
            }
        except Exception as e:
            logger.error(f"Error getting secrets: {str(e)}")
            raise e
    else:  # Local
        from dotenv import load_dotenv
        load_dotenv()
        return {
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY')
        }

app = FastAPI(title="Builder Pattern Analyzer")


class CodeAnalysisRequest(BaseModel):
    code: str
    designPattern: str
    model_provider: ModelProvider = ModelProvider.OPENAI

class DesignPatternExample(BaseModel):
    input_code: str
    design_pattern: str
    implementation: str

example_prompt = PromptTemplate(
    input_variables=["original_code", "pattern", "implemented_code"],
    template="""
Original Code:
{original_code}

Analysis for {pattern} Pattern:
Determine if the {pattern} would be beneficial. If applicable, think about a high-level outline of how it could be implemented. Then, give the full code that implements the {pattern}. If {pattern} should not be implemented, respond with: '{pattern} should NOT be implemented'

Implemented Code:
{implemented_code}
---"""
)




def get_model(model_provider: ModelProvider, api_keys: dict):
    if model_provider == ModelProvider.OPENAI:
        return ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            openai_api_key=api_keys['openai']
        )
    else:  # ANTHROPIC
        return ChatAnthropic(
            model_name="claude-3-sonnet-20240229",
            temperature=0.7,
            anthropic_api_key=api_keys['anthropic']
        )

@app.get("/")
async def root():
    return {"message": "Builder Pattern Analysis API"}

@app.post("/analyze")
async def analyze_code(request: CodeAnalysisRequest):
    try:
        api_keys = get_api_keys()
        model = get_model(request.model_provider, api_keys)
        filtered_examples = [ex for ex in examples if ex["pattern"]==request.designPattern]

        if filtered_examples:
            prompt_template = FewShotPromptTemplate(
                examples=filtered_examples,
                example_prompt=example_prompt,
                prefix="Here are examples of implementing design patterns:\n",
                suffix="""
        Now analyze this code:
        {code}

        Determine if the {pattern} would be beneficial. If applicable, think about a high-level outline of how it could be implemented. Then, give the full code that implements the {pattern}. If {pattern} should not be implemented, respond with: '{pattern} should NOT be implemented'
        """,
                input_variables=["code", "pattern"]
            )
        else:
            # no examples are available
            prompt_template = PromptTemplate(
                template="""Analyze this code:
        {code}

        Determine if the {pattern} would be beneficial. If applicable, think about a high-level outline of how it could be implemented. Then, give the full code that implements the {pattern}. If {pattern} should not be implemented, DO NOT RESPOND WITH CODE AND DO NOT GIVE OTHER RECOMMENDATIONS ABOUT ANYTHING ELSE, JUST respond with: '{pattern} should NOT be implemented'
        """,
                input_variables=["code", "pattern"]
            )

        print("About to format prompt...")
        formatted_prompt = prompt_template.format(
            code=request.code,
            pattern=request.designPattern
        )

        logger.info(f"Sending request to {request.model_provider} model")
        response = model.predict(formatted_prompt)
        logger.info(f"Received response from {request.model_provider}")

        # split response into explanation and code parts
        parts = response.split("```")
        explanation = parts[0].strip()
        code = parts[1].strip() if len(parts) > 1 else ""

        return {
            "statusCode": 200,
            "body": {
                "explanation": explanation,
                "code": code
            }
        }

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# handler for AWS Lambda
lambda_handler = Mangum(app)