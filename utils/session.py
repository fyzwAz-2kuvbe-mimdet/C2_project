import streamlit as st

_DEFAULTS = {
    "current_step": 1,
    "grade": "고1",
    "learning_type": "hana",
    # step 1: keyword analysis
    "keyword": "",
    "s1_result": None,
    "student_context": "",
    # step 2: topic selection
    "s2_topics": None,
    "selected_topic": None,
    # step 3: roadmap
    "curiosity": "",
    "current_level": "",
    "s3_roadmap": None,
    # step 4: resources
    "s4_resources": None,
    # step 5: trends
    "s5_trends": None,
    # step 6: reflection
    "s6_what_i_studied": "",
    "s6_most_interesting": "",
    "s6_stuck_points": "",
    "s6_reflection": None,
    # step 7: abstract
    "s7_study_notes": "",
    "s7_motivation": "",
    "s7_key_findings": "",
    "s7_limits_and_next": "",
    "s7_abstract": None,
    # step 8: writing feedback
    "student_draft": "",
    "s8_feedback": None,
    # step 9: knowledge map (3 rounds)
    "s9_study_summary": "",
    "s9_most_interesting": "",
    "s9_stuck_points": "",
    "s9_r1": None,
    "s9_r2": None,
    "s9_r3": None,
    "s9_student_r1": "",
    "s9_student_r2": "",
    "selected_seed": "",
    # step 10: curriculum
    "s10_key_findings": "",
    "s10_my_idea": "",
    "s10_current_subjects": "",
    "s10_result": None,
}


def init_session():
    for key, val in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_all():
    for key, val in _DEFAULTS.items():
        st.session_state[key] = val
    # also clear ai_runner done-flags for all result keys
    for rk in ["s1_result", "s2_topics", "s3_roadmap", "s4_resources", "s5_trends",
               "s6_reflection", "s7_abstract", "s8_feedback",
               "s9_r1", "s9_r2", "s9_r3", "s10_result"]:
        st.session_state[f"_done_{rk}"] = False
