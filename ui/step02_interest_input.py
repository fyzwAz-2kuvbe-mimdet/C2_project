import streamlit as st
from core.step02_topics import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s2_back"):
        st.session_state.current_step = 1
        st.rerun()

    st.markdown('<div class="section-header">탐구 주제 추천</div>', unsafe_allow_html=True)

    keyword = st.session_state.get("keyword", "")
    student_context = st.session_state.get("student_context", "")

    st.markdown(
        f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
        f'padding:10px 14px;font-size:13px;color:#374151;margin-bottom:12px;">'
        f'<span style="color:#0d9488;font-weight:700;">키워드:</span> {keyword}'
        f'{"  |  " + student_context if student_context else ""}</div>',
        unsafe_allow_html=True,
    )

    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 추천", key="reset_s2", use_container_width=True):
            reset_result("s2_topics")
            st.session_state.selected_topic = None
            st.rerun()

    system, prompt_text = build_prompt(keyword, student_context, learning_type=st.session_state.get("learning_type", "hana"))
    if not prompt_panel(system, prompt_text, "s2_topics",
                        spinner_text="AI가 탐구 주제를 추천하고 있어요...",
                        btn_label="주제 추천 받기"):
        return

    topics_data = st.session_state.get("s2_topics") or {}
    topics = topics_data.get("topics", [])
    if not topics:
        st.warning("추천 주제를 불러오지 못했습니다. 다시 시도해주세요.")
        return

    st.markdown("**추천 주제 목록** — 클릭해서 탐구할 주제를 선택하세요")

    selected = st.session_state.get("selected_topic")
    sel_name = (selected or {}).get("name", "")

    for i, topic in enumerate(topics):
        name = topic.get("name", "")
        hook = topic.get("hook", "")
        insight = topic.get("insight", "")
        real_use = topic.get("real_use", "")
        is_sel = name == sel_name

        # CSS marker for button targeting
        st.markdown(
            f"<style>"
            f".element-container:has(#tm-topic-{i}) + .element-container button{{"
            f"  border-left:5px solid #0d9488 !important;"
            f"  border-radius:0 10px 10px 0 !important;"
            f"  white-space:pre-line !important;"
            f"  text-align:left !important;"
            f"  height:auto !important;"
            f"  min-height:100px !important;"
            f"  padding:14px 18px !important;"
            f"  line-height:1.6 !important;"
            f"  font-size:13px !important;"
            f"  font-weight:400 !important;"
            f"  display:block !important;"
            f"}}"
            f".element-container:has(#tm-topic-{i}) + .element-container button p{{"
            f"  text-align:left !important;"
            f"  width:100% !important;"
            f"  margin:0 !important;"
            f"}}"
            f"</style>"
            f'<span id="tm-topic-{i}"></span>',
            unsafe_allow_html=True,
        )
        label = f"{name}\n{hook}\n{insight}"
        if real_use:
            label += f"\n실생활: {real_use}"

        if st.button(label, key=f"topic_btn_{i}", use_container_width=True,
                     type="primary" if is_sel else "secondary"):
            st.session_state.selected_topic = topic
            # reset downstream
            reset_result("s3_roadmap")
            reset_result("s4_resources")
            reset_result("s5_trends")
            reset_result("s6_reflection")
            reset_result("s7_abstract")
            reset_result("s8_feedback")
            reset_result("s9_r1")
            reset_result("s9_r2")
            reset_result("s9_r3")
            reset_result("s10_result")
            st.rerun()

        st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)

    if not sel_name:
        st.markdown(
            '<div style="font-size:12px;color:#4b7772;margin-top:8px;">'
            '주제를 선택하면 다음 단계로 진행할 수 있어요.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f'<div style="background:#e8f5f3;border:1px solid #0d9488;border-radius:10px;'
        f'padding:10px 14px;font-size:13px;color:#0a5c52;font-weight:700;margin:8px 0;">'
        f'선택된 주제: {sel_name}</div>',
        unsafe_allow_html=True,
    )

    if st.button("다음 단계", type="primary", use_container_width=True, key="s2_next"):
        st.session_state.current_step = 3
        st.rerun()
