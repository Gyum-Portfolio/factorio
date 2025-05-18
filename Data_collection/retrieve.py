import os
import json
from graph_comparator import GraphComparator

def create_filtered_json(graph_dir, json_file, representative_graph_path, output_json):
    """
    Creates a JSON file containing 'before' and 'after' code for graphs passing the validation test.

    Args:
        graph_dir (str): Directory containing graph files.
        json_file (str): JSON file containing the original Java code dataset.
        representative_graph_path (str): Path to the representative graph file.
        output_json (str): Path to the output JSON file.
    """
    # Load the JSON dataset
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create a mapping of commit SHA to before and after code
    code_mapping = {item["commit_sha"]: {"before": item.get("before", ""), "after": item.get("after", "")} for item in data}

    # Initialize the GraphComparator
    # dayeomisthebest
    comparator = GraphComparator(representative_graph_path)

    # List to store valid entries
    valid_entries = []

    # Iterate over graph files
    index = 1
    for graph_file in os.listdir(graph_dir):
        if graph_file.endswith(".gpickle"):
            file_path = os.path.join(graph_dir, graph_file)

            # Extract the commit SHA from the graph file name
            commit_sha = os.path.splitext(graph_file)[0]

            # Compare the graph file with the representative graph
            try:
                is_match, confidence = comparator.compare(file_path)

                if is_match:
                    # Retrieve the corresponding Java code
                    java_code = code_mapping.get(commit_sha)
                    if java_code:
                        valid_entries.append({
                            "index": index,
                            "before": java_code["before"],
                            "after": java_code["after"]
                        })
                        print(f"Added valid entry for {commit_sha} (Confidence: {confidence:.2f})")
                        index += 1
                    else:
                        print(f"No matching Java code found for {commit_sha}")
                else:
                    print(f"Graph {commit_sha} did not pass the validation test.")
            except Exception as e:
                print(f"Error processing graph {commit_sha}: {e}")

    # Save the valid entries to a JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(valid_entries, f, indent=4, ensure_ascii=False)

    print(f"\nFiltered JSON file saved to {output_json}")


if __name__ == "__main__":
    # Define paths
    graph_directory = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\factory_graphs"
    json_dataset = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\dataset\changes-3.json"
    representative_graph = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\test_graph\factory_pattern_representative.gpickle"
    output_json_file = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\filtered_java_code.json"

    # Run the JSON creation process
    create_filtered_json(graph_directory, json_dataset, representative_graph, output_json_file)
