from config.learning_types import get_type
from core.llm_client import ask
from prompts.mentoring_prompts import (
    GRADE_TONE_GUIDE, STEP03_FOLLOW_UP_QUESTIONS, STEP03_REFINE_TOPIC,
    SYSTEM_BASE, TYPE_QUESTION_STYLE,
)


def _grade_group(grade: str) -> str:
    return "초등" if grade.startswith("초") else ("중등" if grade.startswith("중") else "고등")


def _system(grade: str, learning_type_id: str) -> str:
    info = get_type(learning_type_id)
    return SYSTEM_BASE.format(
        type_name=info["name"],
        type_core=info["core"],
        grade=grade,
        tone_guide=GRADE_TONE_GUIDE[_grade_group(grade)],
        question_style=TYPE_QUESTION_STYLE[learning_type_id],
    )


def build_questions_prompt(
    interest: str, estimated_subtopic: str, grade: str, learning_type_id: str
) -> tuple:
    info = get_type(learning_type_id)
    user = STEP03_FOLLOW_UP_QUESTIONS.format(
        interest=interest,
        estimated_subtopic=estimated_subtopic,
        grade=grade,
        type_name=info["name"],
        question_style=TYPE_QUESTION_STYLE[learning_type_id],
    )
    return _system(grade, learning_type_id), user


def generate_questions(
    interest: str, estimated_subtopic: str, grade: str, learning_type_id: str
) -> list:
    system, user = build_questions_prompt(interest, estimated_subtopic, grade, learning_type_id)
    result = ask(system, user, json_mode=True)
    questions = result.get("questions", [])
    if len(questions) < 3:
        questions += ["이 주제에서 특히 어떤 부분이 가장 궁금한가요?"] * (3 - len(questions))
    return questions[:5]


def build_refine_prompt(
    interest: str, questions: list, answers: dict, grade: str, learning_type_id: str
) -> tuple:
    info = get_type(learning_type_id)
    qa_pairs = "\n".join(
        f"Q: {q}\nA: {answers.get(str(i), '(미답변)')}"
        for i, q in enumerate(questions)
    )
    user = STEP03_REFINE_TOPIC.format(
        interest=interest,
        qa_pairs=qa_pairs,
        grade=grade,
        type_name=info["name"],
        type_core=info["core"],
    )
    return _system(grade, learning_type_id), user


def refine_topic(
    interest: str, questions: list, answers: dict, grade: str, learning_type_id: str,
) -> dict:
    system, user = build_refine_prompt(interest, questions, answers, grade, learning_type_id)
    return ask(system, user, json_mode=True)
