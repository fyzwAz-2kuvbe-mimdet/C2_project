import json
from prompts.mentoring_prompts import STEP01_KEYWORD, get_system_prompt


def build_prompt(keyword: str, learning_type: str = "hana") -> tuple:
    user = STEP01_KEYWORD.format(keyword=keyword)
    return get_system_prompt(learning_type), user
