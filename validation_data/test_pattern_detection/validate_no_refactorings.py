""" This file reads the data mined factory pattern classes and asks the API to refactor each of them. 
    Please avoid running this when checking our repository, so as to avoid spamming the API.

Returns:
    The results of the API calls are stored in the samples_results.json file.
"""

import requests
import json

def call_model(code):
    """Calls Refactorio's LLM, asking it to refactor the given snippet of code to a factory design pattern.

    Args:
        code (_type_): the code to refactor

    Returns:
        _type_: the model's response in JSON format.
    """    
    endpoint = 'https://puqb636le2.execute-api.us-east-1.amazonaws.com/Prod/analyze'

    header = {'Content-Type': "application/json"}

    print("Calling endpoint with factory pattern")

    data = {
        'code': code,
        'designPattern': "Factory",
        'model_provider': "anthropic"
    }

    response = requests.post(endpoint, json=data, headers=header)

    return response.json()



if __name__ == '__main__':

    # samples.json is the file containing the data mined factory pattern classes.
    with open('samples.json') as classes_with_factory_pattern:
        classes = json.load(classes_with_factory_pattern)

    results = []

    # iterate through each of the mined classes and call the api to ask for a refactoring.
    # we expect the model to not find a refactoring for these classes.
    for factory_class in classes:
        results.append(call_model(factory_class["after"]))

    print(results)

    # dump the results into the 'samples_results.json' file.               
    with open('samples_results.json', "w") as results_file:
        json.dump(results, results_file)


        

