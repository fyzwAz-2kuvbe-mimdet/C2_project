from prompts.mentoring_prompts import STEP02_TOPICS, get_system_prompt


def build_prompt(refined_keyword: str, student_context: str, learning_type: str = "hana") -> tuple:
    user = STEP02_TOPICS.format(
        refined_keyword=refined_keyword,
        student_context=student_context or "(없음)",
    )
    return get_system_prompt(learning_type), user
