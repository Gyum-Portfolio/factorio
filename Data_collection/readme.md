## Data Miner

This tool mines GitHub repositories for Factory pattern implementations in Java code. It specifically looks for commits that introduce new Factory patterns where none existed before.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
## Install dependencies
2. pip install requests

## Add Github Token
Create a GitHub Personal Access Token with repo scope and replace the token in github_config.py:

3. Add your GitHub token:
token = "your_github_token_here"

How it Works

## The pipeline follows these steps:

1. Repository Collection: Collects Java repositories from GitHub based on stars and activity.
2. Commit Analysis: Analyzes commit messages for Factory pattern-related keywords.
3. Pattern Detection: Uses regex-based validation to identify Factory pattern implementations.
4. Data Storage: Saves before/after code snapshots when new Factory patterns are found.

## Usage
Run the main pipeline with:

python3 main_pipeline.py

The tool will:

1. Collect top Java repositories (configurable via max_repos in RepoCollector).
2. Track processed repositories to avoid duplicates.
3. Save found patterns to dataset/changes.json.
4. Handle GitHub API rate limits automatically.

## Output

Data is saved in JSON format with the following details:

1. Before and after code snapshots.
2. Repository metadata.
3. Commit details.


## Factory Pattern Validator

This repository contains the implementation for validating and preparing datasets that transition from "before" to "after" code following the Factory Pattern. The system includes scripts for parsing Java code, generating graph representations, and validating against a representative Factory Pattern graph.

---

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
    - [Step 1: Generate Graphs](#step-1-generate-graphs)
    - [Step 2: Create a Representative Graph](#step-2-create-a-representative-graph)
    - [Step 3: Validate Graphs](#step-3-validate-graphs)
    - [Step 4: Filter and Output Results](#step-4-filter-and-output-results)
4. [File Structure](#file-structure)
5. [Example Workflow](#example-workflow)

---

## Requirements
- **Python**: 3.8 or higher
- Required Libraries:
  - `networkx`
  - `pickle`
  - `os`
  - `json`
  - `ast` (built-in)

Install the required dependencies using:
```bash
pip install networkx


Installation
Clone the repository:  git clone https://github.com/your-repo/factory-pattern-validator.git
cd factory-pattern-validator
	•	
	•	Ensure the project directory includes the required scripts:
	•	data_to_graph.py
	•	representative_graph.py
	•	graph_comparator.py
	•	filter_results.py

Usage
Step 1: Generate Graphs
Convert Java code into graph representations.
	•	Place your Java code files in a directory (e.g., input_code).
Run the data_to_graph.py script:  python data_to_graph.py --input_dir input_code --output_dir graphs
	•	
	•	Input: Directory containing .java files.
	•	Output: .gpickle files stored in the graphs directory.
Step 2: Create a Representative Graph
Generate the canonical Factory Pattern graph.
Run the representative_graph.py script:  python representative_graph.py --output_file graphs/factory_pattern_representative.gpickle
	•	
	•	Output: A .gpickle file representing the Factory Pattern.
Step 3: Validate Graphs
Compare each generated graph against the representative graph.
Run the graph_comparator.py script:  python graph_comparator.py --rep_graph graphs/factory_pattern_representative.gpickle --input_dir graphs --output_file validated_results.json
	•	
	•	Input: Graphs from Step 1 and the representative graph from Step 2.
	•	Output: A JSON file containing validation results.
Step 4: Filter and Output Results
Filter validated graphs and generate the final dataset.
Run the filter_results.py script:  python filter_results.py --input_file validated_results.json --output_file final_dataset.json
	•	
	•	Input: Validation results from Step 3.
	•	Output: A JSON file with indexed "before" and "after" snippets of code.

File Structure
	•	input_code/: Directory containing raw Java code files.
	•	graphs/: Directory for storing graph representations and the representative graph.
	•	validated_results.json: Validation results showing which graphs match the Factory Pattern.
	•	final_dataset.json: Final dataset of validated "before" and "after" code pairs.

Example Workflow
	•	Prepare your Java files in the input_code directory.
Generate graph representations:  python data_to_graph.py --input_dir input_code --output_dir graphs

	•	Create the representative Factory Pattern graph:
  python representative_graph.py --output_file graphs/factory_pattern_representative.gpickle

	•	Validate the graphs:
  python graph_comparator.py --rep_graph graphs/factory_pattern_representative.gpickle --input_dir graphs --output_file validated_results.json
	•	Filter and save the final dataset:
  python filter_results.py --input_file validated_results.json --output_file final_dataset.json


Notes
	•	Ensure all Java files are properly formatted and syntactically correct before processing.
	•	Modify the representative_graph.py script if additional optional characteristics need to be included.
	•	Use the final dataset (final_dataset.json) for downstream model training or evaluation tasks.

