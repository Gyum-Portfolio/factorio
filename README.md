# Team 12

## VS Code Extension

To seamlessly integrate the agent into a developer's workflow, we created a VS Code extension that analyzes files during commit. The extension is located in [`refactorio`](./refactorio), and setup and running instructions can be found in [`refactorio/README.md`](./refactorio/README.md).

## Model

The VS Code extension is based on Anthropic's Claude 3.5 Sonnet and OpenAI's GPT-4.0, trained with few-shot prompting. The implementation details may be found under [`builder-pattern-service`](./builder-pattern-service). 

[`ai_training`](./ai_training) is an artifact representing our initial testing of the ai-suite.

## Dataset

### Datamining Approach

Everything related to the data mining approach that we followed can be found under [`Data_collection`](./Data_collection).

### Synthetic Dataset Generation

Everything related to the dataset generation can be found under [`data_generation`](data_generation).


## Evaluation

To evaluate our model, we evaluated:

1. its design pattern opportunity detection capabilities. This can be found under [the `test_pattern_detection` folder inside of `validation_data`](./validation_data/test_pattern_detection). 

2. its refactoring suggestion capabilities. This can be found under [the `test_refactoring_suggestions` folder inside of `validation_data`](./validation_data/test_refactoring_suggestions).

## API Limits

Please be mindful of the API usage limits. Avoid spamming the API with a large number of commits or sending very large context data during debugging, as this can quickly consume available tokens. Excessive use may impact performance or lead to timeouts, and will interrupt the debugging process.
