import json
import networkx as nx
import javalang
from pathlib import Path
import pickle


class DataToGraph:
    def __init__(self, json_file):
        """
        Initializes the DataToGraph class by loading the JSON file.
        """
        current_dir = Path(__file__).parent
        file_path = current_dir / json_file
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def create_graph_from_java(self, code):
        """
        Parses the Java code and creates a graph representation focused on Factory relationships.
        """
        graph = nx.DiGraph()
        try:
            tokens = javalang.tokenizer.tokenize(code)
            parser = javalang.parser.Parser(tokens)
            tree = parser.parse()
            self._extract_relevant_relationships(tree, graph)
        except javalang.parser.JavaSyntaxError as e:
            print(f"JavaSyntaxError while parsing code: {e}")
            print("Problematic code snippet:")
            print(code[:500])
        except Exception as e:
            print(f"Error while creating graph: {e}")
        return graph

    def _extract_relevant_relationships(self, node, graph, parent=None):
        """
        Extracts only important relationships such as 'creates', 'implements', and related methods.
        """
        factory_prefixes = ['create', 'make', 'build', 'generate', 'construct', 'produce', 'new', 'get']

        if isinstance(node, javalang.tree.ClassDeclaration):
            graph.add_node(node.name, type="class")
            if parent:
                graph.add_edge(parent, node.name, relation="contains")
            print(f"Added class node: {node.name}")

            # Look for 'implements' relationships
            if node.implements:
                for interface in node.implements:
                    graph.add_node(interface.name, type="interface")
                    graph.add_edge(node.name, interface.name, relation="implements")
                    print(f"Added implements edge: {node.name} -> {interface.name}")

            # Traverse class members
            for member in node.body:
                self._extract_relevant_relationships(member, graph, parent=node.name)

        elif isinstance(node, javalang.tree.MethodDeclaration):
            # Look for factory methods with expanded prefixes
            if any(node.name.startswith(prefix) for prefix in factory_prefixes):
                graph.add_node(node.name, type="factory_method")
                if parent:
                    graph.add_edge(parent, node.name, relation="creates")
                print(f"Added factory method: {node.name}")

        elif hasattr(node, "children"):
            for child in node.children:
                if isinstance(child, list):
                    for subchild in child:
                        self._extract_relevant_relationships(subchild, graph, parent=parent)
                else:
                    self._extract_relevant_relationships(child, graph, parent=parent)

    def process_and_save(self, output_dir="graphs"):
        """
        Processes the "after" code from the JSON file and saves the generated graphs.
        """
        current_dir = Path(__file__).parent
        output_path = current_dir / output_dir
        output_path.mkdir(parents=True, exist_ok=True)

        for item in self.data:
            code = item.get("after", "")
            if not code.strip():
                print(f"Skipping empty 'after' code for commit: {item.get('commit_sha', 'unknown')}")
                continue
            print(f"Processing commit: {item['commit_sha']}")
            graph = self.create_graph_from_java(code)

            # Debugging: Print the nodes and edges of the graph
            print("Generated Graph Details:")
            print("Nodes:", list(graph.nodes(data=True)))
            print("Edges:", list(graph.edges(data=True)))

            filename = output_path / f"{item['commit_sha']}.gpickle"
            with open(filename, 'wb') as f:
                pickle.dump(graph, f)
                print(f"Graph saved: {filename}")


if __name__ == "__main__":
    # Specify the input JSON file and output directory
    json_file = r"C:\Users\gyumc\OneDrive\바탕 화면\ML4SE\team-12\Data_collection\dataset\6.json"
    dtg = DataToGraph(json_file)
    dtg.process_and_save("graphs")
