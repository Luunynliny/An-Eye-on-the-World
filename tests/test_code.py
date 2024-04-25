from src.code import get_code_non_abrogated_articles, get_code_name, get_code_soup

CODE_CIVIL_ID: str = "LEGITEXT000006070721"
CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
CODE_DOMAINE_ETAT_ID: str = "LEGITEXT000006070208"


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


def test_get_code_name():
    code_civil_soup = get_code_soup(CODE_CIVIL_ID)
    code_deontologie_architecture_soup = get_code_soup(CODE_DEONTOLOGIE_ARCHITECTES_ID)
    code_domaine_etat_soup = get_code_soup(CODE_DOMAINE_ETAT_ID)

    assert get_code_name(code_civil_soup) == "Code_civil"
    assert get_code_name(code_deontologie_architecture_soup) == "Code_de_déontologie_des_architectes"
    assert get_code_name(code_domaine_etat_soup) == "Code_du_domaine_de_l_Etat"
