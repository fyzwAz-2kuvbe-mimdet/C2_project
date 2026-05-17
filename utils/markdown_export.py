import streamlit as st
from config.learning_types import get_type


def build_markdown() -> str:
    grade = st.session_state.get("grade", "")
    lt_id = st.session_state.get("learning_type", "hana")
    lt_info = get_type(lt_id)
    lt_name = lt_info.get("name", "")
    lt_core = lt_info.get("core", "")

    lines = [
        "# AI 학습 멘토 — 탐구 기록",
        "",
        f"**학년:** {grade}  |  **학습 유형:** {lt_info.get('icon','')} {lt_name} ({lt_core})",
        "",
        "---",
        "",
    ]

    # Step 2
    interest = st.session_state.get("interest_text", "")
    if interest:
        lines += ["## 관심 주제", "", interest, ""]
        analysis = st.session_state.get("initial_analysis") or {}
        if analysis.get("estimated_subtopic"):
            lines += [
                f"- **추정 세부 주제:** {analysis['estimated_subtopic']}",
                f"- **학습 깊이:** {analysis.get('depth_level','')}",
                "",
            ]

    # Step 3
    questions = st.session_state.get("follow_up_questions") or []
    answers = st.session_state.get("user_answers") or {}
    if questions and answers:
        lines += ["## 탐구 방향 질문 & 답변", ""]
        for i, q in enumerate(questions):
            a = answers.get(str(i), "").strip()
            if a:
                lines += [f"**Q{i+1}. {q}**", f"A: {a}", ""]

    refined = st.session_state.get("refined_topic") or {}
    if refined.get("refined_topic"):
        lines += [
            "## 확정 탐구 주제",
            "",
            f"**{refined['refined_topic']}**",
            "",
        ]
        if refined.get("specific_angle"):
            lines.append(f"- 탐구 각도: {refined['specific_angle']}")
        if refined.get("learning_goal"):
            lines.append(f"- 학습 목표: {refined['learning_goal']}")
        if refined.get("key_concepts"):
            lines.append(f"- 핵심 개념: {', '.join(refined['key_concepts'])}")
        lines.append("")

    # Step 4
    roadmap = st.session_state.get("roadmap") or []
    if roadmap:
        lines += ["## 학습 로드맵", ""]
        for i, step in enumerate(roadmap):
            title = step.get("step_title", f"단계 {i+1}")
            goal = step.get("goal", "")
            duration = step.get("duration", "")
            lines.append(f"### {i+1}단계: {title}")
            if goal:
                lines.append(f"{goal}")
            if duration:
                lines.append(f"*예상 기간: {duration}*")
            for act in step.get("activities", []):
                lines.append(f"- {act}")
            lines.append("")

    # Step 5 (brief)
    resources = st.session_state.get("resources") or {}
    per_step = resources.get("per_step", {})
    general = resources.get("general", [])
    if per_step or general:
        lines += ["## 추천 학습 자료", ""]
        for key, items in per_step.items():
            if items:
                lines.append(f"**{key}단계 자료**")
                for r in items:
                    lines.append(f"- [{r.get('type','')}] {r.get('title','')} — {r.get('description','')}")
                lines.append("")
        if general:
            lines.append("**공통 자료**")
            for r in general:
                lines.append(f"- [{r.get('type','')}] {r.get('title','')} — {r.get('description','')}")
            lines.append("")

    # Step 6
    news = st.session_state.get("news_items") or []
    summaries = st.session_state.get("news_summaries") or {}
    if news:
        lines += ["## 관련 뉴스", ""]
        for i, item in enumerate(news):
            headline = item.get("headline", "")
            link = item.get("link", "")
            press = item.get("press", "")
            date = item.get("date", "")
            meta = "  ·  ".join(filter(None, [press, date]))
            lines.append(f"- [{headline}]({link})" + (f" — {meta}" if meta else ""))
            if str(i) in summaries:
                lines.append(f"  > {summaries[str(i)]}")
        lines.append("")

    # Step 7
    core_qs = st.session_state.get("core_questions") or []
    q_answers = st.session_state.get("question_answers") or {}
    if core_qs:
        lines += ["## 핵심 탐구 질문 & 답변", ""]
        for i, q in enumerate(core_qs):
            a = q_answers.get(str(i), "").strip()
            lines += [f"**Q{i+1}. {q}**", f"A: {a}" if a else "A: (미작성)", ""]

    # Step 8
    student_text = st.session_state.get("student_text", "").strip()
    fmt = st.session_state.get("format_type", "에세이")
    if student_text:
        lines += [f"## 제출 결과물 ({fmt})", "", student_text, ""]

    # Step 9
    feedback = st.session_state.get("feedback") or {}
    if feedback:
        lines += ["## AI 첨삭 결과", ""]
        lines.append(f"**종합 점수:** {feedback.get('overall_score', 0)}/100")
        if feedback.get("overall_comment"):
            lines.append(f"\n{feedback['overall_comment']}")
        lines.append("")
        if feedback.get("strengths"):
            lines += ["**강점**", ""]
            for s in feedback["strengths"]:
                lines.append(f"- {s}")
            lines.append("")
        if feedback.get("weaknesses"):
            lines += ["**개선 사항**", ""]
            for w in feedback["weaknesses"]:
                lines.append(f"- {w}")
            lines.append("")
        if feedback.get("before_after"):
            lines += ["**Before → After**", ""]
            for ba in feedback["before_after"]:
                lines += [
                    f"**Before:** {ba.get('before','')}",
                    f"**After:** {ba.get('after','')}",
                    f"*{ba.get('reason','')}*",
                    "",
                ]

    # Step 10
    nr = st.session_state.get("next_step_result") or {}
    if nr.get("next_topic"):
        lines += ["## 다음 탐구 방향", "", f"**{nr['next_topic']}**"]
        if nr.get("reason"):
            lines.append(f"\n{nr['reason']}")
        lines.append("")
        if nr.get("expansion_topics"):
            lines.append(f"**확장 주제:** {', '.join(nr['expansion_topics'])}")
        if nr.get("suggested_activities"):
            lines += ["**추천 활동**", ""]
            for act in nr["suggested_activities"]:
                lines.append(f"- {act}")
        lines.append("")

    reflection = st.session_state.get("reflection_text", "").strip()
    if reflection:
        lines += ["## 자기 성찰 노트", "", reflection, ""]

    lines += ["---", "", "*Generated by AI 학습 멘토 (Powered by Google Gemini)*"]
    return "\n".join(lines)
