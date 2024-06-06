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
    assert codes == [('LEGITEXT000006070721', 'Code civil'),
                     ('LEGITEXT000005634379', 'Code de commerce'),
                     ('LEGITEXT000006074232', 'Code de déontologie des architectes'),
                     ('LEGITEXT000006070933', 'Code de justice administrative'),
                     ('LEGITEXT000006071360', 'Code de justice militaire (nouveau)'),
                     ('LEGITEXT000006074069', "Code de l'action sociale et des familles"),
                     ('LEGITEXT000006075116', "Code de l'artisanat"),
                     ('LEGITEXT000006074234', "Code de l'aviation civile"),
                     ('LEGITEXT000006070158',
                      "Code de l'entrée et du séjour des étrangers et du droit d'asile"),
                     ('LEGITEXT000006074220', "Code de l'environnement"),
                     ('LEGITEXT000006074224',
                      "Code de l'expropriation pour cause d'utilité publique"),
                     ('LEGITEXT000006071164', "Code de l'organisation judiciaire"),
                     ('LEGITEXT000006074075', "Code de l'urbanisme"),
                     ('LEGITEXT000006071191', "Code de l'éducation"),
                     ('LEGITEXT000023983208', "Code de l'énergie"),
                     ('LEGITEXT000037673300',
                      "Code de la Légion d'honneur, de la Médaille militaire et de l'ordre "
                      'national du Mérite'),
                     ('LEGITEXT000037701019', 'Code de la commande publique'),
                     ('LEGITEXT000006069565', 'Code de la consommation'),
                     ('LEGITEXT000006074096', "Code de la construction et de l'habitation"),
                     ('LEGITEXT000006071307', 'Code de la défense'),
                     ('LEGITEXT000006072637', "Code de la famille et de l'aide sociale"),
                     ('LEGITEXT000039086952', 'Code de la justice pénale des mineurs'),
                     ('LEGITEXT000006074067', 'Code de la mutualité'),
                     ('LEGITEXT000006069414', 'Code de la propriété intellectuelle'),
                     ('LEGITEXT000006071190', 'Code de la recherche'),
                     ('LEGITEXT000006074228', 'Code de la route'),
                     ('LEGITEXT000006072665', 'Code de la santé publique'),
                     ('LEGITEXT000025503132', 'Code de la sécurité intérieure'),
                     ('LEGITEXT000006073189', 'Code de la sécurité sociale'),
                     ('LEGITEXT000006070667', 'Code de la voirie routière'),
                     ('LEGITEXT000006070716', 'Code de procédure civile'),
                     ('LEGITEXT000006071154', 'Code de procédure pénale'),
                     ('LEGITEXT000006073984', 'Code des assurances'),
                     ('LEGITEXT000006070162', 'Code des communes'),
                     ('LEGITEXT000006070300', 'Code des communes de la Nouvelle-Calédonie'),
                     ('LEGITEXT000006071570', 'Code des douanes'),
                     ('LEGITEXT000006071645', 'Code des douanes de Mayotte'),
                     ('LEGITEXT000044595989', 'Code des impositions sur les biens et services'),
                     ('LEGITEXT000006070666', 'Code des instruments monétaires et des médailles'),
                     ('LEGITEXT000006070249', 'Code des juridictions financières'),
                     ('LEGITEXT000006070302',
                      'Code des pensions civiles et militaires de retraite'),
                     ('LEGITEXT000006074066',
                      'Code des pensions de retraite des marins français du commerce, de pêche ou '
                      'de plaisance'),
                     ('LEGITEXT000031712069',
                      "Code des pensions militaires d'invalidité et des victimes de guerre"),
                     ('LEGITEXT000006074233', 'Code des ports maritimes'),
                     ('LEGITEXT000006070987',
                      'Code des postes et des communications électroniques'),
                     ('LEGITEXT000025024948', "Code des procédures civiles d'exécution"),
                     ('LEGITEXT000031366350',
                      "Code des relations entre le public et l'administration"),
                     ('LEGITEXT000023086525', 'Code des transports'),
                     ('LEGITEXT000006071188', 'Code disciplinaire et pénal de la marine marchande'),
                     ('LEGITEXT000020908868', "Code du cinéma et de l'image animée"),
                     ('LEGITEXT000006070208', "Code du domaine de l'Etat"),
                     ('LEGITEXT000006074235',
                      "Code du domaine de l'Etat et des collectivités publiques applicable à la "
                      'collectivité territoriale de Mayotte'),
                     ('LEGITEXT000006074237',
                      'Code du domaine public fluvial et de la navigation intérieure'),
                     ('LEGITEXT000006074236', 'Code du patrimoine'),
                     ('LEGITEXT000006071335', 'Code du service national'),
                     ('LEGITEXT000006071318', 'Code du sport'),
                     ('LEGITEXT000006074073', 'Code du tourisme'),
                     ('LEGITEXT000006072050', 'Code du travail'),
                     ('LEGITEXT000006072051', 'Code du travail maritime'),
                     ('LEGITEXT000025244092', 'Code forestier (nouveau)'),
                     ('LEGITEXT000044416551', 'Code général de la fonction publique'),
                     ('LEGITEXT000006070299',
                      'Code général de la propriété des personnes publiques'),
                     ('LEGITEXT000006070633', 'Code général des collectivités territoriales'),
                     ('LEGITEXT000006069577', 'Code général des impôts'),
                     ('LEGITEXT000006069568', 'Code général des impôts, annexe I'),
                     ('LEGITEXT000006069569', 'Code général des impôts, annexe II'),
                     ('LEGITEXT000006069574', 'Code général des impôts, annexe III'),
                     ('LEGITEXT000006069576', 'Code général des impôts, annexe IV'),
                     ('LEGITEXT000006071785', 'Code minier'),
                     ('LEGITEXT000023501962', 'Code minier (nouveau)'),
                     ('LEGITEXT000006072026', 'Code monétaire et financier'),
                     ('LEGITEXT000006070719', 'Code pénal'),
                     ('LEGITEXT000045476241', 'Code pénitentiaire'),
                     ('LEGITEXT000006071366', 'Code rural (ancien)'),
                     ('LEGITEXT000022197698', 'Code rural et de la pêche maritime'),
                     ('LEGITEXT000006070239', 'Code électoral'),
                     ('LEGITEXT000006069583', 'Livre des procédures fiscales')]


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
