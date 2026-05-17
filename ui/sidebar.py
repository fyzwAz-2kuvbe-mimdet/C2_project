import streamlit as st
from config.learning_types import get_all_types

_GRADES = ["초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"]
_STEP_NAMES = {
    1: "관심구체화", 2: "주제추천",  3: "로드맵",
    4: "자료탐색",  5: "트렌드",    6: "회고·계획",
    7: "초록생성",  8: "글쓰기",    9: "지식지도",  10: "교과연결",
}
_PHASES = [
    ("Phase 1", "#0d9488", [1, 2]),
    ("Phase 2", "#0891b2", [3, 4, 5]),
    ("Phase 3", "#059669", [6, 7, 8]),
    ("Phase 4", "#0a5c52", [9, 10]),
]
_TYPE_ORDER = ["hana", "sciencehigh", "minsa", "foreign"]


def render_sidebar():
    st.markdown(
        "<div style='font-size:20px;font-weight:800;color:#0a5c52;margin-bottom:2px;'>AI 학습 멘토</div>"
        "<div style='font-size:12px;color:#4b7772;margin-bottom:12px;'>10단계 탐구 멘토링</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── 학습 유형 선택 ──
    _render_type_selector()
    st.divider()

    # ── 학년 ──
    st.markdown("**학년**")
    grade = st.selectbox("학년", _GRADES,
                         index=_GRADES.index(st.session_state.get("grade", "고1")),
                         label_visibility="collapsed")
    if grade != st.session_state.get("grade"):
        st.session_state.grade = grade

    # ── 현재 탐구 주제 ──
    selected = st.session_state.get("selected_topic") or {}
    if selected.get("name"):
        st.divider()
        st.markdown("**탐구 주제**")
        st.markdown(
            f'<div style="background:#e8f5f3;border:1px solid #0d9488;border-radius:8px;'
            f'padding:8px 12px;font-size:13px;font-weight:700;color:#0a5c52;">'
            f'{selected["name"]}</div>',
            unsafe_allow_html=True,
        )
        hook = selected.get("hook", "")
        if hook:
            st.markdown(
                f'<div style="font-size:11px;color:#4b7772;margin-top:4px;">{hook}</div>',
                unsafe_allow_html=True,
            )

    st.divider()

    # ── 단계 이동 ──
    current = st.session_state.get("current_step", 1)
    st.markdown("**단계 이동**")
    _render_phase_labels()
    _render_step_buttons(current, 1, 5)
    _render_step_buttons(current, 6, 10)

    st.divider()

    # ── 진행 상태 ──
    st.markdown(
        f"<div style='font-size:12px;color:#6b7280;'>"
        f"현재: <strong style='color:#0a5c52;'>{current}단계 — {_STEP_NAMES[current]}</strong></div>",
        unsafe_allow_html=True,
    )
    if current > 1:
        if st.button("처음부터 다시", use_container_width=True):
            from utils.session import reset_all
            reset_all()
            st.rerun()


def _render_type_selector():
    all_types = get_all_types()
    current = st.session_state.get("learning_type", "hana")

    st.markdown("**목표 유형**")
    for tid in _TYPE_ORDER:
        t = all_types[tid]
        is_sel = tid == current

        st.markdown(
            f"<style>"
            f".element-container:has(#type-{tid}) + .element-container button{{"
            f"  border-left:5px solid #0d9488 !important;"
            f"  border-radius:0 8px 8px 0 !important;"
            f"  white-space:pre-line !important;"
            f"  text-align:left !important;"
            f"  height:auto !important;"
            f"  min-height:64px !important;"
            f"  padding:10px 14px !important;"
            f"  line-height:1.5 !important;"
            f"  font-size:13px !important;"
            f"  font-weight:400 !important;"
            f"}}"
            f"</style>"
            f'<span id="type-{tid}"></span>',
            unsafe_allow_html=True,
        )
        label = f"{t['name']}  |  {t['core']}\n{t['description']}"
        if st.button(label, key=f"_type_{tid}", use_container_width=True,
                     type="primary" if is_sel else "secondary"):
            st.session_state.learning_type = tid
            st.rerun()


def _render_phase_labels():
    parts = []
    for name, color, steps in _PHASES:
        flex = len(steps)
        parts.append(
            f'<div style="flex:{flex};text-align:center;font-size:9px;font-weight:700;'
            f'color:{color};border-bottom:2px solid {color};padding-bottom:3px;'
            f'white-space:nowrap;overflow:hidden;">{name}</div>'
        )
    html = f'<div style="display:flex;gap:2px;margin-bottom:6px;">{"".join(parts)}</div>'
    st.markdown(html, unsafe_allow_html=True)


def _render_step_buttons(current: int, start: int, end: int):
    cols = st.columns(end - start + 1)
    for i, col in enumerate(cols):
        sn = start + i
        done = sn < current
        active = sn == current
        lbl = "✓" if done else str(sn)
        btn_type = "primary" if active else "secondary"
        with col:
            if st.button(
                lbl,
                key=f"_nav_{sn}",
                type=btn_type,
                use_container_width=True,
                help=f"{sn}. {_STEP_NAMES[sn]}",
            ):
                st.session_state.current_step = sn
                st.rerun()
