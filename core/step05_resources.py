from config.learning_types import get_type
from core.llm_client import ask
from prompts.mentoring_prompts import (
    GRADE_TONE_GUIDE, STEP05_RESOURCES, SYSTEM_BASE, TYPE_QUESTION_STYLE,
)


def _grade_group(grade: str) -> str:
    return "초등" if grade.startswith("초") else ("중등" if grade.startswith("중") else "고등")


def build_prompt(roadmap: list, refined_topic: str, grade: str, learning_type_id: str) -> tuple:
    info = get_type(learning_type_id)
    system = SYSTEM_BASE.format(
        type_name=info["name"], type_core=info["core"], grade=grade,
        tone_guide=GRADE_TONE_GUIDE[_grade_group(grade)],
        question_style=TYPE_QUESTION_STYLE[learning_type_id],
    )
    roadmap_text = "\n".join(
        f"단계 {r['step_number']}: {r['goal']} (예상 {r.get('estimated_hours', '')})"
        for r in roadmap
    )
    preferred = ", ".join(info.get("preferred_sources", []))
    user = STEP05_RESOURCES.format(
        refined_topic=refined_topic,
        roadmap_text=roadmap_text,
        grade=grade,
        type_name=info["name"],
        preferred_sources=preferred,
    )
    return system, user


def recommend(roadmap: list, refined_topic: str, grade: str, learning_type_id: str) -> dict:
    system, user = build_prompt(roadmap, refined_topic, grade, learning_type_id)
    result = ask(system, user, json_mode=True)
    return result if isinstance(result, dict) else {}
