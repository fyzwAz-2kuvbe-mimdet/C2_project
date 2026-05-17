import streamlit as st
from core.news_crawler import search_news


def render_step3():
    if st.button("← 이전 단계"):
        st.session_state.current_step = 2
        st.rerun()

    diagnosis = st.session_state.get("diagnosis", {})
    topic = diagnosis.get("estimated_subtopic") or st.session_state.get("interest_text", "")

    st.markdown('<div class="section-header">📰 최신 뉴스</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-subheader">"{topic}" 관련 최신 소식 (네이버 뉴스)</div>',
        unsafe_allow_html=True,
    )

    news_items = st.session_state.get("news_items")

    if news_items is None:
        st.markdown(
            '<div class="coach-card" style="text-align:center; padding:32px;">'
            "<p style='font-size:16px; color:#374151; margin-bottom:4px;'>최신 뉴스를 검색해볼까요?</p>"
            "<p style='font-size:13px; color:#9ca3af;'>네이버 뉴스에서 관련 기사를 가져옵니다</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("📡 최신 뉴스 검색", type="primary", use_container_width=True):
            _fetch_news(topic)
    else:
        _render_news(news_items)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 뉴스 새로고침", use_container_width=True):
                st.session_state.news_items = None
                st.rerun()
        with col2:
            if st.button("✏️ 결과물 제출하기 →", type="primary", use_container_width=True):
                st.session_state.step3_complete = True
                st.session_state.current_step = 4
                st.rerun()


def _fetch_news(topic: str):
    with st.spinner("뉴스를 불러오고 있어요..."):
        try:
            news = search_news(topic, max_results=10)
            st.session_state.news_items = news
        except Exception:
            st.session_state.news_items = []
        st.rerun()


def _render_news(news_items: list):
    if not news_items:
        st.warning(
            "관련 뉴스를 찾지 못했습니다. "
            "네이버 접속 환경을 확인하거나 '뉴스 새로고침'을 눌러 다시 시도해보세요."
        )
        return

    st.markdown(
        f"<div style='font-size:13px; color:#6b7280; margin-bottom:12px;'>"
        f"총 {len(news_items)}개의 기사를 찾았어요</div>",
        unsafe_allow_html=True,
    )

    for item in news_items:
        headline = item.get("headline", "")
        link = item.get("link", "#")
        press = item.get("press", "")
        date = item.get("date", "")
        summary = item.get("summary", "")

        st.markdown(
            f"""<div class="news-card">
              <a href="{link}" target="_blank" class="news-headline">{headline}</a>
              <div class="news-meta">{press} &middot; {date}</div>
              {"<div class='news-summary'>" + summary + "</div>" if summary else ""}
            </div>""",
            unsafe_allow_html=True,
        )
