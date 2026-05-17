import streamlit as st
from core.step07_abstract import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s7_back"):
        st.session_state.current_step = 6
        st.rerun()

    st.markdown('<div class="section-header">AI 초록 생성</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">탐구 내용을 바탕으로 학술 초록 초안을 만들어드려요.</div>', unsafe_allow_html=True)

    topic = (st.session_state.get("selected_topic") or {}).get("name", "")
    if not topic:
        st.warning("선택된 주제가 없습니다. 처음 단계부터 시작해주세요.")
        return

    st.markdown(
        f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
        f'padding:10px 14px;font-size:13px;color:#374151;margin-bottom:14px;">'
        f'<span style="color:#0d9488;font-weight:700;">탐구 주제:</span> {topic}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("**초록 작성을 위한 정보를 입력해주세요**")

    motivation = st.text_area(
        "탐구 동기",
        value=st.session_state.get("s7_motivation", ""),
        placeholder="이 주제를 탐구하게 된 출발점이 무엇인가요? 일상 관찰, 수업 경험 등...",
        height=80,
        label_visibility="visible",
    )
    if motivation != st.session_state.get("s7_motivation", ""):
        st.session_state.s7_motivation = motivation
        reset_result("s7_abstract")

    key_findings = st.text_area(
        "핵심 발견",
        value=st.session_state.get("s7_key_findings", ""),
        placeholder="탐구를 통해 알게 된 가장 중요한 것 2~3가지를 적어주세요.",
        height=100,
        label_visibility="visible",
    )
    if key_findings != st.session_state.get("s7_key_findings", ""):
        st.session_state.s7_key_findings = key_findings
        reset_result("s7_abstract")

    limits_and_next = st.text_area(
        "한계 및 후속 질문",
        value=st.session_state.get("s7_limits_and_next", ""),
        placeholder="이번 탐구에서 도달하지 못한 부분과 다음에 탐구하고 싶은 질문을 적어주세요.",
        height=80,
        label_visibility="visible",
    )
    if limits_and_next != st.session_state.get("s7_limits_and_next", ""):
        st.session_state.s7_limits_and_next = limits_and_next
        reset_result("s7_abstract")

    study_notes = st.text_area(
        "공부한 내용 (선택 사항)",
        value=st.session_state.get("s7_study_notes", ""),
        placeholder="공부한 내용을 추가로 적어주세요. 6단계에서 입력한 내용을 그대로 붙여 넣어도 됩니다.",
        height=100,
        label_visibility="visible",
    )
    if study_notes != st.session_state.get("s7_study_notes", ""):
        st.session_state.s7_study_notes = study_notes
        reset_result("s7_abstract")

    if not st.session_state.get("s7_motivation", "").strip() or \
       not st.session_state.get("s7_key_findings", "").strip():
        st.markdown(
            '<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
            'padding:12px;font-size:13px;color:#4b7772;margin-top:8px;">'
            '탐구 동기와 핵심 발견을 입력하면 AI가 초록을 생성해요.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")
    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 생성", key="reset_s7", use_container_width=True):
            reset_result("s7_abstract")
            st.rerun()

    system, prompt_text = build_prompt(
        topic,
        st.session_state.get("s7_study_notes", ""),
        st.session_state.get("s7_motivation", ""),
        st.session_state.get("s7_key_findings", ""),
        st.session_state.get("s7_limits_and_next", ""),
        learning_type=st.session_state.get("learning_type", "hana"),
    )
    if not prompt_panel(system, prompt_text, "s7_abstract",
                        spinner_text="AI가 초록을 작성하고 있어요...",
                        btn_label="초록 생성"):
        return

    result = st.session_state.get("s7_abstract")
    if not result:
        return

    _render_abstract(result)

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True, key="s7_next"):
        st.session_state.current_step = 8
        st.rerun()


def _render_abstract(data: dict):
    abstract = data.get("abstract", {})
    full_text = data.get("full_text", "")
    check_points = data.get("check_points", [])

    st.markdown("**AI 초록 초안**")

    para_labels = [
        ("motivation", "탐구 동기", "#0d9488"),
        ("method", "탐구 내용 및 방법", "#0891b2"),
        ("findings", "핵심 발견", "#059669"),
        ("limits", "한계 인식", "#d97706"),
        ("next_direction", "후속 탐구 방향", "#7c3aed"),
    ]

    for key, label, color in para_labels:
        text = abstract.get(key, "")
        if text:
            st.markdown(
                f'<div style="background:#f0faf8;border-left:4px solid {color};'
                f'border-radius:0 8px 8px 0;padding:12px 14px;margin-bottom:8px;">'
                f'<div style="font-size:11px;font-weight:700;color:{color};margin-bottom:4px;">{label}</div>'
                f'<div style="font-size:13px;color:#374151;">{text}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if full_text:
        with st.expander("완성 초록 전문 보기"):
            st.markdown(
                f'<div style="font-size:14px;color:#374151;line-height:1.8;'
                f'background:#fff;border:1px solid #c9e6e1;border-radius:10px;padding:16px;">'
                f'{full_text}</div>',
                unsafe_allow_html=True,
            )

    if check_points:
        st.markdown("**학생 확인 사항**")
        for i, cp in enumerate(check_points, 1):
            st.markdown(
                f'<div style="background:#e8f5f3;border-radius:8px;padding:8px 14px;'
                f'font-size:12px;color:#0a5c52;margin-bottom:6px;">'
                f'{i}. {cp}</div>',
                unsafe_allow_html=True,
            )
