import streamlit as st
from core.step06_reflection import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s6_back"):
        st.session_state.current_step = 5
        st.rerun()

    st.markdown('<div class="section-header">회고 & 연구 계획</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">지금까지 공부한 것을 정리하고 다음 탐구 방향을 설계해요.</div>', unsafe_allow_html=True)

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

    st.markdown("**탐구 내용을 정리해주세요**")

    what_i_studied = st.text_area(
        "지금까지 공부한 내용 요약",
        value=st.session_state.get("s6_what_i_studied", ""),
        placeholder="어떤 개념을, 어떤 순서로, 어떻게 공부했는지 자유롭게 적어주세요.",
        height=120,
        label_visibility="visible",
    )
    if what_i_studied != st.session_state.get("s6_what_i_studied", ""):
        st.session_state.s6_what_i_studied = what_i_studied
        reset_result("s6_reflection")

    most_interesting = st.text_area(
        "가장 흥미로웠던 지점",
        value=st.session_state.get("s6_most_interesting", ""),
        placeholder="공부하면서 가장 흥미롭거나 놀라웠던 순간이 무엇인가요?",
        height=80,
        label_visibility="visible",
    )
    if most_interesting != st.session_state.get("s6_most_interesting", ""):
        st.session_state.s6_most_interesting = most_interesting
        reset_result("s6_reflection")

    stuck_points = st.text_area(
        "막혔거나 이해 안 된 부분",
        value=st.session_state.get("s6_stuck_points", ""),
        placeholder="공부 중 막혔거나 아직 잘 이해가 안 되는 부분이 있나요?",
        height=80,
        label_visibility="visible",
    )
    if stuck_points != st.session_state.get("s6_stuck_points", ""):
        st.session_state.s6_stuck_points = stuck_points
        reset_result("s6_reflection")

    if not st.session_state.get("s6_what_i_studied", "").strip():
        st.markdown(
            '<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
            'padding:12px;font-size:13px;color:#4b7772;margin-top:8px;">'
            '공부한 내용을 적어야 AI가 회고를 도와드릴 수 있어요.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")
    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 분석", key="reset_s6", use_container_width=True):
            reset_result("s6_reflection")
            st.rerun()

    system, prompt_text = build_prompt(
        topic,
        st.session_state.get("s6_what_i_studied", ""),
        st.session_state.get("s6_most_interesting", ""),
        st.session_state.get("s6_stuck_points", ""),
        learning_type=st.session_state.get("learning_type", "hana"),
    )
    if not prompt_panel(system, prompt_text, "s6_reflection",
                        spinner_text="AI가 회고를 분석하고 있어요...",
                        btn_label="회고 분석 시작"):
        return

    result = st.session_state.get("s6_reflection")
    if not result:
        return

    _render_reflection(result)

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True, key="s6_next"):
        st.session_state.current_step = 7
        st.rerun()


def _render_reflection(data: dict):
    reflection = data.get("reflection", {})
    limits = data.get("limits", [])
    limit_q = data.get("limit_question", "")
    apply_tasks = data.get("apply_tasks", [])
    directions = data.get("research_directions", [])
    plan = data.get("my_research_plan", {})

    # 회고
    truly = reflection.get("truly_understood", [])
    surface = reflection.get("surface_level", [])
    ref_q = reflection.get("reflection_question", "")

    st.markdown("**회고 — 내가 이해한 것**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div style="background:#d1fae5;border-radius:8px;padding:10px 14px;font-size:12px;">'
            '<div style="font-weight:700;color:#065f46;margin-bottom:6px;">진짜 이해한 것</div>'
            + "".join(f'<div>• {c}</div>' for c in truly)
            + '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div style="background:#fef3c7;border-radius:8px;padding:10px 14px;font-size:12px;">'
            '<div style="font-weight:700;color:#92400e;margin-bottom:6px;">표면적으로 아는 것</div>'
            + "".join(f'<div>• {c}</div>' for c in surface)
            + '</div>',
            unsafe_allow_html=True,
        )

    if ref_q:
        st.markdown(
            f'<div style="background:#f0faf8;border-left:4px solid #0d9488;border-radius:0 8px 8px 0;'
            f'padding:12px 14px;font-size:13px;color:#0a5c52;font-weight:600;margin:10px 0;">'
            f'회고 질문: {ref_q}</div>',
            unsafe_allow_html=True,
        )

    # 한계
    if limits:
        st.markdown("**한계 인식 — 내가 아직 모르는 것**")
        for lim in limits:
            ltype = lim.get("type", "")
            desc = lim.get("description", "")
            next_step = lim.get("next_step", "")
            st.markdown(
                f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:8px;'
                f'padding:10px 14px;margin-bottom:8px;font-size:12px;">'
                f'<div style="font-weight:700;color:#0d9488;margin-bottom:4px;">{ltype}</div>'
                f'<div style="color:#374151;margin-bottom:4px;">{desc}</div>'
                f'<div style="color:#4b7772;"><b style="color:#0d9488;">해결 방법:</b> {next_step}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if limit_q:
            st.markdown(
                f'<div style="background:#f0faf8;border-left:4px solid #0891b2;border-radius:0 8px 8px 0;'
                f'padding:12px 14px;font-size:13px;color:#0a5c52;font-weight:600;margin:10px 0;">'
                f'한계 질문: {limit_q}</div>',
                unsafe_allow_html=True,
            )

    # 적용 과제
    if apply_tasks:
        st.markdown("**지금 당장 해볼 수 있는 것**")
        for task in apply_tasks:
            t = task.get("task", "")
            disc = task.get("expected_discovery", "")
            st.markdown(
                f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:8px;'
                f'padding:10px 14px;margin-bottom:8px;font-size:12px;">'
                f'<div style="font-weight:600;color:#0a5c52;margin-bottom:4px;">{t}</div>'
                f'<div style="color:#4b7772;"><b style="color:#0d9488;">예상 발견:</b> {disc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # 연구 방향
    if directions:
        st.markdown("**다음 탐구 방향 (3가지)**")
        diff_colors = {"고1 현재": "#d1fae5", "고2 수준": "#fef3c7", "대학 입학 후": "#ede9fe"}
        for d in directions:
            direction = d.get("direction", "")
            core_q = d.get("core_question", "")
            next_study = d.get("next_study", "")
            connects = d.get("connects_to_trend", "")
            diff = d.get("difficulty", "")
            dc = diff_colors.get(diff, "#f0faf8")
            st.markdown(
                f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
                f'padding:12px 16px;margin-bottom:10px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
                f'<div style="font-size:14px;font-weight:700;color:#0a5c52;">{direction}</div>'
                f'<div style="background:{dc};border-radius:6px;padding:2px 8px;font-size:11px;">{diff}</div>'
                f'</div>'
                f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                f'<b style="color:#0d9488;">탐구 질문:</b> {core_q}</div>'
                f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                f'<b style="color:#0d9488;">다음 공부:</b> {next_study}</div>'
                f'<div style="font-size:12px;color:#4b7772;">'
                f'<b style="color:#0d9488;">트렌드 연결:</b> {connects}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # 빈칸 계획서
    if plan is not None:
        st.markdown("**나의 연구 계획서 (직접 작성)**")
        st.markdown(
            '<div style="background:#e8f5f3;border:1px dashed #0d9488;border-radius:10px;'
            'padding:14px;font-size:12px;color:#4b7772;margin-bottom:4px;">'
            'AI가 만든 분석을 참고해서 아래 빈칸을 직접 채워보세요. '
            '이 내용은 다음 단계에서 초록 작성에 활용됩니다.</div>',
            unsafe_allow_html=True,
        )
        for field, label in [
            ("what_i_truly_understood", "내가 진짜 이해한 것"),
            ("my_remaining_question", "내게 남은 질문"),
            ("chosen_direction", "선택한 방향 (위 3가지 중)"),
            ("next_study_topic", "다음에 공부할 주제"),
            ("apply_task_i_will_do", "지금 해볼 적용 과제"),
            ("timeline", "목표 일정"),
        ]:
            st.text_input(label, key=f"plan_{field}", placeholder="직접 적어보세요")
