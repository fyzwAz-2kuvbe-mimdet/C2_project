import streamlit as st
from core.step09_knowledge_map import build_r1_prompt, build_r2_prompt, build_r3_prompt
from utils.ai_runner import prompt_panel, reset_result, is_done


def render():
    if st.button("← 이전", key="s9_back"):
        st.session_state.current_step = 8
        st.rerun()

    st.markdown('<div class="section-header">지식 지도</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">3라운드 대화로 지금까지 공부한 것을 한 장의 지식 지도로 완성해요.</div>', unsafe_allow_html=True)

    topic = (st.session_state.get("selected_topic") or {}).get("name", "")
    if not topic:
        st.warning("선택된 주제가 없습니다. 처음 단계부터 시작해주세요.")
        return

    # 초록 전문 (7단계에서 가져옴)
    abstract_data = st.session_state.get("s7_abstract") or {}
    final_abstract = abstract_data.get("full_text", "")

    # ── 초기 입력 폼 ──
    st.markdown("**지식 지도 작성을 위한 정보 입력**")

    study_summary = st.text_area(
        "1~8단계를 거치며 공부한 것",
        value=st.session_state.get("s9_study_summary", ""),
        placeholder="어떤 개념을 공부했고, 어떤 흐름으로 이해했는지 요약해주세요.",
        height=100,
        label_visibility="visible",
    )
    if study_summary != st.session_state.get("s9_study_summary", ""):
        st.session_state.s9_study_summary = study_summary
        _reset_all_rounds()

    most_interesting = st.text_area(
        "가장 흥미로웠던 개념",
        value=st.session_state.get("s9_most_interesting", ""),
        placeholder="공부 중 가장 흥미로웠던 개념이나 발견은 무엇인가요?",
        height=70,
        label_visibility="visible",
    )
    if most_interesting != st.session_state.get("s9_most_interesting", ""):
        st.session_state.s9_most_interesting = most_interesting
        _reset_all_rounds()

    stuck_points = st.text_area(
        "막혔거나 이해 안 된 것",
        value=st.session_state.get("s9_stuck_points", ""),
        placeholder="아직 잘 모르거나 연결이 안 된 개념이 있나요?",
        height=70,
        label_visibility="visible",
    )
    if stuck_points != st.session_state.get("s9_stuck_points", ""):
        st.session_state.s9_stuck_points = stuck_points
        _reset_all_rounds()

    if not st.session_state.get("s9_study_summary", "").strip():
        st.markdown(
            '<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
            'padding:12px;font-size:13px;color:#4b7772;margin-top:8px;">'
            '공부한 내용을 입력하면 라운드 1을 시작할 수 있어요.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")

    # ── 라운드 1 ──
    st.markdown(
        '<div style="background:#e8f5f3;border-radius:8px;padding:8px 14px;'
        'font-size:13px;font-weight:700;color:#0a5c52;margin-bottom:10px;">'
        '라운드 1 — 개념 추출 & 미러링</div>',
        unsafe_allow_html=True,
    )

    col_r1, _ = st.columns([1, 4])
    with col_r1:
        if st.button("R1 초기화", key="reset_r1", use_container_width=True):
            _reset_all_rounds()
            st.rerun()

    _ltype = st.session_state.get("learning_type", "hana")
    sys1, p1 = build_r1_prompt(
        topic,
        st.session_state.get("s9_study_summary", ""),
        st.session_state.get("s9_most_interesting", ""),
        st.session_state.get("s9_stuck_points", ""),
        final_abstract,
        learning_type=_ltype,
    )
    if not prompt_panel(sys1, p1, "s9_r1",
                        spinner_text="AI가 개념을 추출하고 있어요...",
                        btn_label="라운드 1 시작"):
        return

    r1 = st.session_state.get("s9_r1") or {}
    _render_r1(r1)

    # ── 학생 R1 피드백 ──
    st.markdown("**라운드 1 확인 답변**")
    st.markdown(
        '<div style="font-size:12px;color:#4b7772;margin-bottom:6px;">'
        '빠진 개념, AI 추론 연결 중 다른 것, 고립 개념 중 사실은 연결된 것이 있다면 적어주세요.</div>',
        unsafe_allow_html=True,
    )
    student_r1 = st.text_area(
        "R1 답변",
        value=st.session_state.get("s9_student_r1", ""),
        placeholder="예: 'X 개념이 빠졌어요', 'A→B 연결은 제 생각과 달라요', '없어요' 등",
        height=80,
        label_visibility="collapsed",
    )
    if student_r1 != st.session_state.get("s9_student_r1", ""):
        st.session_state.s9_student_r1 = student_r1
        reset_result("s9_r2")
        reset_result("s9_r3")

    if not st.session_state.get("s9_student_r1", "").strip():
        st.markdown(
            '<div style="font-size:12px;color:#4b7772;">'
            '"없어요" 라도 입력해야 라운드 2로 진행됩니다.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")

    # ── 라운드 2 ──
    st.markdown(
        '<div style="background:#e0f2fe;border-radius:8px;padding:8px 14px;'
        'font-size:13px;font-weight:700;color:#0c4a6e;margin-bottom:10px;">'
        '라운드 2 — 구조 설계 & 빈 칸 가시화</div>',
        unsafe_allow_html=True,
    )

    col_r2, _ = st.columns([1, 4])
    with col_r2:
        if st.button("R2 초기화", key="reset_r2", use_container_width=True):
            reset_result("s9_r2")
            reset_result("s9_r3")
            st.rerun()

    sys2, p2 = build_r2_prompt(
        topic,
        st.session_state.get("s9_study_summary", ""),
        st.session_state.get("s9_most_interesting", ""),
        st.session_state.get("s9_stuck_points", ""),
        final_abstract,
        r1,
        st.session_state.get("s9_student_r1", ""),
        learning_type=_ltype,
    )
    if not prompt_panel(sys2, p2, "s9_r2",
                        spinner_text="AI가 지식 지도 구조를 설계하고 있어요...",
                        btn_label="라운드 2 시작"):
        return

    r2 = st.session_state.get("s9_r2") or {}
    _render_r2(r2)

    # ── 학생 R2 피드백 ──
    st.markdown("**라운드 2 확인 답변**")
    st.markdown(
        '<div style="font-size:12px;color:#4b7772;margin-bottom:6px;">'
        '중심 개념 확인, 빈 칸 A 수정, 빈 칸 B 중 탐구하고 싶은 것이 있으면 적어주세요.</div>',
        unsafe_allow_html=True,
    )
    student_r2 = st.text_area(
        "R2 답변",
        value=st.session_state.get("s9_student_r2", ""),
        placeholder="예: '중심 개념이 맞아요', '빈 칸 B 중 X가 흥미로워요', '없어요' 등",
        height=80,
        label_visibility="collapsed",
    )
    if student_r2 != st.session_state.get("s9_student_r2", ""):
        st.session_state.s9_student_r2 = student_r2
        reset_result("s9_r3")

    if not st.session_state.get("s9_student_r2", "").strip():
        st.markdown(
            '<div style="font-size:12px;color:#4b7772;">'
            '"없어요" 라도 입력해야 라운드 3으로 진행됩니다.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("---")

    # ── 라운드 3 ──
    st.markdown(
        '<div style="background:#d1fae5;border-radius:8px;padding:8px 14px;'
        'font-size:13px;font-weight:700;color:#065f46;margin-bottom:10px;">'
        '라운드 3 — 지식 지도 완성 & 탐구 씨앗</div>',
        unsafe_allow_html=True,
    )

    col_r3, _ = st.columns([1, 4])
    with col_r3:
        if st.button("R3 초기화", key="reset_r3", use_container_width=True):
            reset_result("s9_r3")
            st.rerun()

    sys3, p3 = build_r3_prompt(
        topic,
        st.session_state.get("s9_study_summary", ""),
        st.session_state.get("s9_most_interesting", ""),
        st.session_state.get("s9_stuck_points", ""),
        final_abstract,
        r1,
        st.session_state.get("s9_student_r1", ""),
        r2,
        st.session_state.get("s9_student_r2", ""),
        learning_type=_ltype,
    )
    if not prompt_panel(sys3, p3, "s9_r3",
                        spinner_text="AI가 최종 지식 지도를 완성하고 있어요...",
                        btn_label="라운드 3 시작"):
        return

    r3 = st.session_state.get("s9_r3") or {}
    selected_seed = _render_r3(r3)

    if selected_seed:
        st.session_state.selected_seed = selected_seed
        st.markdown("")
        if st.button("다음 단계", type="primary", use_container_width=True, key="s9_next"):
            st.session_state.current_step = 10
            st.rerun()
    else:
        st.markdown(
            '<div style="font-size:12px;color:#4b7772;margin-top:8px;">'
            '탐구 씨앗 하나를 선택해야 10단계로 진행할 수 있어요.</div>',
            unsafe_allow_html=True,
        )


def _reset_all_rounds():
    reset_result("s9_r1")
    reset_result("s9_r2")
    reset_result("s9_r3")
    st.session_state.s9_student_r1 = ""
    st.session_state.s9_student_r2 = ""


def _render_r1(data: dict):
    concepts = data.get("concepts", [])
    connections = data.get("connections", [])
    isolated = data.get("isolated_concepts", [])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**추출된 개념 ({len(concepts)}개)**")
        for c in concepts:
            ctype = "직접" if "직접" in c.get("type", "") else "암묵"
            st.markdown(
                f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:6px;'
                f'padding:6px 10px;margin-bottom:4px;font-size:12px;">'
                f'<b>{c.get("name", "")}</b>'
                f'<span style="color:#4b7772;font-size:10px;margin-left:6px;">[{ctype}]</span>'
                f'<div style="color:#4b7772;font-size:11px;">{c.get("context", "")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown(f"**연결 ({len(connections)}개)**")
        for conn in connections:
            src = "학생" if "학생" in conn.get("source", "") else "AI 추론"
            st.markdown(
                f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:6px;'
                f'padding:6px 10px;margin-bottom:4px;font-size:12px;">'
                f'{conn.get("from", "")} → {conn.get("to", "")}'
                f'<span style="color:#4b7772;font-size:10px;margin-left:6px;">[{src}]</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if isolated:
            st.markdown(f"**고립 개념 ({len(isolated)}개)**")
            for iso in isolated:
                st.markdown(
                    f'<div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;'
                    f'padding:6px 10px;margin-bottom:4px;font-size:12px;">'
                    f'{iso.get("name", "")}'
                    f'</div>',
                    unsafe_allow_html=True,
                )


def _render_r2(data: dict):
    map_structure = data.get("map_structure", {})
    gap_list = data.get("gap_list", {})
    core = map_structure.get("core_concepts", [])
    branches = map_structure.get("branches", [])
    gap_a = gap_list.get("gap_a", [])
    gap_b = gap_list.get("gap_b", [])

    st.markdown(f"**핵심 개념:** {', '.join(core)}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**빈 칸 A — 내가 모르는 것 ({len(gap_a)}개)**")
        for g in gap_a:
            st.markdown(
                f'<div style="background:#fee2e2;border-radius:6px;padding:6px 10px;'
                f'margin-bottom:4px;font-size:12px;">'
                f'<b>{g.get("name", "")}</b><br/>'
                f'<span style="color:#4b7772;">{g.get("how_to_fill", "")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown(f"**빈 칸 B — 아직 못 만난 것 ({len(gap_b)}개)**")
        for g in gap_b:
            st.markdown(
                f'<div style="background:#ede9fe;border-radius:6px;padding:6px 10px;'
                f'margin-bottom:4px;font-size:12px;">'
                f'<b>{g.get("name", "")}</b><br/>'
                f'<span style="color:#4b7772;">{g.get("leads_to", "")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if branches:
        with st.expander("지식 지도 구조 보기"):
            for b in branches:
                concept = b.get("concept", "")
                level = b.get("level", "")
                st.markdown(
                    f'<div style="border-left:3px solid #0d9488;padding-left:10px;margin-bottom:8px;">'
                    f'<b style="color:#0a5c52;">{concept}</b> '
                    f'<span style="font-size:11px;color:#4b7772;">[{level}]</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


def _render_r3(data: dict) -> str:
    final_map = data.get("final_map", {})
    seeds = data.get("exploration_seeds", [])
    core = final_map.get("core_concepts", [])
    confirmed = final_map.get("confirmed_connections", [])

    st.markdown(f"**확정 핵심 개념:** {', '.join(core)}")
    st.markdown(f"**확인된 연결:** {len(confirmed)}개")

    if seeds:
        st.markdown("**탐구 씨앗 목록 — 하나를 선택해 10단계로 넘어가세요**")
        current_seed = st.session_state.get("selected_seed", "")

        for i, seed in enumerate(seeds):
            q = seed.get("seed_question", "")
            field = seed.get("connected_field", "")
            diff = seed.get("difficulty", "")
            connects = seed.get("connects_to_map", "")
            is_sel = q == current_seed

            diff_colors = {
                "지금 당장": "#d1fae5",
                "고2 수준": "#fef3c7",
                "대학 입학 후": "#ede9fe",
            }
            dc = diff_colors.get(diff, "#f0faf8")

            # CSS marker for button
            st.markdown(
                f"<style>"
                f".element-container:has(#seed-{i}) + .element-container button{{"
                f"  border-left:5px solid #059669 !important;"
                f"  border-radius:0 10px 10px 0 !important;"
                f"  white-space:pre-line !important;"
                f"  text-align:left !important;"
                f"  height:auto !important;"
                f"  min-height:80px !important;"
                f"  padding:12px 16px !important;"
                f"}}"
                f"</style>"
                f'<span id="seed-{i}"></span>',
                unsafe_allow_html=True,
            )
            label = f"{q}\n{field}  |  {diff}"
            if st.button(label, key=f"seed_btn_{i}", use_container_width=True,
                         type="primary" if is_sel else "secondary"):
                st.session_state.selected_seed = q
                st.rerun()

        return st.session_state.get("selected_seed", "")

    return ""
