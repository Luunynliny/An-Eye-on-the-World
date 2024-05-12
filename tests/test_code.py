import pytest

from src.code import get_non_abrogated_codes, get_code_non_abrogated_articles, get_code_soup, get_code_title
from src.utils import generate_api_token

CODE_CIVIL_ID: str = "LEGITEXT000006070721"
CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
CODE_DOMAINE_ETAT_ID: str = "LEGITEXT000006070208"


@pytest.fixture
def api_token():
    return generate_api_token()


def test_get_non_abrogated_codes(api_token):
    codes = get_non_abrogated_codes(api_token)

    assert isinstance(codes, list)
    assert len(codes) == 77  # As for now, May 2024, there are 77 Codes in effect


def test_get_code_non_abrogated_articles():
    code_civil_soup = get_code_soup(CODE_CIVIL_ID)
    code_deontologie_architecture_soup = get_code_soup(CODE_DEONTOLOGIE_ARCHITECTES_ID)

    article_ids = get_code_non_abrogated_articles(code_civil_soup)

    assert isinstance(article_ids, list)
    assert len(article_ids) == 2883
    assert isinstance(article_ids[0], str)
    assert article_ids[0] == "LEGIARTI000006419280"

    article_ids = get_code_non_abrogated_articles(code_deontologie_architecture_soup)

    assert isinstance(article_ids, list)
    assert len(article_ids) == 48
    assert isinstance(article_ids[0], str)
    assert article_ids[0] == "LEGIARTI000006842411"


def test_get_code_title(api_token):
    assert get_code_title(api_token, CODE_CIVIL_ID) == "Code_civil"
    assert get_code_title(api_token, CODE_DEONTOLOGIE_ARCHITECTES_ID) == "Code_de_déontologie_des_architectes"
    assert get_code_title(api_token, CODE_DOMAINE_ETAT_ID) == "Code_du_domaine_de_l_Etat"
