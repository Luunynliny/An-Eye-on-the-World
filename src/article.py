import requests

from src.utils import API_BASE_URL, wait

ARTICLE_HIERARCHY = ["LO",  # Article LO119 Code électoral (2024-04-20)
                     "L",  # Article L101-1 Code de l'urbanisme (2024-04-20)
                     "R**",  # Article R**273 Code électoral (2024-04-20)
                     "R*",  # Article R*121-1-1 Code de l'urbanisme (2024-04-20)
                     "R",  # Article R1 Code électoral (2024-04-20)
                     "D*",  # Article D*752-25 Code monétaire et financier (2024-04-20)
                     "D",  # Article D1 Code de procédure pénale (2024-04-20)
                     "A"]  # Article A424-1 Code de l'urbanisme (2024-04-20)


@wait
def get_article_data(api_token: str, article_id: str):  # -> tuple[str, str] | tuple[None, None]:
    """
    Get Article data.

    Args:
        api_token (str): API token.
        article_id (str): Article id.

    Returns:
        tuple[str, str] | tuple[None, None]: Article number and text length, None and None if article is unavailable.
    """
    url = f"{API_BASE_URL}/consult/getArticle"
    headers = {"Authorization": f"Bearer {api_token}"}

    data = {
        "id": article_id,
    }

    response = requests.post(url, json=data, headers=headers).json()

    if response["article"] is None:
        return None, None

    return response["article"]["num"], len(response["article"]["texte"].split())


@wait
def get_article_citation_data(api_token: str, article_id: str) -> list[tuple[str, str]]:
    """
    Get Code Articles quoted by the Article.

    Args:
        api_token (str): API token.
        article_id (str): Article id.

    Returns:
        list[tuple[str, str]]: Article ids and Code parent ids.
    """
    url = f"{API_BASE_URL}/consult/relatedLinksArticle"
    headers = {"Authorization": f"Bearer {api_token}"}

    data = {
        "articleId": article_id,
    }

    response = requests.post(url, json=data, headers=headers).json()

    citations = []
    for citation in response.get("liensCite", []):
        if citation["nature"] != "CODE":
            continue

        # Avoid abrogated unremoved quotation (e.g. Code du domaine de l'Etat Article R1 (2024-04-20))
        if citation["dateVigeur"] is None:
            continue

        if citation["dateVigeur"] < 0:
            continue

        if "art." not in citation["name"]:
            continue

        citations.append((citation["id"], citation["cidText"]))

    return citations


def get_article_hierarchy(article_number: str) -> str:
    """
    Get article hierarchy.

    Args:
        article_number (str): Article number.

    Returns:
        str: Article hierarchy group.
    """

    for code in ARTICLE_HIERARCHY:
        if code in article_number:
            return code

    # Special case for the Code with no division in parts
    # Code civil, Code de déontologie architectes...
    return "NC"
