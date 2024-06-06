import pytest

from src.article import get_article_data, get_article_hierarchy, get_article_citation_data
from src.utils import generate_api_token

CODE_CIVIL_ARTICLE_1_ID: str = "LEGIARTI000006419280"
CODE_CIVIL_ARTICLE_21_19_ID: str = "LEGIARTI000006419879"
CODE_CIVIL_ARTICLE_92_ID: str = "LEGIARTI000006421376"

CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID: str = "LEGIARTI000006842411"

CODE_DOMAINE_ETAT_ARTICLE_R1_ID: str = "LEGIARTI000006350500"
CODE_DOMAINE_ETAT_ARTICLE_L3_ID: str = "LEGIARTI000006350304"
CODE_DOMAINE_ETAT_ARTICLE_A1_ID: str = "LEGIARTI000006350040"

CODE_ELECTORAL_ARTICLE_LO119_ID: str = "LEGIARTI000020103138"
CODE_ELECTORAL_ARTICLE_Rstarstar273_ID: str = "LEGIARTI000006355123"

CODE_PROCEDURE_PENALE_ARTICLE_D1_ID: str = "LEGIARTI000033328430"

CODE_URBANISME_ARTICLE_L101_1_ID: str = "LEGIARTI000031210068"
CODE_URBANISME_ARTICLE_Rstar121_1_1_ID: str = "LEGIARTI000047750711"
CODE_URBANISME_ARTICLE_A424_1_ID: str = "LEGIARTI000006814020"

CODE_MONETAIRE_FINANCIER_Dstar752_25_ID: str = "LEGIARTI000046632944"

CODE_CONSOMMATION_L432_6_ID: str = "LEGIARTI000032222797"


@pytest.fixture
def api_token():
    return generate_api_token()


def test_get_article_data(api_token):
    assert get_article_data(api_token, CODE_CIVIL_ARTICLE_1_ID) == ("1", 101)
    assert get_article_data(api_token, CODE_CIVIL_ARTICLE_21_19_ID) == ("21-19", 134)
    assert get_article_data(api_token, CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID) == ("1", 28)
    assert get_article_data(api_token, CODE_ELECTORAL_ARTICLE_Rstarstar273_ID) == ("R**273", 25)

    # Article not avaible or not created at the date
    assert get_article_data(api_token, CODE_CONSOMMATION_L432_6_ID) == (None, None)


def test_get_article_citation_data(api_token):
    # Article quote other Codes Articles
    assert get_article_citation_data(api_token, CODE_CIVIL_ARTICLE_92_ID) == [
        ("LEGIARTI000006421855", "LEGITEXT000006070721"),
        ("LEGIARTI000006421836", "LEGITEXT000006070721"),
        ("LEGIARTI000006421846", "LEGITEXT000006070721"),
        ("LEGIARTI000039367547", "LEGITEXT000006070721")]

    # Article quote abrogated Code Articles
    assert get_article_citation_data(api_token, CODE_DOMAINE_ETAT_ARTICLE_R1_ID) == [
        ("LEGIARTI000006350687", "LEGITEXT000006070208")]

    # Article does not quoted other Codes Articles
    assert get_article_citation_data(api_token, CODE_CIVIL_ARTICLE_21_19_ID) == []

    # Article does not quoted
    assert get_article_citation_data(api_token, CODE_CIVIL_ARTICLE_1_ID) == []

    # Article is an orphan
    assert get_article_citation_data(api_token, CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID) == []

    # Not Code Article, but contains art. (Loi n°51-1508 du 31 décembre 1951 - art. 15, v. init.)
    assert get_article_citation_data(api_token, CODE_DOMAINE_ETAT_ARTICLE_A1_ID) == [
        ('LEGIARTI000006350512', 'LEGITEXT000006070208'),
        ('LEGIARTI000006350707', 'LEGITEXT000006070208'),
        ('LEGIARTI000045525641', 'LEGITEXT000006074075')]


def test_get_article_hierarchy():
    assert get_article_hierarchy("L101-1") == "L"
    assert get_article_hierarchy("LO119") == "LO"
    assert get_article_hierarchy("R1") == "R"
    assert get_article_hierarchy("D1") == "D"
    assert get_article_hierarchy("R*121-1-1") == "R*"
    assert get_article_hierarchy("R**273") == "R**"
    assert get_article_hierarchy("D*752_25") == "D*"
    assert get_article_hierarchy("A424-1") == "A"
    assert get_article_hierarchy("21-19") == "NC"
