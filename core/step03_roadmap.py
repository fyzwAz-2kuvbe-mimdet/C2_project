from prompts.mentoring_prompts import STEP03_ROADMAP, get_system_prompt


def build_prompt(topic: str, curiosity: str, current_level: str, learning_type: str = "hana") -> tuple:
    user = STEP03_ROADMAP.format(
        topic=topic,
        curiosity=curiosity or "(없음)",
        current_level=current_level or "(없음)",
    )
    return get_system_prompt(learning_type), user
