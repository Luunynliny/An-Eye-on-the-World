from os.path import join, dirname
from xml.etree import ElementTree


class GEXFDocument:
    """
    GEFX Document class.
    """

    def __init__(self):
        self._tree: ElementTree.ElementTree = ElementTree.parse(join(dirname(__file__), 'template.gexf'))

        self._nodes: ElementTree.Element = self._tree.find(".//nodes")
        self._edges: ElementTree.Element = self._tree.find(".//edges")

    def add_node(self, node_id: str, node_label: str, node_attributes: list[str]) -> None:
        """
        Add a node to the document.

        Args:
            node_id (str): node id.
            node_label (str): node label.
            node_attributes (list[str]): node attributes.

        Returns:
            None
        """
        node = ElementTree.Element("node", {"id": node_id, "label": node_label})
        attributes = ElementTree.Element("attvalues")

        for i, value in enumerate(node_attributes):
            attribute = ElementTree.Element("attvalue", {"for": str(i), "value": value})
            attributes.append(attribute)

        node.append(attributes)
        self._nodes.append(node)

    def add_edge(self, edge_source: str, edge_target: str) -> None:
        """
        Add an edge to the document.

        Args:
            edge_source (str): edge source.
            edge_target (str): edge target.

        Returns:
            None
        """
        edge = ElementTree.Element("edge", {"source": edge_source, "target": edge_target})
        self._edges.append(edge)

    def save(self, filename: str) -> None:
        """
        Save the document.

        Args:
            filename (str): file name without extension.

        Returns:
            None
        """
        filepath = join(dirname(__file__), f"../gexf_files/{filename}.gexf")

        # Ensure proper XML formatting
        ElementTree.indent(self._tree, '    ')

        with open(filepath, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n' + ElementTree.tostring(self._tree.getroot()))
