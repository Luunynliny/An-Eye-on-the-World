from icecream import ic
from tqdm import tqdm

from src.article import get_article_data, get_article_citation_data, get_article_hierarchy
from src.code import get_code_non_abrogated_articles, get_code_soup, get_code_title
from src.gexf_document import GEXFDocument


def create_code_graph(api_token: str, code_id: str) -> None:
    """
    Create a GEFX document graph of a Code.

    Args:
        api_token (str): API token.
        code_id (str): Code id.

    Returns:
        None
    """
    # Init GEXF document
    gexf_doc: GEXFDocument = GEXFDocument()

    # Retrieve all Code Articles
    code_soup = get_code_soup(code_id)
    seen_article_ids: set[str] = set()

    for article_id in tqdm(get_code_non_abrogated_articles(code_soup), desc="Article retrieval"):

        ic(article_id)

        if article_id not in seen_article_ids:
            article_number, article_text_length = get_article_data(api_token, article_id)

            # Create GEXF node
            gexf_doc.add_node(article_id, f"Article {article_number}",
                              node_attributes=[code_id, get_article_hierarchy(article_number),
                                               str(article_text_length)])

            seen_article_ids.add(article_id)

        # Create citation links
        for citation_id, citation_code_parent_id in get_article_citation_data(api_token, article_id):
            gexf_doc.add_edge(article_id, citation_id)

            if citation_id not in seen_article_ids:
                citation_number, citation_text_length = get_article_data(api_token, citation_id)

                # Create quoted nodes
                gexf_doc.add_node(citation_id, f"Article {citation_number}",
                                  node_attributes=[citation_code_parent_id,
                                                   get_article_hierarchy(citation_number),
                                                   str(citation_text_length)])

                seen_article_ids.add(citation_id)

    # Save result
    gexf_doc.save(get_code_title(api_token, code_id))
