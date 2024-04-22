from os.path import join, dirname
from xml.etree import ElementTree


class GEXFDocument:
    def __init__(self):
        self.tree: ElementTree.ElementTree = ElementTree.parse(join(dirname(__file__), 'template.gexf'))

        self.nodes: ElementTree.Element = self.tree.find(".//nodes")
        self.edges: ElementTree.Element = self.tree.find(".//edges")
