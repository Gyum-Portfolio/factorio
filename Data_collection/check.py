import pickle
import networkx as nx
from pathlib import Path

def load_and_check_graph(file_path):
    """
    Loads a graph from a .gpickle file and prints its details.
    """
    file_path = Path(file_path)

    # Check if the file exists
    if not file_path.exists():
        print(f"Error: File not found at {file_path}")
        return

    # Load the graph
    try:
        with open(file_path, 'rb') as f:
            graph = pickle.load(f)
    except Exception as e:
        print(f"Error loading graph: {e}")
        return

    # Print graph details
    print(f"Graph loaded from: {file_path}")
    print("\nNodes:")
    for node, attrs in graph.nodes(data=True):
        print(f"  {node}: {attrs}")

    print("\nEdges:")
    for source, target, attrs in graph.edges(data=True):
        print(f"  {source} -> {target}: {attrs}")


if __name__ == "__main__":
    # Specify the path to the .gpickle file
    graph_file_path = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\test_graph\044da794f471b62e65a1dc903a3f1dc71547f070.gpickle" #'test_graph/044da794f471b62e65a1dc903a3f1dc71547f070.gpickle'
    load_and_check_graph(graph_file_path)