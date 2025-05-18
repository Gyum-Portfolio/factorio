import aisuite as ai
import yaml
from dotenv import load_dotenv
import os
from pathlib import Path

class CodeAnalyzer:
    def __init__(self):
        load_dotenv()
        root_dir = Path(__file__).parent.parent.parent
        config_path = root_dir / 'config' / 'config.yaml'

        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)


        self.client = ai.Client()
        self.current_model = "huggingface:HuggingFaceH4/starchat-alpha"

    def analyze_code(self, code):

        messages = [
            {"role": "user", "content": f"""
                Analyze this code for factory pattern opportunities:
                {code}
                Should this code use the factory pattern? If yes, explain why and how.
            """}
        ]
        try:
            print(self.current_model)
            response = self.client.chat.completions.create(
                model=self.current_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000  # will increase later
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return None

    def switch_model(self, model_name):
        self.current_model = model_name

    def analyze_with_all_models(self, code):
        results = {}
        for model_name, model_id in self.config['models']['available'].items():
            self.switch_model(model_id)
            result = self.analyze_code(code)
            if result:
                results[model_name] = result
        return results

if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    test_code = """
    class Car:
        def __init__(self, type):
            if type == "sport":
                self.speed = "fast"
            elif type == "family":
                self.speed = "medium"
    """
    result = analyzer.analyze_code(test_code)
    if result:
        print(result)