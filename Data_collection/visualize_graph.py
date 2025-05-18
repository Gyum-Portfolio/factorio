import pickle
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


def visualize_graph(file_path):
    """
    Visualizes a graph stored in a .gpickle file.
    """
    # Ensure the file exists
    if not Path(file_path).exists():
        print(f"Error: File not found at {file_path}")
        return

    # Load the graph
    with open(file_path, 'rb') as f:
        graph = pickle.load(f)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)  # Layout for graph positioning
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        edge_color="gray",
    )
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=nx.get_edge_attributes(graph, 'relation'),
    )
    plt.title(f"Graph Visualization: {Path(file_path).name}")
    plt.show()


if __name__ == "__main__":
    # Specify the full path to the .gpickle file
    graph_file_path = r'C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\test_graph\044da794f471b62e65a1dc903a3f1dc71547f070.gpickle'
    visualize_graph(graph_file_path)
