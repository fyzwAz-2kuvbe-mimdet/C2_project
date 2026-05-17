import json
import streamlit as st

from core.llm_client import _extract_json, ask


def _done_key(result_key: str) -> str:
    return f"_done_{result_key}"


def is_done(result_key: str) -> bool:
    return st.session_state.get(_done_key(result_key), False)


def reset_result(result_key: str):
    st.session_state[result_key] = None
    st.session_state[_done_key(result_key)] = False


def prompt_panel(
    system: str,
    prompt: str,
    result_key: str,
    *,
    json_mode: bool = True,
    spinner_text: str = "AI가 분석 중이에요...",
    btn_label: str = "AI에게 전송하기",
) -> bool:
    """
    Dual-mode AI panel (오프라인 Ollama 버전).
    - Tab 1: Gemma (Ollama) 자동 전송.
    - Tab 2: 프롬프트 복사 후 수동 붙여넣기.
    """
    if is_done(result_key):
        return True

    show_key = f"_show_{result_key}"
    if show_key not in st.session_state:
        st.session_state[show_key] = False
    if st.button("프롬프트 보기 / 숨기기", key=f"_toggle_{result_key}"):
        st.session_state[show_key] = not st.session_state[show_key]
    if st.session_state[show_key]:
        st.caption("아래 내용을 복사해서 다른 AI에도 사용할 수 있어요.")
        st.code(prompt, language="text")

    tab_auto, tab_manual = st.tabs(["Gemma 자동 전송 (로컬)", "직접 붙여넣기"])

    with tab_auto:
        st.caption("로컬 Gemma 모델이 자동으로 분석합니다.")
        if st.button(btn_label, key=f"_auto_{result_key}", type="primary", use_container_width=True):
            with st.spinner(spinner_text):
                try:
                    result = ask(system, prompt, json_mode=json_mode)
                    st.session_state[result_key] = result
                    st.session_state[_done_key(result_key)] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"AI 오류: {e}")

    with tab_manual:
        st.caption("프롬프트를 복사해서 원하는 AI에 붙여넣기 후 응답을 아래에 입력하세요.")
        manual = st.text_area(
            "AI 응답",
            height=220,
            key=f"_manual_{result_key}",
            placeholder="AI의 응답을 여기에 붙여넣으세요...",
            label_visibility="collapsed",
        )
        if st.button("결과 적용하기", key=f"_apply_{result_key}", type="primary", use_container_width=True):
            if manual.strip():
                try:
                    parsed = json.loads(_extract_json(manual)) if json_mode else manual.strip()
                    st.session_state[result_key] = parsed
                    st.session_state[_done_key(result_key)] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"형식 오류: {e} — JSON 형식인지 확인하거나 AI 자동 전송을 이용해주세요.")
            else:
                st.warning("AI 응답을 입력해주세요.")

    return False
