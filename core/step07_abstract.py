from prompts.mentoring_prompts import STEP07_ABSTRACT, get_system_prompt


def build_prompt(topic: str, study_notes: str, motivation: str, key_findings: str, limits_and_next: str, learning_type: str = "hana") -> tuple:
    user = STEP07_ABSTRACT.format(
        topic=topic,
        study_notes=study_notes or "(없음)",
        motivation=motivation or "(없음)",
        key_findings=key_findings or "(없음)",
        limits_and_next=limits_and_next or "(없음)",
    )
    return get_system_prompt(learning_type), user
