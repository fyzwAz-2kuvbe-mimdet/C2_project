from prompts.mentoring_prompts import STEP10_CURRICULUM, get_system_prompt


def build_prompt(topic: str, key_findings: str, my_idea: str,
                 selected_seed: str, current_subjects: str, learning_type: str = "hana") -> tuple:
    user = STEP10_CURRICULUM.format(
        topic=topic,
        key_findings=key_findings or "(없음)",
        my_idea=my_idea or "(없음)",
        selected_seed=selected_seed or "(없음)",
        current_subjects=current_subjects or "(없음)",
    )
    return get_system_prompt(learning_type), user
