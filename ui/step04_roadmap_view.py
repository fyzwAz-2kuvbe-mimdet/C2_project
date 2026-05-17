import streamlit as st
from core.step04_resources import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s4_back"):
        st.session_state.current_step = 3
        st.rerun()

    st.markdown('<div class="section-header">단계별 자료 탐색</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">각 학습 단계에 맞는 자료를 어디서 어떻게 찾는지 안내해드려요.</div>', unsafe_allow_html=True)

    topic = (st.session_state.get("selected_topic") or {}).get("name", "")
    roadmap_data = st.session_state.get("s3_roadmap") or {}
    roadmap = roadmap_data.get("roadmap", [])

    if not topic or not roadmap:
        st.warning("로드맵이 없습니다. 이전 단계로 돌아가 로드맵을 생성해주세요.")
        return

    st.markdown(
        f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
        f'padding:10px 14px;font-size:13px;color:#374151;margin-bottom:12px;">'
        f'<span style="color:#0d9488;font-weight:700;">탐구 주제:</span> {topic}</div>',
        unsafe_allow_html=True,
    )

    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 생성", key="reset_s4", use_container_width=True):
            reset_result("s4_resources")
            st.rerun()

    system, prompt_text = build_prompt(topic, roadmap, learning_type=st.session_state.get("learning_type", "hana"))
    if not prompt_panel(system, prompt_text, "s4_resources",
                        spinner_text="AI가 자료 탐색 경로를 안내하고 있어요...",
                        btn_label="자료 탐색 경로 안내받기"):
        return

    resources_data = st.session_state.get("s4_resources") or {}
    resources_by_step = resources_data.get("resources", {})
    if not resources_by_step:
        st.warning("자료를 불러오지 못했습니다. 다시 시도해주세요.")
        return

    st.markdown("**단계별 탐색 경로**")

    for step in roadmap:
        n = str(step.get("step_number", ""))
        title = step.get("title", "")
        items = resources_by_step.get(n, [])

        with st.expander(f"단계 {n}: {title} ({len(items)}개 자료)"):
            if not items:
                st.markdown('<div style="color:#4b7772;font-size:13px;">자료 없음</div>', unsafe_allow_html=True)
                continue
            for item in items:
                rtype = item.get("type", "")
                level = item.get("level", "")
                where = item.get("where", "")
                keyword = item.get("search_keyword", "")
                what_to_see = item.get("what_to_see", "")
                connects_to = item.get("connects_to", "")

                level_colors = {"입문": "#d1fae5", "중급": "#fef3c7", "심화": "#ede9fe"}
                lc = level_colors.get(level, "#f0faf8")

                st.markdown(
                    f'<div style="background:#fff;border:1px solid #c9e6e1;border-radius:8px;'
                    f'padding:12px 14px;margin-bottom:8px;">'
                    f'<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;">'
                    f'<span style="background:#0d9488;color:#fff;border-radius:4px;padding:2px 8px;font-size:11px;font-weight:700;">{rtype}</span>'
                    f'<span style="background:{lc};border-radius:4px;padding:2px 8px;font-size:11px;">{level}</span>'
                    f'</div>'
                    f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                    f'<b style="color:#0d9488;">어디서:</b> {where}</div>'
                    f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                    f'<b style="color:#0d9488;">검색어:</b> {keyword}</div>'
                    f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                    f'<b style="color:#0d9488;">무엇을 볼까:</b> {what_to_see}</div>'
                    f'<div style="font-size:12px;color:#4b7772;">'
                    f'<b style="color:#0d9488;">연결:</b> {connects_to}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True, key="s4_next"):
        st.session_state.current_step = 5
        st.rerun()
