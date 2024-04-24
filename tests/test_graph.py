from os import remove
from os.path import join, dirname, exists

from src.graph import create_code_graph
from src.utils import get_code_name

CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"


def test_create_code_graph():
    with open("gexf_code_deontologie_architectes.txt", 'r') as f:
        code_deontologie_architectes = f.read()

    create_code_graph(CODE_DEONTOLOGIE_ARCHITECTES_ID)
    filename = get_code_name(CODE_DEONTOLOGIE_ARCHITECTES_ID)

    filepath = join(dirname(__file__), f"../gexf_files/{filename}.gexf")
    assert exists(filepath)

    with open(filepath, 'r') as f:
        assert f.read() == code_deontologie_architectes

    # Delete file after test
    remove(filepath)
