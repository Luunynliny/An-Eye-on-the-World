from xml.dom.minidom import parseString
from xml.etree import ElementTree

import pytest

from src.gexf_document import GEXFDocument


@pytest.fixture
def gexf_doc():
    return GEXFDocument()


def test_init(gexf_doc):
    with open("gexf_template.txt", 'r') as f:
        template = f.read()

    assert isinstance(gexf_doc.tree, ElementTree.ElementTree)
    assert parseString(ElementTree.tostring(gexf_doc.tree.getroot())).toxml() == template

    assert isinstance(gexf_doc.nodes, ElementTree.Element)
    assert len(gexf_doc.nodes) == 0

    assert isinstance(gexf_doc.edges, ElementTree.Element)
    assert len(gexf_doc.edges) == 0


def test_add_node(gexf_doc):
    gexf_doc.add_node("a", "node_a")

    assert len(gexf_doc.nodes) == 1
    assert all([isinstance(node, ElementTree.Element)] for node in gexf_doc.nodes)
    assert [node.items() for node in gexf_doc.nodes] == [[("id", "a"), ("label", "node_a")]]

    gexf_doc.add_node("b", "node_b")

    assert len(gexf_doc.nodes) == 2
    assert all([isinstance(node, ElementTree.Element)] for node in gexf_doc.nodes)
    assert [node.items() for node in gexf_doc.nodes] == [[("id", "a"), ("label", "node_a")],
                                                         [("id", "b"), ("label", "node_b")]]


def test_add_edge(gexf_doc):
    gexf_doc.add_edge("node_a", "node_b")

    assert len(gexf_doc.edges) == 1
    assert all([isinstance(edge, ElementTree.Element)] for edge in gexf_doc.edges)
    assert [edge.items() for edge in gexf_doc.edges] == [[("source", "node_a"), ("target", "node_b")]]

    gexf_doc.add_edge("node_b", "node_c")

    assert len(gexf_doc.edges) == 2
    assert all([isinstance(edge, ElementTree.Element)] for edge in gexf_doc.edges)
    assert [edge.items() for edge in gexf_doc.edges] == [[("source", "node_a"), ("target", "node_b")],
                                                         [("source", "node_b"), ("target", "node_c")]]