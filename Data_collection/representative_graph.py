import networkx as nx
import pickle
from pathlib import Path


def create_representative_factory_graph(output_file):
    """
    Creates a representative graph for the Factory design pattern with essential and optional features.
    """
    graph = nx.DiGraph()

    # Essential Nodes
    graph.add_node("Product", type="interface")  # Essential: Interface or abstract class
    graph.add_node("ConcreteProductA", type="class")  # Essential: Concrete product
    graph.add_node("ConcreteProductB", type="class")  # Essential: Another concrete product
    graph.add_node("Factory", type="class")  # Essential: Factory class
    graph.add_node("createProductA", type="factory_method")  # Essential: Factory method
    graph.add_node("createProductB", type="factory_method")  # Essential: Another factory method

    # Optional Nodes
    graph.add_node("HelperClass", type="class")  # Optional: Helper class

    # Essential Edges
    graph.add_edge("ConcreteProductA", "Product", relation="implements")
    graph.add_edge("ConcreteProductB", "Product", relation="implements")
    graph.add_edge("Factory", "createProductA", relation="creates")
    graph.add_edge("Factory", "createProductB", relation="creates")

    # Optional Edges
    graph.add_edge("Factory", "HelperClass", relation="uses")

    # Save the graph
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'wb') as f:
        pickle.dump(graph, f)

    print(f"Representative graph saved to: {output_file}")


if __name__ == "__main__":
    # Specify the output file
    output_file = "graphs/factory_pattern_representative.gpickle"
    create_representative_factory_graph(output_file)
