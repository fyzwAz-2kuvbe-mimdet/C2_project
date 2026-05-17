import streamlit as st
from core.step05_trends import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전", key="s5_back"):
        st.session_state.current_step = 4
        st.rerun()

    st.markdown('<div class="section-header">최신 트렌드 분석</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">이 주제가 현재 세계에서 어떻게 연구되고 있는지 알아봐요.</div>', unsafe_allow_html=True)

    topic = (st.session_state.get("selected_topic") or {}).get("name", "")
    if not topic:
        st.warning("선택된 주제가 없습니다. 이전 단계로 돌아가 주제를 선택해주세요.")
        return

    st.markdown(
        f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:10px;'
        f'padding:10px 14px;font-size:13px;color:#374151;margin-bottom:12px;">'
        f'<span style="color:#0d9488;font-weight:700;">탐구 주제:</span> {topic}</div>',
        unsafe_allow_html=True,
    )

    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("다시 분석", key="reset_s5", use_container_width=True):
            reset_result("s5_trends")
            st.rerun()

    current_level = st.session_state.get("current_level", "")
    system, prompt_text = build_prompt(topic, current_level, learning_type=st.session_state.get("learning_type", "hana"))
    if not prompt_panel(system, prompt_text, "s5_trends",
                        spinner_text="AI가 최신 트렌드를 분석하고 있어요...",
                        btn_label="트렌드 분석 시작"):
        return

    trends_data = st.session_state.get("s5_trends") or {}
    if not trends_data:
        return

    _render_trends(trends_data)

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True, key="s5_next"):
        st.session_state.current_step = 6
        st.rerun()


def _render_trends(data: dict):
    topic_type = data.get("topic_type", "")
    trends = data.get("trends", {})

    st.markdown(
        f'<div style="background:#e8f5f3;border-radius:8px;padding:8px 14px;'
        f'font-size:12px;color:#0a5c52;font-weight:700;margin-bottom:12px;">'
        f'주제 유형: {topic_type}</div>',
        unsafe_allow_html=True,
    )

    layer_cfg = [
        ("layer1_current_research", "#0d9488", "층위 1: 지금 연구자들이 파고드는 문제"),
        ("layer2_real_applications", "#0891b2", "층위 2: 현실에서 이미 쓰이고 있는 곳"),
        ("layer3_student_directions", "#059669", "층위 3: 내가 탐구해볼 수 있는 방향"),
    ]

    for key, color, default_title in layer_cfg:
        layer = trends.get(key, {})
        if not layer:
            continue
        title = layer.get("title", default_title)
        items = layer.get("items", [])

        st.markdown(
            f'<div style="border-left:4px solid {color};padding-left:12px;margin-bottom:14px;">'
            f'<div style="font-size:14px;font-weight:700;color:{color};margin-bottom:8px;">{title}</div>',
            unsafe_allow_html=True,
        )

        for item in items:
            if key == "layer1_current_research":
                q = item.get("research_question", "")
                why = item.get("why_matters", "")
                where = item.get("where_to_find", {})
                platform = where.get("platform", "")
                skw = where.get("search_keyword", "")
                st.markdown(
                    f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:8px;'
                    f'padding:10px 14px;margin-bottom:8px;">'
                    f'<div style="font-size:13px;font-weight:600;color:#0a5c52;margin-bottom:4px;">{q}</div>'
                    f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">{why}</div>'
                    f'<div style="font-size:11px;color:#4b7772;">'
                    f'탐색: {platform} | 검색어: {skw}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            elif key == "layer2_real_applications":
                app = item.get("application", "")
                how = item.get("how_it_connects", "")
                where = item.get("where_to_find", {})
                platform = where.get("platform", "")
                skw = where.get("search_keyword", "")
                st.markdown(
                    f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:8px;'
                    f'padding:10px 14px;margin-bottom:8px;">'
                    f'<div style="font-size:13px;font-weight:600;color:#0a5c52;margin-bottom:4px;">{app}</div>'
                    f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">{how}</div>'
                    f'<div style="font-size:11px;color:#4b7772;">'
                    f'탐색: {platform} | 검색어: {skw}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            elif key == "layer3_student_directions":
                q = item.get("my_question", "")
                connects = item.get("connects_to_trend", "")
                leads = item.get("leads_to_field", "")
                st.markdown(
                    f'<div style="background:#f0faf8;border:1px solid #c9e6e1;border-radius:8px;'
                    f'padding:10px 14px;margin-bottom:8px;">'
                    f'<div style="font-size:13px;font-weight:600;color:#0a5c52;margin-bottom:4px;">{q}</div>'
                    f'<div style="font-size:12px;color:#374151;margin-bottom:4px;">'
                    f'<b style="color:{color};">트렌드 연결:</b> {connects}</div>'
                    f'<div style="font-size:12px;color:#374151;">'
                    f'<b style="color:{color};">이어지는 분야:</b> {leads}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('</div>', unsafe_allow_html=True)
