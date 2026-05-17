from prompts.mentoring_prompts import STEP08_FEEDBACK, get_system_prompt


def build_prompt(topic: str, student_draft: str, ai_abstract: str, learning_type: str = "hana") -> tuple:
    user = STEP08_FEEDBACK.format(
        topic=topic,
        student_draft=student_draft or "(없음)",
        ai_abstract=ai_abstract or "(없음)",
    )
    return get_system_prompt(learning_type), user
