import json
from prompts.mentoring_prompts import STEP09_R1, STEP09_R2, STEP09_R3, get_system_prompt


def build_r1_prompt(topic: str, study_summary: str, most_interesting: str,
                    stuck_points: str, final_abstract: str, learning_type: str = "hana") -> tuple:
    user = STEP09_R1.format(
        topic=topic,
        study_summary=study_summary or "(없음)",
        most_interesting=most_interesting or "(없음)",
        stuck_points=stuck_points or "(없음)",
        final_abstract=final_abstract or "(없음)",
    )
    return get_system_prompt(learning_type), user


def build_r2_prompt(topic: str, study_summary: str, most_interesting: str,
                    stuck_points: str, final_abstract: str,
                    r1_result: dict, student_r1: str, learning_type: str = "hana") -> tuple:
    r1_text = json.dumps(r1_result, ensure_ascii=False, indent=2)
    user = STEP09_R2.format(
        topic=topic,
        study_summary=study_summary or "(없음)",
        most_interesting=most_interesting or "(없음)",
        stuck_points=stuck_points or "(없음)",
        final_abstract=final_abstract or "(없음)",
        r1_result=r1_text,
        student_r1=student_r1 or "(없음)",
    )
    return get_system_prompt(learning_type), user


def build_r3_prompt(topic: str, study_summary: str, most_interesting: str,
                    stuck_points: str, final_abstract: str,
                    r1_result: dict, student_r1: str,
                    r2_result: dict, student_r2: str, learning_type: str = "hana") -> tuple:
    r1_text = json.dumps(r1_result, ensure_ascii=False, indent=2)
    r2_text = json.dumps(r2_result, ensure_ascii=False, indent=2)
    user = STEP09_R3.format(
        topic=topic,
        study_summary=study_summary or "(없음)",
        most_interesting=most_interesting or "(없음)",
        stuck_points=stuck_points or "(없음)",
        final_abstract=final_abstract or "(없음)",
        r1_result=r1_text,
        student_r1=student_r1 or "(없음)",
        r2_result=r2_text,
        student_r2=student_r2 or "(없음)",
    )
    return get_system_prompt(learning_type), user
