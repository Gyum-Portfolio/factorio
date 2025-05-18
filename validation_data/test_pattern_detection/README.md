# What

This directory runs Refactorio on the dataset that we mined by using the factory pattern. In pricniple, Refactorio should detect no refactoring opportunities for none of the mined classes. We calculate the model's accuracy. 

# Files structure:

`samples.json` - the data mined factory pattern classes

`samples_results.json` - the responses obtained from calling Refactorio on these classes

`validate_no_refactorings.py` - calls the API on each of the classes from `samples.json`, returns the result in `samples_results.json`

`stats.csv` - the results from `samples_result.json`, in csv format

`final_stats.csv` - contains the accuracy of the model

`samples_results_statistics.py` - takes the results from `samples_results.json` and calculates the LLM accuracy
