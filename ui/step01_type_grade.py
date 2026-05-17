import streamlit as st
from core.step01_keyword import build_prompt
from utils.ai_runner import prompt_panel, reset_result, is_done


def render():
    st.markdown('<div class="section-header">관심사 구체화</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">탐구하고 싶은 키워드를 자유롭게 입력하세요.</div>', unsafe_allow_html=True)

    keyword = st.text_input(
        "관심 키워드",
        value=st.session_state.get("keyword", ""),
        placeholder="예: AI, 기후변화, 최저임금, 블랙홀...",
        label_visibility="collapsed",
    )

    # 키워드 바뀌면 분석 초기화
    if keyword.strip() != st.session_state.get("keyword", ""):
        st.session_state.keyword = keyword.strip()
        reset_result("s1_result")
        st.session_state.student_context = ""
        st.rerun()

    if not keyword.strip():
        st.markdown(
            '<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
            'padding:14px 18px;font-size:13px;color:#4b7772;margin-top:8px;">'
            '키워드를 입력하면 AI가 구체성을 분석하고 탐구 방향을 찾아드려요.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")

    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 분석", key="reset_s1", use_container_width=True):
            reset_result("s1_result")
            st.session_state.student_context = ""
            st.rerun()

    system, prompt_text = build_prompt(keyword.strip(), learning_type=st.session_state.get("learning_type", "hana"))
    if not prompt_panel(system, prompt_text, "s1_result",
                        spinner_text="AI가 키워드를 분석하고 있어요...",
                        btn_label="AI 분석 시작"):
        return

    result = st.session_state.get("s1_result")
    if not result:
        return

    _render_result(result)


def _render_result(result: dict):
    level = result.get("specificity_level", "")
    reason = result.get("reason", "")
    question = result.get("clarifying_question")

    level_cfg = {
        "broad":    ("#fee2e2", "#991b1b", "모호함"),
        "medium":   ("#fef3c7", "#92400e", "중간"),
        "specific": ("#d1fae5", "#065f46", "구체적"),
    }
    bg, text, label = level_cfg.get(level, ("#f0faf8", "#0d9488", level))

    st.markdown("**AI 분석 결과**")
    st.markdown(
        f'<div style="display:flex;gap:10px;align-items:center;margin-bottom:10px;">'
        f'<div style="background:{bg};color:{text};border-radius:8px;padding:6px 14px;'
        f'font-size:13px;font-weight:700;">{label}</div>'
        f'<div style="font-size:13px;color:#374151;">{reason}</div></div>',
        unsafe_allow_html=True,
    )

    if level in ("broad", "medium") and question:
        st.markdown(
            f'<div style="background:#f0faf8;border-left:4px solid #0d9488;border-radius:0 8px 8px 0;'
            f'padding:14px 16px;font-size:14px;color:#0a5c52;font-weight:600;margin:12px 0;">'
            f'{question}</div>',
            unsafe_allow_html=True,
        )

        context = st.text_area(
            "내 생각",
            value=st.session_state.get("student_context", ""),
            placeholder="떠오른 장면, 경험, 구체적인 상황을 자유롭게 적어주세요.",
            height=100,
            label_visibility="collapsed",
        )
        if context.strip() != st.session_state.get("student_context", ""):
            st.session_state.student_context = context.strip()

        if not st.session_state.get("student_context", "").strip():
            st.markdown(
                '<div style="font-size:12px;color:#4b7772;margin-top:4px;">'
                '위 질문에 답을 적으면 더 정확한 주제 추천을 받을 수 있어요.</div>',
                unsafe_allow_html=True,
            )
            return

    else:
        st.session_state.student_context = ""

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True, key="s1_next"):
        st.session_state.current_step = 2
        st.rerun()
