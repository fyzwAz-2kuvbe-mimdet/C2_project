import streamlit as st
from core.interest_diagnosis import diagnose
from utils.session import reset_from_step

_PLACEHOLDERS = {
    "초": "예: 로봇이 어떻게 움직이는지 궁금해요, 공룡이 왜 멸종했는지 알고 싶어요...",
    "중": "예: 인공지능의 원리, 환경 문제와 경제 성장의 관계, 한국 역사 속 외교...",
    "고": "예: 양자컴퓨팅의 큐비트 원리, 빅데이터와 개인정보 윤리, 행동경제학...",
}


def render_step1():
    st.markdown('<div class="section-header">💡 관심 주제 탐구</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subheader">어떤 주제가 궁금한가요? 키워드 하나만 입력해도 됩니다.</div>',
        unsafe_allow_html=True,
    )

    grade = st.session_state.get("grade", "고1")
    placeholder = _PLACEHOLDERS.get(grade[:1], _PLACEHOLDERS["고"])

    interest = st.text_area(
        "관심 주제",
        value=st.session_state.get("interest_text", ""),
        placeholder=placeholder,
        height=110,
        label_visibility="collapsed",
        key="interest_input",
    )

    col1, col2 = st.columns([4, 1])
    with col1:
        gen_disabled = not interest.strip()
        if st.button(
            "🔍 후속 질문 생성",
            type="primary",
            use_container_width=True,
            disabled=gen_disabled,
        ):
            _generate_questions(interest.strip())
    with col2:
        if st.button("초기화", use_container_width=True):
            reset_from_step(1)
            st.rerun()

    if st.session_state.get("follow_up_questions"):
        _render_questions_form()


# ── helpers ──

def _generate_questions(interest_text: str):
    with st.spinner("AI가 탐구 질문을 생성하고 있어요..."):
        try:
            result = diagnose(
                interest_text,
                st.session_state.grade,
                st.session_state.learning_type,
            )
            st.session_state.interest_text = interest_text
            st.session_state.follow_up_questions = result.get("follow_up_questions", [])
            st.session_state.diagnosis = result
            st.session_state.user_answers = {}
            st.session_state.step1_complete = False
            reset_from_step(2)
            st.rerun()
        except Exception as e:
            st.error(f"질문 생성 중 오류가 발생했습니다: {e}")


def _render_questions_form():
    diagnosis = st.session_state.get("diagnosis", {})
    st.markdown("---")

    # Diagnosis badges
    subtopic = diagnosis.get("estimated_subtopic", "")
    depth = diagnosis.get("depth_level", "")
    if subtopic:
        _depth_colors = {
            "초급": ("#d1fae5", "#065f46"),
            "중급": ("#fef3c7", "#92400e"),
            "고급": ("#ede9fe", "#5b21b6"),
        }
        bg, text = _depth_colors.get(depth, ("#f3f4f6", "#374151"))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""<div style="background:#eff6ff; border-radius:8px; padding:12px 16px;">
                  <div style="font-size:11px; color:#3b82f6; font-weight:700; margin-bottom:3px;">추정 세부 주제</div>
                  <div style="font-size:15px; color:#1e40af; font-weight:700;">{subtopic}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""<div style="background:{bg}; border-radius:8px; padding:12px 16px;">
                  <div style="font-size:11px; color:{text}; font-weight:700; margin-bottom:3px;">학습 깊이</div>
                  <div style="font-size:15px; color:{text}; font-weight:700;">{depth}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        st.markdown("")

    st.markdown("**AI의 후속 질문에 답해주세요**")

    questions = st.session_state.follow_up_questions
    answers = {}

    for i, question in enumerate(questions):
        st.markdown(
            f"""<div style="background:#f8fafc; border-left:3px solid #3b82f6;
                            border-radius:0 8px 8px 0; padding:12px 16px; margin-bottom:6px;">
              <span style="font-size:12px; font-weight:700; color:#3b82f6;">Q{i+1}</span>
              <div style="font-size:14px; color:#111827; margin-top:2px; line-height:1.5;">{question}</div>
            </div>""",
            unsafe_allow_html=True,
        )

        saved = st.session_state.user_answers.get(str(i), "")
        answer = st.text_area(
            f"답변 {i+1}",
            value=saved,
            placeholder="여기에 답변을 입력하세요...",
            height=80,
            label_visibility="collapsed",
            key=f"answer_{i}",
        )
        answers[str(i)] = answer
        st.markdown("")

    any_answered = any(a.strip() for a in answers.values())

    if st.button(
        "📚 학습 자료 보기 →",
        type="primary",
        use_container_width=True,
        disabled=not any_answered,
    ):
        st.session_state.user_answers = answers
        st.session_state.step1_complete = True
        st.session_state.current_step = 2
        st.rerun()

    if not any_answered:
        st.caption("💬 하나 이상 답하면 다음 단계로 진행할 수 있어요.")
