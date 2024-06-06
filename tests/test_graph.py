from os import remove
from os.path import join, dirname, exists

import pytest

from src.code import get_code_title
from src.graph import create_code_graph
from src.utils import generate_api_token

CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"


@pytest.fixture
def api_token():
    return generate_api_token()


def test_create_code_graph(api_token):
    with open("gexf_code_deontologie_architectes.txt", 'r') as f:
        code_deontologie_architectes = f.read()

    create_code_graph(CODE_DEONTOLOGIE_ARCHITECTES_ID)
    filename = get_code_title(api_token, CODE_DEONTOLOGIE_ARCHITECTES_ID)

    filepath = join(dirname(__file__), f"../gexf_files/{filename}.gexf")
    assert exists(filepath)

    with open(filepath, 'r') as f:
        assert f.read() == code_deontologie_architectes

    # Delete file after test
    remove(filepath)
