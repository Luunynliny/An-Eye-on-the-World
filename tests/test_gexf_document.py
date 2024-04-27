from os import remove
from os.path import join, dirname, exists
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

    assert isinstance(gexf_doc._tree, ElementTree.ElementTree)
    assert parseString(ElementTree.tostring(gexf_doc._tree.getroot())).toxml() == template

    assert isinstance(gexf_doc._nodes, ElementTree.Element)
    assert len(gexf_doc._nodes) == 0

    assert isinstance(gexf_doc._edges, ElementTree.Element)
    assert len(gexf_doc._edges) == 0


def test_add_node(gexf_doc):
    gexf_doc.add_node("a", "node_a", [])

    assert len(gexf_doc._nodes) == 1
    assert all([isinstance(node, ElementTree.Element)] for node in gexf_doc._nodes)
    assert [node.items() for node in gexf_doc._nodes] == [[("id", "a"), ("label", "node_a")]]

    gexf_doc.add_node("b", "node_b", [])

    assert len(gexf_doc._nodes) == 2
    assert all([isinstance(node, ElementTree.Element)] for node in gexf_doc._nodes)
    assert [node.items() for node in gexf_doc._nodes] == [[("id", "a"), ("label", "node_a")],
                                                          [("id", "b"), ("label", "node_b")]]


def test_add_edge(gexf_doc):
    gexf_doc.add_edge("node_a", "node_b")

    assert len(gexf_doc._edges) == 1
    assert all([isinstance(edge, ElementTree.Element)] for edge in gexf_doc._edges)
    assert [edge.items() for edge in gexf_doc._edges] == [[("source", "node_a"), ("target", "node_b")]]

    gexf_doc.add_edge("node_b", "node_c")

    assert len(gexf_doc._edges) == 2
    assert all([isinstance(edge, ElementTree.Element)] for edge in gexf_doc._edges)
    assert [edge.items() for edge in gexf_doc._edges] == [[("source", "node_a"), ("target", "node_b")],
                                                          [("source", "node_b"), ("target", "node_c")]]


def test_save(gexf_doc):
    with open("gexf_saved_blank.txt", 'r') as f:
        blank = f.read()

    with open("gexf_saved_hello_world.txt", 'r') as f:
        hello_world = f.read()

    filename = "__test"
    filepath = join(dirname(__file__), f"../gexf_files/{filename}.gexf")

    # Empty file
    gexf_doc.save(filename)

    assert exists(filepath)

    with open(filepath, 'r') as f:
        assert f.read() == blank

    # Add nodes and edge
    gexf_doc.add_node("0", "Hello", ["AAA", "BBB", "10"])
    gexf_doc.add_node("1", "World", ["CCC", "DDD", "5"])
    gexf_doc.add_edge("0", "1")

    gexf_doc.save(filename)

    assert exists(filepath)

    with open(filepath, 'r') as f:
        assert f.read() == hello_world

    # Delete file after test
    remove(filepath)
