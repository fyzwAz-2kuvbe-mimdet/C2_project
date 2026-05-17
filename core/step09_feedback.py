from config.learning_types import get_criteria, get_type
from core.llm_client import ask
from prompts.mentoring_prompts import (
    GRADE_TONE_GUIDE, STEP09_FEEDBACK, SYSTEM_BASE, TYPE_QUESTION_STYLE,
)


def _grade_group(grade: str) -> str:
    return "초등" if grade.startswith("초") else ("중등" if grade.startswith("중") else "고등")


def build_prompt(student_text: str, format_type: str, grade: str, learning_type_id: str) -> tuple:
    info = get_type(learning_type_id)
    criteria = get_criteria(learning_type_id)
    gg = _grade_group(grade)
    system = SYSTEM_BASE.format(
        type_name=info["name"], type_core=info["core"], grade=grade,
        tone_guide=GRADE_TONE_GUIDE[gg],
        question_style=TYPE_QUESTION_STYLE[learning_type_id],
    )
    criteria_text = "\n".join(f"- [{c['key']}] {c['label']} (가중치 {c['weight']}%)" for c in criteria)
    criteria_keys = ", ".join(f'"{c["key"]}": 점수' for c in criteria)
    user = STEP09_FEEDBACK.format(
        student_text=student_text,
        format_type=format_type,
        grade=grade,
        type_name=info["name"],
        type_core=info["core"],
        criteria_text=criteria_text,
        criteria_keys=criteria_keys,
        tone_guide=GRADE_TONE_GUIDE[gg],
    )
    return system, user


def analyze(student_text: str, format_type: str, grade: str, learning_type_id: str) -> dict:
    system, user = build_prompt(student_text, format_type, grade, learning_type_id)
    return ask(system, user, max_tokens=8192, json_mode=True)
