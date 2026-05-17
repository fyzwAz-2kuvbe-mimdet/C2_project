import streamlit as st

st.set_page_config(
    page_title="AI 학습 멘토 (오프라인)",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import inject_css
from ui.progress import render_progress
from ui.sidebar import render_sidebar
from ui.step01_type_grade import render as step01
from ui.step02_interest_input import render as step02
from ui.step03_follow_up import render as step03
from ui.step04_roadmap_view import render as step04
from ui.step05_resource_view import render as step05
from ui.step06_news_view import render as step06
from ui.step07_question_view import render as step07
from ui.step08_upload import render as step08
from ui.step09_feedback_view import render as step09
from ui.step10_summary import render as step10
from utils.session import init_session
from core.llm_client import check_ollama_connection

inject_css()

# ── Ollama 연결 확인 ────────────────────────────────────
ok, msg = check_ollama_connection()
if not ok:
    st.error("Ollama 연결 오류")
    st.markdown(msg)
    st.info(
        "**설치 방법**\n"
        "1. https://ollama.com 에서 Ollama 설치\n"
        "2. 터미널: `ollama pull gemma4`\n"
        "3. 터미널: `ollama serve` (별도 창에서 실행)\n"
        "4. 이 페이지 새로고침"
    )
    st.stop()

init_session()

# ── Progress bar 클릭 → 단계 이동 ──────────────────────
_nav = st.query_params.get("nav_to")
if _nav is not None:
    try:
        _target = int(_nav)
        if 1 <= _target <= 10:
            st.session_state.current_step = _target
    except (ValueError, TypeError):
        pass
    st.query_params.clear()
    st.rerun()

with st.sidebar:
    render_sidebar()

step = st.session_state.get("current_step", 1)
render_progress(step)

_STEPS = {
    1: step01, 2: step02, 3: step03, 4: step04, 5: step05,
    6: step06, 7: step07, 8: step08, 9: step09, 10: step10,
}
_STEPS.get(step, step01)()
