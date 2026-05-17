from prompts.mentoring_prompts import STEP06_REFLECTION, get_system_prompt


def build_prompt(topic: str, what_i_studied: str, most_interesting: str, stuck_points: str, learning_type: str = "hana") -> tuple:
    user = STEP06_REFLECTION.format(
        topic=topic,
        what_i_studied=what_i_studied or "(없음)",
        most_interesting=most_interesting or "(없음)",
        stuck_points=stuck_points or "(없음)",
    )
    return get_system_prompt(learning_type), user
