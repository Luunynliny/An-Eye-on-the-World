import pytest
from selenium import webdriver

from src.article import get_article_name, get_article_soup, is_article_abrogated, \
    get_article_text_length, get_article_quote_ids, get_article_hierarchy

CODE_CIVIL_ARTICLE_1_ID: str = "LEGIARTI000006419280"
CODE_CIVIL_ARTICLE_21_19_ID: str = "LEGIARTI000006419879"
CODE_CIVIL_ARTICLE_92_ID: str = "LEGIARTI000006421376"

CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID: str = "LEGIARTI000006842411"

CODE_DOMAINE_ETAT_ARTICLE_R1_ID: str = "LEGIARTI000006350500"
CODE_DOMAINE_ETAT_ARTICLE_L3_ID: str = "LEGIARTI000006350304"

CODE_ELECTORAL_ARTICLE_LO119_ID: str = "LEGIARTI000020103138"
CODE_ELECTORAL_ARTICLE_Rstarstar273_ID: str = "LEGIARTI000006355123"

CODE_PROCEDURE_PENALE_ARTICLE_D1_ID: str = "LEGIARTI000033328430"

CODE_URBANISME_ARTICLE_L101_1_ID: str = "LEGIARTI000031210068"
CODE_URBANISME_ARTICLE_Rstar121_1_1_ID: str = "LEGIARTI000047750711"
CODE_URBANISME_ARTICLE_A424_1_ID: str = "LEGIARTI000006814020"

CODE_MONETAIRE_FINANCIER_Dstar752_25_ID: str = "LEGIARTI000046632944"


@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    yield driver

    driver.quit()


def test_get_article_name():
    code_civil_article_1_soup = get_article_soup(CODE_CIVIL_ARTICLE_1_ID)
    code_civil_article_21_19_soup = get_article_soup(CODE_CIVIL_ARTICLE_21_19_ID)
    code_deontologie_architectes_article_1_soup = get_article_soup(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID)

    assert get_article_name(code_civil_article_1_soup) == "Article 1"
    assert get_article_name(code_civil_article_21_19_soup) == "Article 21-19"
    assert get_article_name(code_deontologie_architectes_article_1_soup)


def test_is_article_abrogated():
    code_civil_article_92_soup = get_article_soup(CODE_CIVIL_ARTICLE_92_ID)
    code_domaine_etat_article_l3_soup = get_article_soup(CODE_DOMAINE_ETAT_ARTICLE_L3_ID)

    assert not is_article_abrogated(code_civil_article_92_soup)
    assert is_article_abrogated(code_domaine_etat_article_l3_soup)


def test_get_article_text_length():
    code_civil_article_1_soup = get_article_soup(CODE_CIVIL_ARTICLE_1_ID)
    code_civil_article_92_soup = get_article_soup(CODE_CIVIL_ARTICLE_92_ID)
    code_deontologie_architectes_article_1_soup = get_article_soup(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID)

    assert get_article_text_length(code_civil_article_1_soup) == 101
    assert get_article_text_length(code_civil_article_92_soup) == 64
    assert get_article_text_length(code_deontologie_architectes_article_1_soup) == 28


def test_get_article_quote_ids(driver):
    # Article quote other Codes Articles
    code_civil_article_92_soup = get_article_soup(CODE_CIVIL_ARTICLE_92_ID)

    assert get_article_quote_ids(code_civil_article_92_soup, driver) == ["LEGIARTI000006421855", "LEGIARTI000006421836",
                                                                         "LEGIARTI000006421846",
                                                                         "LEGIARTI000039367547"]

    # Article quote abrogated Code Articles
    code_domaine_etat_article_r1_soup = get_article_soup(CODE_DOMAINE_ETAT_ARTICLE_R1_ID)

    assert get_article_quote_ids(code_domaine_etat_article_r1_soup, driver) == ["LEGIARTI000006350687"]

    # Article does not quoted other Codes Articles
    code_civil_article_21_19_soup = get_article_soup(CODE_CIVIL_ARTICLE_21_19_ID)

    assert get_article_quote_ids(code_civil_article_21_19_soup, driver) == []

    # Article does not quoted
    code_civil_article_1_soup = get_article_soup(CODE_CIVIL_ARTICLE_1_ID)

    assert get_article_quote_ids(code_civil_article_1_soup, driver) == []

    # Article is an orphan
    code_deontologie_architectes_article_1_soup = get_article_soup(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID)

    assert get_article_quote_ids(code_deontologie_architectes_article_1_soup, driver) == []


def test_get_article_hierarchy():
    code_urbanisme_article_l101_1_soup = get_article_soup(CODE_URBANISME_ARTICLE_L101_1_ID)
    code_electoral_article_lo119_soup = get_article_soup(CODE_ELECTORAL_ARTICLE_LO119_ID)
    code_domaine_etat_article_r1_soup = get_article_soup(CODE_DOMAINE_ETAT_ARTICLE_R1_ID)
    code_procedure_penale_article_d1_soup = get_article_soup(CODE_PROCEDURE_PENALE_ARTICLE_D1_ID)
    code_urbanisme_article_rstart121_1_1_soup = get_article_soup(CODE_URBANISME_ARTICLE_Rstar121_1_1_ID)
    code_electoral_article_rstartstar273_soup = get_article_soup(CODE_ELECTORAL_ARTICLE_Rstarstar273_ID)
    code_monetaire_financier_article_dstart752_25_soup = get_article_soup(CODE_MONETAIRE_FINANCIER_Dstar752_25_ID)
    code_urbanisme_article_a424_1_soup = get_article_soup(CODE_URBANISME_ARTICLE_A424_1_ID)
    code_civil_article_21_19_soup = get_article_soup(CODE_CIVIL_ARTICLE_21_19_ID)

    assert get_article_hierarchy(code_urbanisme_article_l101_1_soup) == "L"
    assert get_article_hierarchy(code_electoral_article_lo119_soup) == "LO"
    assert get_article_hierarchy(code_domaine_etat_article_r1_soup) == "R"
    assert get_article_hierarchy(code_procedure_penale_article_d1_soup) == "D"
    assert get_article_hierarchy(code_urbanisme_article_rstart121_1_1_soup) == "R*"
    assert get_article_hierarchy(code_electoral_article_rstartstar273_soup) == "R**"
    assert get_article_hierarchy(code_monetaire_financier_article_dstart752_25_soup) == "D*"
    assert get_article_hierarchy(code_urbanisme_article_a424_1_soup) == "A"
    assert get_article_hierarchy(code_civil_article_21_19_soup) == "CC"
