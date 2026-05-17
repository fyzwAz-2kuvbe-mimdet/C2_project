import streamlit as st
from core.step08_writing_feedback import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s8_back"):
        st.session_state.current_step = 7
        st.rerun()

    st.markdown('<div class="section-header">글쓰기 첨삭</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">직접 쓴 글을 AI 코치에게 첨삭 받아보세요.</div>', unsafe_allow_html=True)

    topic = (st.session_state.get("selected_topic") or {}).get("name", "")
    if not topic:
        st.warning("선택된 주제가 없습니다. 처음 단계부터 시작해주세요.")
        return

    # 7단계 초록 참고용 표시
    abstract_data = st.session_state.get("s7_abstract") or {}
    full_text = abstract_data.get("full_text", "")
    if full_text:
        with st.expander("7단계 AI 초록 참고하기"):
            st.markdown(
                f'<div style="font-size:13px;color:#374151;line-height:1.8;'
                f'background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;padding:14px;">'
                f'{full_text}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("**나의 초고를 입력해주세요**")
    st.markdown(
        '<div style="font-size:12px;color:#4b7772;margin-bottom:8px;">'
        'AI 초록을 참고해서 직접 쓴 버전을 입력하세요. '
        '분량은 300~600자 정도가 좋습니다.</div>',
        unsafe_allow_html=True,
    )

    draft = st.text_area(
        "나의 초고",
        value=st.session_state.get("student_draft", ""),
        placeholder="직접 쓴 탐구 보고서 초록이나 에세이를 여기에 붙여 넣으세요...",
        height=280,
        label_visibility="collapsed",
    )
    if draft != st.session_state.get("student_draft", ""):
        st.session_state.student_draft = draft
        reset_result("s8_feedback")

    if not st.session_state.get("student_draft", "").strip():
        st.markdown(
            '<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
            'padding:12px;font-size:13px;color:#4b7772;margin-top:8px;">'
            '글을 입력하면 AI 첨삭을 시작할 수 있어요.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")
    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 첨삭", key="reset_s8", use_container_width=True):
            reset_result("s8_feedback")
            st.rerun()

    ai_abstract = full_text or "(없음)"
    system, prompt_text = build_prompt(
        topic,
        st.session_state.get("student_draft", ""),
        ai_abstract,
        learning_type=st.session_state.get("learning_type", "hana"),
    )
    if not prompt_panel(system, prompt_text, "s8_feedback",
                        spinner_text="AI가 글을 첨삭하고 있어요...",
                        btn_label="첨삭 시작"):
        return

    result = st.session_state.get("s8_feedback")
    if not result:
        return

    _render_feedback(result)

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True, key="s8_next"):
        st.session_state.current_step = 9
        st.rerun()


def _render_feedback(data: dict):
    overall = data.get("overall_impression", {})
    para_feedback = data.get("paragraph_feedback", [])
    patterns = data.get("recurring_patterns", [])
    top3 = data.get("top3_revisions", [])

    st.markdown("**AI 첨삭 결과**")

    # 전체 인상
    if overall:
        st.markdown(
            f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;padding:14px;margin-bottom:12px;">'
            f'<div style="font-size:13px;font-weight:700;color:#0a5c52;margin-bottom:8px;">전체 인상</div>'
            f'<div style="font-size:12px;color:#374151;margin-bottom:6px;">'
            f'<b style="color:#0d9488;">강점:</b> {overall.get("strongest_point", "")}</div>'
            f'<div style="font-size:12px;color:#374151;margin-bottom:6px;">'
            f'<b style="color:#d97706;">우선 개선:</b> {overall.get("first_priority", "")}</div>'
            f'<div style="font-size:12px;color:#374151;">'
            f'<b style="color:#0891b2;">흐름 평가:</b> {overall.get("flow_assessment", "")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # 최우선 수정 과제
    if top3:
        st.markdown("**최우선 수정 과제**")
        priority_colors = {1: "#0d9488", 2: "#0891b2", 3: "#059669"}
        for item in top3:
            p = item.get("priority", 1)
            task = item.get("task", "")
            why = item.get("why_first", "")
            color = priority_colors.get(p, "#0d9488")
            st.markdown(
                f'<div style="background:#f0faf8;border-left:4px solid {color};'
                f'border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;">'
                f'<div style="font-size:13px;font-weight:700;color:{color};margin-bottom:4px;">'
                f'{p}순위: {task}</div>'
                f'<div style="font-size:12px;color:#4b7772;">{why}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # 단락별 첨삭
    if para_feedback:
        st.markdown("**단락별 첨삭**")
        for item in para_feedback:
            para = item.get("paragraph", "")
            current = item.get("current_state", "")
            diag = item.get("diagnosis", "")
            direction = item.get("direction", "")
            guide_q = item.get("guiding_question", "")
            with st.expander(f"단락: {para}"):
                st.markdown(
                    f'<div style="font-size:12px;color:#374151;">'
                    f'<div style="margin-bottom:6px;"><b style="color:#0d9488;">현재 상태:</b> {current}</div>'
                    f'<div style="margin-bottom:6px;"><b style="color:#d97706;">문제 진단:</b> {diag}</div>'
                    f'<div style="margin-bottom:6px;"><b style="color:#059669;">개선 방향:</b> {direction}</div>'
                    f'<div style="background:#e8f5f3;border-radius:6px;padding:8px;font-weight:600;color:#0a5c52;">'
                    f'질문: {guide_q}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # 반복 패턴
    if patterns:
        st.markdown("**반복 패턴 진단**")
        for pat in patterns:
            pattern = pat.get("pattern", "")
            why = pat.get("why_it_matters", "")
            rep = pat.get("representative_sentence", "")
            st.markdown(
                f'<div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;'
                f'padding:10px 14px;margin-bottom:8px;font-size:12px;">'
                f'<div style="font-weight:700;color:#92400e;margin-bottom:4px;">{pattern}</div>'
                f'<div style="color:#374151;margin-bottom:4px;">{why}</div>'
                f'<div style="color:#4b7772;font-style:italic;">대표 문장: "{rep}"</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
