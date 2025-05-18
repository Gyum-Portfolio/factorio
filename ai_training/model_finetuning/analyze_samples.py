import json
import sys



def format_diff(input_file, output_file):
   with open(input_file, 'r') as f, open(output_file, 'w') as out:
       data = json.load(f)
       for diff in data:
           out.write(f"\nDiff #{diff.get('index')}\n")
           out.write("\nBEFORE:\n")
           out.write(diff.get("before"))
           out.write("\nAFTER:\n")
           out.write(diff.get("after"))
           out.write("\n" + "-"*80 + "\n")

format_diff('filtered_java_code.json', 'diffs.txt')