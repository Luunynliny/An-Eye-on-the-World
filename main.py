from src.graph import create_code_graph
from src.utils import generate_api_token

CODE_DOMAINE_ETAT_ID: str = "LEGITEXT000006070208"
CODE_CIVIL_ID: str = "LEGITEXT000006070721"
CODE_PENAL_ID: str = "LEGITEXT000006070719"
CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
CODE_ROUTE_ID: str = "LEGITEXT000006074228"

CODES_LIST_URL: str = "https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR"

create_code_graph(generate_api_token(), CODE_ROUTE_ID)
