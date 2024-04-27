from src.graph import create_code_graph

CODE_DOMAINE_ETAT_ID: str = "LEGITEXT000006070208"
# CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
CODES_LIST_URL: str = "https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR"

create_code_graph(CODE_DOMAINE_ETAT_ID)