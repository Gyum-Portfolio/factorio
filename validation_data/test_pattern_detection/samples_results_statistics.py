import json
import csv
from validate_no_refactorings import call_model

def write_csv():
    """ Write the results from samples_results.json into a file. The file is named stats.csv.

    """
    time_outs = 0

    with open('samples_results.json', "r") as results_file, open('stats.csv', 'w') as results_stats_file:
        results = json.load(results_file)
        writer = csv.writer(results_stats_file)
        # Keep track of the index (in case further investigations are needed), of whether the code was refactored or not, the refactored code if available the API's response message.
        csv_header = ["index", "refactoring_opportunity_detected?", "code", "message"]

        writer.writerow(csv_header)

        for idx, fact_class in enumerate(results):
            opportunity_detected = None 
            code = None 
            message = None 

            if "body" in fact_class:
                code = fact_class["body"]["code"]
                opportunity_detected = True

                if fact_class["body"]["code"] == "":
                    opportunity_detected = False     
                    
                writer.writerow([idx, opportunity_detected, code, message])
            else: 
                message = fact_class["message"]
                writer.writerow([idx, opportunity_detected, code, message])


def calculate_stats_for_csv():
    """Calculate the accuracy detection for negative cases. The result is dumped into final_stats.csv.
    """
    total = 0
    correct = 0

    with open("stats.csv", 'r') as csv_file, ("final_stats.csv", 'w') as csv_file_stats:
        reader = csv.reader(csv_file)
        writer = csv.writer(csv_file_stats)

        for row in reader:
            total += 1

            if row[1] == 'False':
                correct += 1
        
        header = ["Total", "Correct", "Accuracy"]

        writer.writerow(header)
        writer.writerow([total, correct, correct/total])

        print(f"Total: {total}")
        print(f"Correct: {correct}")
        print(f"Accuracy: {correct/total}")



if __name__ == '__main__':
    # First, write the results from samples_results.json into a csv file.
    #write_csv()
    
    # Based on that csv file, calculate the accuracy
    calculate_stats_for_csv()
        
        

