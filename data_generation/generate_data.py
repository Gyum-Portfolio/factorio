import anthropic
import json

def call_api(api_key, design_pattern):
    """Performs api call that prompts the model to generate 20 examples of classes before and after being refactored to a specific design pattern. 
    Returns the api response in textual form.


    Args:
        api_key (str): the key to use in order to call the api.
        design_pattern (str): the design pattern to generate the model for.
    """    
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="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",
    )


    prompt = f"""
   Provide exactly 20 Java examples that demonstrate refactoring a class to use the {design_pattern} Design Pattern. 
   
   For each example:
   
   - Start by creating a class that does not use any design patterns. 
   - Then refactor this class to use the {design_pattern} pattern.
   - Do not print any explanation. Print the code only in JSON format with two keys: "class_before_refactoring" and "class_after_refactoring"

    Return the answer as a JSON list, where each example is a different element of the list. Print each element on a separate line.

    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        system = f"You are a seasoned Java developer who is an expert in the {design_pattern} design pattern.",
        messages=[
            {
                "role": "user", 
                "content": f"{prompt}"
            }
        ]
    )

    return message.content[0].text


if __name__ == '__main__':
    api_key = "your-api-key-here"
    design_pattern = "Factory"
    responses = []
    
    response = call_api(api_key, design_pattern)

    file_name = "generated_data.json"

    # Write the model's response to the file.
    with open(file_name, "w") as file:
        file.write(response)