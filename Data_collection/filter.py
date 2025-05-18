import os
import pickle
import shutil
from graph_comparator import GraphComparator

def filter_factory_pattern_graphs(input_dir, output_dir, representative_graph_path):
    """
    Filters graph files that match the Factory Pattern based on essential conditions.

    Args:
        input_dir (str): Directory containing input graph files.
        output_dir (str): Directory to save matching graph files.
        representative_graph_path (str): Path to the representative graph file.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the GraphComparator
    comparator = GraphComparator(representative_graph_path)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".gpickle"):
            file_path = os.path.join(input_dir, filename)
            print(f"\nProcessing file: {file_path}")

            try:
                # Compare the graph file with the representative graph
                is_match, confidence = comparator.compare(file_path)

                # Save the file if it matches all essential conditions
                if is_match:
                    print(f"  -> Match found! Saving {filename} (Confidence: {confidence:.2f})")
                    shutil.copy(file_path, os.path.join(output_dir, filename))
                else:
                    print(f"  -> No match. Skipping {filename} (Confidence: {confidence:.2f})")
            except Exception as e:
                print(f"  -> Error processing {filename}: {e}")

if __name__ == "__main__":
    # Define paths
    input_directory = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\graphs"
    output_directory = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\factory_graphs"
    representative_graph = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\test_graph\factory_pattern_representative.gpickle"

    # Run the filtering process
    filter_factory_pattern_graphs(input_directory, output_directory, representative_graph)
