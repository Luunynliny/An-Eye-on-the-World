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
