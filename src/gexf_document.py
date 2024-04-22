from os.path import join, dirname
from xml.etree import ElementTree


class GEXFDocument:
    def __init__(self):
        self.tree: ElementTree.ElementTree = ElementTree.parse(join(dirname(__file__), 'template.gexf'))

        self.nodes: ElementTree.Element = self.tree.find(".//nodes")
        self.edges: ElementTree.Element = self.tree.find(".//edges")

    def add_node(self, node_id: str, node_label: str) -> None:
        """
        Args:
            node_id (str): node id.
            node_label (str): node label.

        Returns:
            None
        """
        node = ElementTree.Element("node", {"id": node_id, "label": node_label})
        self.nodes.append(node)

    def add_edge(self, edge_source: str, edge_target: str) -> None:
        """
        Args:
            edge_source (): edge source.
            edge_target (): edge target.

        Returns:
            None
        """
        edge = ElementTree.Element("node", {"source": edge_source, "target": edge_target})
        self.edges.append(edge)
