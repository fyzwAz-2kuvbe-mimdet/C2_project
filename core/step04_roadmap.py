from config.learning_types import get_type
from core.llm_client import ask
from prompts.mentoring_prompts import (
    GRADE_TONE_GUIDE, STEP04_ROADMAP, SYSTEM_BASE, TYPE_QUESTION_STYLE,
)


def _grade_group(grade: str) -> str:
    return "초등" if grade.startswith("초") else ("중등" if grade.startswith("중") else "고등")


def build_prompt(refined_topic: str, key_concepts: list, grade: str, learning_type_id: str) -> tuple:
    info = get_type(learning_type_id)
    system = SYSTEM_BASE.format(
        type_name=info["name"], type_core=info["core"], grade=grade,
        tone_guide=GRADE_TONE_GUIDE[_grade_group(grade)],
        question_style=TYPE_QUESTION_STYLE[learning_type_id],
    )
    user = STEP04_ROADMAP.format(
        refined_topic=refined_topic,
        key_concepts=", ".join(key_concepts),
        grade=grade,
        type_name=info["name"],
        type_core=info["core"],
    )
    return system, user


def build_roadmap(refined_topic: str, key_concepts: list, grade: str, learning_type_id: str) -> list:
    system, user = build_prompt(refined_topic, key_concepts, grade, learning_type_id)
    result = ask(system, user, json_mode=True)
    return result if isinstance(result, list) else []
