from prompts.mentoring_prompts import STEP05_TRENDS, get_system_prompt


def build_prompt(topic: str, current_level: str, learning_type: str = "hana") -> tuple:
    user = STEP05_TRENDS.format(
        topic=topic,
        current_level=current_level or "(없음)",
    )
    return get_system_prompt(learning_type), user
