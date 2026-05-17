import streamlit as st
from core.step10_curriculum import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s10_back"):
        st.session_state.current_step = 9
        st.rerun()

    st.markdown('<div class="section-header">교과 재연결</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">탐구 결과를 학교 교과와 연결하고 학습 루프를 완성해요.</div>', unsafe_allow_html=True)

    topic = (st.session_state.get("selected_topic") or {}).get("name", "")
    if not topic:
        st.warning("선택된 주제가 없습니다. 처음 단계부터 시작해주세요.")
        return

    selected_seed = st.session_state.get("selected_seed", "")

    st.markdown(
        f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
        f'padding:10px 14px;font-size:13px;color:#374151;margin-bottom:14px;">'
        f'<div><span style="color:#0d9488;font-weight:700;">탐구 주제:</span> {topic}</div>'
        + (f'<div style="margin-top:4px;"><span style="color:#059669;font-weight:700;">탐구 씨앗:</span> {selected_seed}</div>' if selected_seed else '')
        + '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("**10단계 정보를 입력해주세요**")

    key_findings = st.text_area(
        "탐구를 통해 발견한 것",
        value=st.session_state.get("s10_key_findings", ""),
        placeholder="이번 탐구에서 가장 중요하게 발견한 것 2~3가지를 적어주세요.",
        height=80,
        label_visibility="visible",
    )
    if key_findings != st.session_state.get("s10_key_findings", ""):
        st.session_state.s10_key_findings = key_findings
        reset_result("s10_result")

    my_idea = st.text_area(
        "탐구에서 나온 나의 아이디어",
        value=st.session_state.get("s10_my_idea", ""),
        placeholder="탐구하면서 떠오른 나만의 아이디어나 응용 방안이 있나요?",
        height=80,
        label_visibility="visible",
    )
    if my_idea != st.session_state.get("s10_my_idea", ""):
        st.session_state.s10_my_idea = my_idea
        reset_result("s10_result")

    current_subjects = st.text_area(
        "현재 수강 중인 교과목",
        value=st.session_state.get("s10_current_subjects", ""),
        placeholder="예: 수학I, 통합과학, 경제, 언어와매체...",
        height=60,
        label_visibility="visible",
    )
    if current_subjects != st.session_state.get("s10_current_subjects", ""):
        st.session_state.s10_current_subjects = current_subjects
        reset_result("s10_result")

    if not st.session_state.get("s10_key_findings", "").strip():
        st.markdown(
            '<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
            'padding:12px;font-size:13px;color:#4b7772;margin-top:8px;">'
            '탐구에서 발견한 것을 입력하면 AI가 교과 연결을 분석해요.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")
    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 분석", key="reset_s10", use_container_width=True):
            reset_result("s10_result")
            st.rerun()

    system, prompt_text = build_prompt(
        topic,
        st.session_state.get("s10_key_findings", ""),
        st.session_state.get("s10_my_idea", ""),
        selected_seed,
        st.session_state.get("s10_current_subjects", ""),
        learning_type=st.session_state.get("learning_type", "hana"),
    )
    if not prompt_panel(system, prompt_text, "s10_result",
                        spinner_text="AI가 교과 연결을 분석하고 있어요...",
                        btn_label="교과 재연결 분석"):
        return

    result = st.session_state.get("s10_result")
    if not result:
        return

    _render_curriculum(result)

    st.markdown("---")
    st.markdown(
        '<div style="background:#e8f5f3;border:2px solid #0d9488;border-radius:14px;'
        'padding:20px;text-align:center;">'
        '<div style="font-size:18px;font-weight:800;color:#0a5c52;margin-bottom:6px;">'
        '10단계 탐구 여정을 완료했어요!</div>'
        '<div style="font-size:13px;color:#4b7772;">'
        '탐구 씨앗을 가지고 다음 사이클을 시작해보세요.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")
    if st.button("처음부터 새 탐구 시작", type="primary", use_container_width=True):
        from utils.session import reset_all
        reset_all()
        st.rerun()


def _render_curriculum(data: dict):
    connections = data.get("step1_connections", [])
    next_study = data.get("step2_next_study", [])
    loop = data.get("step3_learning_loop", {})

    depth_colors = {
        "표면 연결": "#f0faf8",
        "구조 연결": "#e0f2fe",
        "심화 연결": "#ede9fe",
    }

    # STEP 1: 교과 연결
    if connections:
        st.markdown("**탐구 결과 ↔ 교과 개념 연결**")
        for conn in connections:
            finding = conn.get("finding", "")
            subject = conn.get("subject", "")
            concept = conn.get("concept", "")
            depth = conn.get("connection_depth", "")
            why = conn.get("why_same_structure", "")
            dc = depth_colors.get(depth, "#f0faf8")
            st.markdown(
                f'<div style="background:{dc};border:1px solid #c9e6e1;border-radius:10px;'
                f'padding:12px 14px;margin-bottom:8px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
                f'<div style="font-size:13px;font-weight:700;color:#0a5c52;">{subject} — {concept}</div>'
                f'<div style="font-size:11px;color:#4b7772;background:#fff;border-radius:4px;padding:2px 6px;">{depth}</div>'
                f'</div>'
                f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                f'<b style="color:#0d9488;">탐구 발견:</b> {finding}</div>'
                f'<div style="font-size:12px;color:#4b7772;">'
                f'<b style="color:#0d9488;">같은 원리인 이유:</b> {why}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # STEP 2: 다음 공부할 교과
    if next_study:
        st.markdown("**지금 공부하면 탐구가 깊어지는 교과 개념**")
        for study in next_study:
            subj = study.get("subject", "")
            unit = study.get("unit", "")
            why_now = study.get("why_now", "")
            gap = study.get("gap_it_fills", "")
            path = study.get("path", "")
            level = study.get("level", "")
            level_color = "#d1fae5" if "현재" in level else "#fef3c7"
            st.markdown(
                f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
                f'padding:12px 14px;margin-bottom:8px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
                f'<div style="font-size:14px;font-weight:700;color:#0a5c52;">{subj} — {unit}</div>'
                f'<div style="background:{level_color};border-radius:4px;padding:2px 8px;font-size:11px;">{level}</div>'
                f'</div>'
                f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                f'<b style="color:#0d9488;">지금 공부하면:</b> {why_now}</div>'
                f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                f'<b style="color:#0d9488;">채워지는 빈 칸:</b> {gap}</div>'
                f'<div style="font-size:12px;color:#4b7772;">'
                f'<b style="color:#0d9488;">경로:</b> {path}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # STEP 3: 학습 루프
    if loop:
        st.markdown("**학습 루프**")
        stages = loop.get("loop_stages", [])
        gain = loop.get("loop_gain", "")
        next_seed = loop.get("next_cycle_seed", "")

        stage_colors = ["#0d9488", "#0891b2", "#059669", "#7c3aed"]
        for i, stage in enumerate(stages):
            color = stage_colors[i % len(stage_colors)]
            action = stage.get("action", "")
            enables = stage.get("what_it_enables", "")
            st.markdown(
                f'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px;">'
                f'<div style="width:28px;height:28px;border-radius:50%;background:{color};color:#fff;'
                f'display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;'
                f'flex-shrink:0;">{i+1}</div>'
                f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:8px;'
                f'padding:10px 12px;flex:1;">'
                f'<div style="font-size:13px;font-weight:600;color:#0a5c52;margin-bottom:3px;">{action}</div>'
                f'<div style="font-size:11px;color:#4b7772;">{enables}</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

        if gain:
            st.markdown(
                f'<div style="background:#e8f5f3;border:1px solid #0d9488;border-radius:10px;'
                f'padding:12px 14px;margin-top:8px;">'
                f'<div style="font-size:12px;font-weight:700;color:#0a5c52;margin-bottom:4px;">루프 한 바퀴 후 얻는 것</div>'
                f'<div style="font-size:13px;color:#374151;">{gain}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if next_seed:
            st.markdown(
                f'<div style="background:#ede9fe;border:1px solid #7c3aed;border-radius:10px;'
                f'padding:12px 14px;margin-top:8px;">'
                f'<div style="font-size:12px;font-weight:700;color:#5b21b6;margin-bottom:4px;">다음 사이클 탐구 씨앗</div>'
                f'<div style="font-size:13px;color:#374151;">{next_seed}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
