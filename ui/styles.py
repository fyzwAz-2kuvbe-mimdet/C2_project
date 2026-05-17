import re
import streamlit as st

_FONT = (
    '<link rel="stylesheet" '
    'href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard'
    '/dist/web/static/pretendard.css">'
)

_CSS = """
*, *::before, *::after {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  letter-spacing: -0.01em;
}
body { background: #e8f5f3; }
.main .block-container { max-width: 800px; padding-top: 1rem; padding-bottom: 5rem; }
.coach-card {
  background: #fff; border: 1px solid #c9e6e1; border-radius: 14px;
  padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(13,148,136,.07);
}
.roadmap-item { display: flex; gap: 16px; margin-bottom: 20px; position: relative; }
.roadmap-line { display: flex; flex-direction: column; align-items: center; }
.roadmap-dot {
  width: 36px; height: 36px; border-radius: 50%;
  background: #0d9488; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px; flex-shrink: 0;
}
.roadmap-connector { width: 2px; flex: 1; background: #c9e6e1; margin: 4px 0; min-height: 24px; }
.roadmap-content { flex: 1; padding-bottom: 8px; }
.roadmap-goal { font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 6px; }
.roadmap-meta { font-size: 12px; color: #6b7280; }
.resource-card {
  background: #fff; border: 1px solid #c9e6e1; border-radius: 12px;
  padding: 16px; margin-bottom: 10px; transition: transform .15s, box-shadow .15s;
}
.resource-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(13,148,136,.12); }
.badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.badge-책    { background: #dbeafe; color: #1d4ed8; }
.badge-사이트 { background: #d1fae5; color: #065f46; }
.badge-논문  { background: #ede9fe; color: #5b21b6; }
.badge-영상  { background: #fef3c7; color: #92400e; }
.badge-기타  { background: #f0faf8; color: #0d9488; }
.news-card { background: #fff; border: 1px solid #c9e6e1; border-radius: 12px; padding: 14px 18px; margin-bottom: 10px; }
.news-headline { font-size: 15px; font-weight: 600; color: #111827; text-decoration: none; line-height: 1.5; }
.news-headline:hover { color: #0d9488; }
.news-meta { font-size: 12px; color: #9ca3af; margin-top: 4px; }
.news-summary-box {
  background: #f0faf8; border-left: 3px solid #0d9488;
  border-radius: 0 8px 8px 0; padding: 10px 14px;
  font-size: 13px; color: #374151; line-height: 1.6; margin-top: 10px;
}
.score-bar-bg { background: #dff0ec; border-radius: 999px; height: 8px; overflow: hidden; margin-top: 4px; }
.score-bar-fill { height: 100%; border-radius: 999px; transition: width .5s ease; }
.section-header    { font-size: 22px; font-weight: 800; color: #0a5c52; margin-bottom: 4px; }
.section-subheader { font-size: 14px; color: #4b7772; margin-bottom: 20px; }
.type-card {
  background: #fff; border: 1.5px solid #c9e6e1; border-radius: 14px;
  padding: 18px 20px; transition: transform .15s, box-shadow .15s, border-color .15s;
  margin-bottom: 10px;
}
.type-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(13,148,136,.1); }
.type-card.selected { border-color: #0d9488; box-shadow: 0 0 0 3px rgba(13,148,136,.15); }
div[data-testid="stButton"] button { border-radius: 8px; font-weight: 600; transition: transform .1s; }
div[data-testid="stButton"] button:hover { transform: translateY(-1px); }
div[data-testid="stTextArea"] textarea {
  border-radius: 10px; border-color: #c9e6e1; font-size: 14px; background: #fff;
}
button[kind="primary"] {
  background-color: #0d9488 !important; border-color: #0d9488 !important; color: #fff !important;
}
button[kind="primary"]:hover {
  background-color: #0f766e !important; border-color: #0f766e !important;
}
#MainMenu, footer { visibility: hidden; }
/* 오프라인 환경에서 Material Symbols 폰트 미로드 시 _arrow_right 텍스트 숨김 */
.material-symbols-rounded {
  font-size: 0 !important;
  width: 0 !important;
  overflow: hidden !important;
  display: inline-block !important;
}
section[data-testid="stSidebar"] { background: #f0faf8 !important; }
section[data-testid="stSidebar"] div[data-testid="stColumn"] div[data-testid="stButton"] button {
  border-radius: 50% !important;
  width: 34px !important;
  height: 34px !important;
  min-height: 34px !important;
  padding: 0 !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
"""


def inject_css():
    css = re.sub(r'/\*.*?\*/', '', _CSS, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css).strip()
    st.markdown(
        f'{_FONT}<style>{css}</style>',
        unsafe_allow_html=True,
    )
