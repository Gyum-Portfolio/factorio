import pickle
import networkx as nx


class GraphComparator:
    def __init__(self, representative_graph_file):
        """
        Initializes the GraphComparator with a representative graph.
        """
        with open(representative_graph_file, 'rb') as f:
            self.rep_graph = pickle.load(f)

        print("\n[DEBUG] Representative Graph Loaded")
        print("Nodes:", list(self.rep_graph.nodes(data=True)))
        print("Edges:", list(self.rep_graph.edges(data=True)))

    def compare(self, graph_file):
        """
        Compares the given graph file with the representative graph.
        """
        with open(graph_file, 'rb') as f:
            test_graph = pickle.load(f)

        print("\n[DEBUG] Test Graph Loaded")
        print("Nodes:", list(test_graph.nodes(data=True)))
        print("Edges:", list(test_graph.edges(data=True)))

        # Check essential characteristics
        essential_results = {
            "interface_exists": self._check_interface_exists(test_graph),
            "implementations_exist": self._check_implementations(test_graph),
            "factory_class_exists": self._check_factory_class(test_graph),
            "factory_methods_exist": self._check_factory_methods(test_graph),
        }

        print("\n[DEBUG] Essential Characteristic Results:")
        for characteristic, result in essential_results.items():
            print(f"  {characteristic}: {result}")

        # Adjusted logic: Require at least 2 out of 4 essential characteristics to match
        essential_match_count = sum(essential_results.values())
        is_match = essential_match_count >= 4

        # Confidence calculation: Based only on essential characteristics
        confidence = essential_match_count / len(essential_results)

        return is_match, confidence

    def _check_interface_exists(self, graph):
        """
        Checks if the graph contains at least one 'interface' node.
        """
        for _, attributes in graph.nodes(data=True):
            if attributes.get("type") == "interface":
                return True
        return False

    def _check_implementations(self, graph):
        """
        Checks if 'implements' edges connect 'class' nodes to 'interface' nodes.
        """
        for source, target, attributes in graph.edges(data=True):
            if attributes.get("relation") == "implements":
                if (graph.nodes[source].get("type") == "class" and
                        graph.nodes[target].get("type") == "interface"):
                    return True
        return False

    def _check_factory_class(self, graph):
        """
        Checks if a 'class' node representing a Factory exists.
        """
        for node, attributes in graph.nodes(data=True):
            if attributes.get("type") == "class" and "factory" in node.lower():
                return True
        return False

    def _check_factory_methods(self, graph):
        """
        Checks if 'factory_method' nodes exist and are connected via 'creates' or similar edges.
        """
        for source, target, attributes in graph.edges(data=True):
            if attributes.get("relation") in ["creates", "produces"]:
                if graph.nodes[source].get("type") == "class" and graph.nodes[target].get("type") == "factory_method":
                    return True
        return False


if __name__ == "__main__":
    # Specify the graph files
    rep_graph_file = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\test_graph\factory_pattern_representative.gpickle"
    test_graph_file = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\test_graph\044da794f471b62e65a1dc903a3f1dc71547f070.gpickle"

    # Initialize and run the comparator
    comparator = GraphComparator(rep_graph_file)
    is_match, confidence = comparator.compare(test_graph_file)

    # Print results
    print("\nFinal Results:")
    print(f"Match: {is_match}, Confidence: {confidence:.2f}")
