import streamlit as st
from core.step03_roadmap import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s3_back"):
        st.session_state.current_step = 2
        st.rerun()

    st.markdown('<div class="section-header">학습 로드맵 설계</div>', unsafe_allow_html=True)

    topic = (st.session_state.get("selected_topic") or {}).get("name", "")
    if not topic:
        st.warning("선택된 주제가 없습니다. 이전 단계로 돌아가 주제를 선택해주세요.")
        return

    st.markdown(
        f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
        f'padding:10px 14px;font-size:13px;color:#374151;margin-bottom:14px;">'
        f'<span style="color:#0d9488;font-weight:700;">탐구 주제:</span> {topic}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-subheader">탐구 출발점과 현재 수준을 알려주세요.</div>', unsafe_allow_html=True)

    curiosity = st.text_area(
        "출발 호기심",
        value=st.session_state.get("curiosity", ""),
        placeholder="이 주제에서 가장 궁금한 점이 무엇인가요? (선택 사항)",
        height=80,
        label_visibility="visible",
    )
    if curiosity != st.session_state.get("curiosity", ""):
        st.session_state.curiosity = curiosity
        reset_result("s3_roadmap")

    current_level = st.text_area(
        "현재 수준",
        value=st.session_state.get("current_level", ""),
        placeholder="이 주제에 대해 현재 알고 있는 것을 간단히 적어주세요. (선택 사항)",
        height=80,
        label_visibility="visible",
    )
    if current_level != st.session_state.get("current_level", ""):
        st.session_state.current_level = current_level
        reset_result("s3_roadmap")

    st.markdown("---")

    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 생성", key="reset_s3", use_container_width=True):
            reset_result("s3_roadmap")
            st.rerun()

    system, prompt_text = build_prompt(topic,
                                       st.session_state.get("curiosity", ""),
                                       st.session_state.get("current_level", ""),
                                       learning_type=st.session_state.get("learning_type", "hana"))
    if not prompt_panel(system, prompt_text, "s3_roadmap",
                        spinner_text="AI가 학습 로드맵을 설계하고 있어요...",
                        btn_label="로드맵 생성"):
        return

    roadmap_data = st.session_state.get("s3_roadmap")
    if not roadmap_data:
        return

    _render_roadmap(roadmap_data)

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True, key="s3_next"):
        st.session_state.current_step = 4
        st.rerun()


def _render_roadmap(data: dict):
    total_duration = data.get("total_duration", "")
    roadmap = data.get("roadmap", [])
    schedule = data.get("weekly_schedule", [])

    st.markdown(f"**학습 로드맵** — 전체 기간: {total_duration}")

    for step in roadmap:
        n = step.get("step_number", "")
        title = step.get("title", "")
        goal = step.get("goal", "")
        prereq = step.get("prerequisite", "없음")
        check = step.get("completion_check", "")
        time_est = step.get("estimated_time", "")
        hint = step.get("resource_hint", "")

        st.markdown(
            f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
            f'padding:14px 18px;margin-bottom:10px;">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">'
            f'<div style="width:28px;height:28px;border-radius:50%;background:#0d9488;color:#fff;'
            f'display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;">{n}</div>'
            f'<div style="font-size:15px;font-weight:700;color:#0a5c52;">{title}</div>'
            f'<div style="font-size:11px;color:#4b7772;margin-left:auto;">{time_est}</div>'
            f'</div>'
            f'<div style="font-size:13px;color:#374151;margin-bottom:6px;">{goal}</div>'
            f'<div style="font-size:12px;color:#4b7772;margin-bottom:4px;">'
            f'<b style="color:#0d9488;">완료 기준:</b> {check}</div>'
            f'<div style="font-size:12px;color:#4b7772;margin-bottom:4px;">'
            f'<b style="color:#0d9488;">사전 지식:</b> {prereq}</div>'
            f'<div style="font-size:12px;color:#4b7772;">'
            f'<b style="color:#0d9488;">자료 힌트:</b> {hint}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if schedule:
        with st.expander("주간 스케줄 보기"):
            for week_data in schedule:
                week = week_data.get("week", "")
                sessions = week_data.get("sessions", [])
                st.markdown(f"**{week}주차**")
                for s in sessions:
                    day = s.get("day", "")
                    step_ref = s.get("step", "")
                    focus = s.get("focus", "")
                    st.markdown(
                        f'<div style="padding:4px 10px;font-size:12px;color:#374151;">'
                        f'<b>{day}</b> — 단계 {step_ref}: {focus}</div>',
                        unsafe_allow_html=True,
                    )
