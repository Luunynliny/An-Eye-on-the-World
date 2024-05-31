from tqdm import tqdm

from src.code import get_non_abrogated_codes
from src.graph import create_code_graph
from src.utils import generate_api_token

t_bar = tqdm(get_non_abrogated_codes(generate_api_token()), desc="Code retrieval")

for code_id, code_title in t_bar:
    t_bar.set_postfix_str(code_title)
    create_code_graph(code_id)
