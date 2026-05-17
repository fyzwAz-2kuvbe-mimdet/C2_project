import streamlit as st
from config.learning_types import get_type, get_criteria
from core.feedback_engine import analyze
from utils.file_loader import load_text_from_file


def render_step4():
    if st.button("← 이전 단계"):
        st.session_state.current_step = 3
        st.rerun()

    type_info = get_type(st.session_state.learning_type)
    color = type_info.get("color", "#3b82f6")

    st.markdown('<div class="section-header">✏️ AI 첨삭 받기</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-subheader">{type_info["name"]} 평가기준으로 꼼꼼히 분석해드려요</div>',
        unsafe_allow_html=True,
    )

    with st.expander("📋 평가 기준 보기"):
        for c in get_criteria(st.session_state.learning_type):
            st.markdown(f"- **{c['label']}** (배점 {c['weight']}점)")

    st.markdown("---")
    st.markdown("**학습 결과물 제출**")

    tab_text, tab_file = st.tabs(["📝 직접 입력", "📎 파일 업로드"])

    text_from_input = ""
    text_from_file = ""

    with tab_text:
        text_from_input = st.text_area(
            "결과물 입력",
            value=st.session_state.get("student_text", ""),
            placeholder=(
                "여기에 학습한 내용, 에세이, 탐구 보고서 등을 붙여넣기 하세요.\n"
                "(100자 이상 입력 권장)"
            ),
            height=260,
            label_visibility="collapsed",
            key="student_text_input",
        )

    with tab_file:
        uploaded = st.file_uploader(
            "파일 업로드 (PDF, DOCX, TXT 지원)",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed",
        )
        if uploaded:
            try:
                text_from_file = load_text_from_file(uploaded)
                st.success(f"✅ 파일 로드 완료 ({len(text_from_file):,}자)")
                with st.expander("파일 내용 미리보기"):
                    preview = text_from_file[:1000]
                    if len(text_from_file) > 1000:
                        preview += "\n...(이하 생략)"
                    st.text(preview)
            except Exception as e:
                st.error(f"파일 파싱 오류: {e}")

    final_text = text_from_file or text_from_input
    st.session_state.student_text = final_text

    char_count = len(final_text)
    st.caption(
        f"입력된 글자 수: **{char_count:,}자** {'✅' if char_count >= 100 else '(100자 이상 입력 권장)'}"
    )

    st.markdown("")
    if st.button(
        "🤖 AI 첨삭 받기",
        type="primary",
        use_container_width=True,
        disabled=char_count < 50,
    ):
        _run_feedback(final_text)

    if char_count > 0 and char_count < 50:
        st.warning("50자 이상 입력해야 첨삭이 가능합니다.")

    feedback = st.session_state.get("feedback")
    if feedback:
        _render_feedback(feedback, color)


# ── helpers ──

def _run_feedback(text: str):
    with st.spinner("AI가 꼼꼼히 읽고 첨삭하고 있어요... (30초~1분 소요)"):
        try:
            feedback = analyze(text, st.session_state.learning_type, st.session_state.grade)
            st.session_state.feedback = feedback
            st.rerun()
        except Exception as e:
            st.error(f"첨삭 중 오류가 발생했습니다: {e}")


def _render_feedback(feedback: dict, color: str):
    st.markdown("---")
    st.markdown("## 🎯 첨삭 결과")

    # ── Overall score ──
    overall = int(feedback.get("overall_score", 0))
    pct = overall * 10
    st.markdown(
        f"""<div class="coach-card" style="text-align:center; border-left:4px solid {color};">
          <div style="font-size:52px; font-weight:800; color:{color}; line-height:1.1;">
            {overall}<span style="font-size:22px; color:#9ca3af;">/10</span>
          </div>
          <div style="font-size:14px; color:#6b7280; margin-top:4px;">종합 점수</div>
          <div class="score-bar-bg" style="margin-top:14px;">
            <div class="score-bar-fill" style="width:{pct}%; background:{color};"></div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Criteria scores ──
    criteria = get_criteria(st.session_state.learning_type)
    criteria_scores = feedback.get("criteria_scores", {})
    if criteria and criteria_scores:
        st.markdown("### 📊 평가 기준별 점수")
        for c in criteria:
            score = int(criteria_scores.get(c["key"], 0))
            bar_color = color if score >= 7 else ("#f59e0b" if score >= 5 else "#ef4444")
            st.markdown(
                f"""<div style="margin-bottom:14px;">
                  <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:13px; color:#374151; font-weight:500;">{c['label']}</span>
                    <span style="font-size:13px; font-weight:700; color:{bar_color};">{score}/10</span>
                  </div>
                  <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width:{score*10}%; background:{bar_color};"></div>
                  </div>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Strengths & Weaknesses ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ 강점")
        for s in feedback.get("strengths", []):
            st.markdown(
                f'<div style="background:#f0fdf4; border-left:3px solid #10b981; border-radius:0 8px 8px 0;'
                f'padding:10px 14px; margin-bottom:8px; font-size:13px; color:#065f46;">{s}</div>',
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("### 💡 개선 사항")
        for w in feedback.get("weaknesses", []):
            st.markdown(
                f'<div style="background:#fffbeb; border-left:3px solid #f59e0b; border-radius:0 8px 8px 0;'
                f'padding:10px 14px; margin-bottom:8px; font-size:13px; color:#92400e;">{w}</div>',
                unsafe_allow_html=True,
            )

    # ── Rewrite suggestions ──
    suggestions = feedback.get("rewrite_suggestions", [])
    if suggestions:
        st.markdown("### ✍️ 표현 개선 제안")
        for sug in suggestions:
            st.markdown(
                f"""<div class="coach-card">
                  <div style="font-size:11px; font-weight:700; color:#ef4444; margin-bottom:5px;">원문</div>
                  <div style="background:#fef2f2; border-radius:6px; padding:10px;
                              font-size:13px; color:#374151; margin-bottom:10px;">{sug.get('before','')}</div>
                  <div style="font-size:11px; font-weight:700; color:#10b981; margin-bottom:5px;">개선안</div>
                  <div style="background:#f0fdf4; border-radius:6px; padding:10px;
                              font-size:13px; color:#374151; margin-bottom:10px;">{sug.get('after','')}</div>
                  <div style="font-size:12px; color:#6b7280;"><strong>이유:</strong> {sug.get('reason','')}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Next step ──
    next_step = feedback.get("next_step", "")
    if next_step:
        st.markdown("### 🚀 다음 학습 방향")
        st.markdown(
            f'<div style="background:{color}11; border:1px solid {color}33; border-radius:12px;'
            f'padding:20px; font-size:14px; color:#374151; line-height:1.75;">{next_step}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    if st.button("🔄 다시 첨삭받기"):
        st.session_state.feedback = None
        st.rerun()
