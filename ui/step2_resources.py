from urllib.parse import quote

import streamlit as st
from core.resource_recommender import recommend

_BADGE = {
    "책":    ("badge-책",    "📕"),
    "사이트": ("badge-사이트", "🌐"),
    "논문":  ("badge-논문",  "📄"),
    "영상":  ("badge-영상",  "🎬"),
}
_LEVEL_COLOR = {
    "입문": "#10b981",
    "심화": "#f59e0b",
    "전문": "#ef4444",
}


def render_step2():
    if st.button("← 이전 단계"):
        st.session_state.current_step = 1
        st.rerun()

    diagnosis = st.session_state.get("diagnosis", {})
    subtopic = diagnosis.get("estimated_subtopic") or st.session_state.get("interest_text", "")

    st.markdown('<div class="section-header">📚 맞춤 학습 자료</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-subheader">"{subtopic}" 관련 자료를 유형·학년에 맞게 추천해드려요</div>',
        unsafe_allow_html=True,
    )

    resources = st.session_state.get("resources")

    if resources is None:
        st.markdown(
            '<div class="coach-card" style="text-align:center; padding:32px;">'
            "<p style='font-size:16px; color:#374151; margin-bottom:4px;'>준비가 됐으면 아래 버튼을 눌러주세요</p>"
            "<p style='font-size:13px; color:#9ca3af;'>Gemini AI가 5~8개의 맞춤 자료를 선별해드려요</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("🔍 맞춤 학습 자료 찾기", type="primary", use_container_width=True):
            _generate_resources(subtopic)
    else:
        _render_resources(resources)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 새로 추천받기", use_container_width=True):
                st.session_state.resources = None
                st.rerun()
        with col2:
            if st.button("📰 최신 뉴스 보기 →", type="primary", use_container_width=True):
                st.session_state.step2_complete = True
                st.session_state.current_step = 3
                st.rerun()


def _generate_resources(subtopic: str):
    with st.spinner("맞춤 학습 자료를 찾고 있어요... (10~20초)"):
        try:
            resources = recommend(
                subtopic,
                st.session_state.grade,
                st.session_state.learning_type,
                st.session_state.get("user_answers", {}),
            )
            st.session_state.resources = resources
            st.rerun()
        except Exception as e:
            st.session_state.resources = []
            st.error(f"자료 추천 중 오류가 발생했습니다: {e}")


def _render_resources(resources: list):
    if not resources:
        st.warning("추천 자료를 찾지 못했습니다. '새로 추천받기'를 눌러 다시 시도해보세요.")
        return

    for i in range(0, len(resources), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(resources):
                break
            with col:
                _resource_card(resources[idx])
            st.markdown("")


def _get_link(r: dict) -> str:
    source = r.get("source_url", "")
    if source.startswith("http"):
        return source
    title = quote(r.get("title", ""))
    rtype = r.get("type", "")
    if rtype == "책":
        return f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={title}"
    if rtype == "논문":
        return f"https://scholar.google.com/scholar?q={title}"
    if rtype == "영상":
        return f"https://www.youtube.com/results?search_query={title}"
    return f"https://www.google.com/search?q={title}"


def _resource_card(r: dict):
    rtype = r.get("type", "기타")
    badge_cls, icon = _BADGE.get(rtype, ("badge-기타", "📌"))
    level = r.get("level", "")
    lc = _LEVEL_COLOR.get(level, "#6b7280")
    source = r.get("source_url", "")
    link = _get_link(r)
    if source.startswith("http"):
        source_label = "바로가기"
        caution = ""
    elif rtype == "책":
        source_label = "알라딘 검색"
        caution = " <span style='font-size:10px;color:#f59e0b;'>※검색 후 실존 확인</span>"
    elif rtype == "논문":
        source_label = "Scholar 검색"
        caution = " <span style='font-size:10px;color:#f59e0b;'>※검색 후 실존 확인</span>"
    else:
        source_label = "검색"
        caution = ""
    source_html = f'<a href="{link}" target="_blank" style="color:#3b82f6; font-size:12px; font-weight:600;">🔗 {source_label}</a>{caution}'

    st.markdown(
        f"""<div class="resource-card">
          <span class="resource-badge {badge_cls}">{icon} {rtype}</span>
          <span style="display:inline-block; margin-left:6px; padding:3px 8px;
                       background:{lc}22; color:{lc}; border-radius:20px;
                       font-size:11px; font-weight:700;">{level}</span>
          <div class="resource-title">{r.get('title', '')}</div>
          <div class="resource-why">{r.get('why', '')}</div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
            {source_html}
            <span style="font-size:11px; color:#9ca3af;">⏱ {r.get('duration', '')}</span>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
