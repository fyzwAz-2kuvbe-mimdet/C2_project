import streamlit as st

_STEPS = {
    1: "관심구체화", 2: "주제추천",  3: "로드맵",
    4: "자료탐색",  5: "트렌드",    6: "회고·계획",
    7: "초록생성",  8: "글쓰기",    9: "지식지도",  10: "교과연결",
}

_PHASES = [
    (1, "Phase 1 진단", [1, 2]),
    (2, "Phase 2 학습", [3, 4, 5]),
    (3, "Phase 3 탐구", [6, 7, 8]),
    (4, "Phase 4 성찰", [9, 10]),
]

_PC = {1: "#0d9488", 2: "#0891b2", 3: "#059669", 4: "#0a5c52"}
_STEP_PC = {s: _PC[pn] for pn, _, steps in _PHASES for s in steps}

STEP_W = 52   # px — each step cell width
CONN_W = 18   # px — connector cell width


def render_progress(current_step: int):
    ph_row: list[str] = []
    data_row: list[str] = []

    for idx, (pn, pname, psteps) in enumerate(_PHASES):
        pc = _PC[pn]
        done_ph  = current_step > max(psteps)
        active_ph = min(psteps) <= current_step <= max(psteps)
        ph_c = "#10b981" if done_ph else (pc if active_ph else "#d1d5db")

        span = 2 * len(psteps) - 1
        ph_row.append(
            f'<td colspan="{span}" style="border:0;text-align:center;padding:0 0 6px;'
            f'border-bottom:2px solid {ph_c} !important;font-size:9px;font-weight:700;'
            f'color:{ph_c};white-space:nowrap;letter-spacing:.03em;">{pname}</td>'
        )

        for i, sn in enumerate(psteps):
            name = _STEPS[sn]
            done   = sn < current_step
            active = sn == current_step

            if done:
                cbg, cfg, ct = "#10b981", "#fff", "✓"
                lc, lw = "#10b981", "600"
                shadow = "filter:drop-shadow(0 1px 3px #10b98155);"
            elif active:
                cbg, cfg, ct = pc, "#fff", str(sn)
                lc, lw = pc, "700"
                shadow = f"box-shadow:0 0 0 4px {pc}28;"
            else:
                cbg, cfg, ct = "#f3f4f6", "#9ca3af", str(sn)
                lc, lw = "#9ca3af", "400"
                shadow = ""

            circle = (
                f'<div style="width:34px;height:34px;border-radius:50%;'
                f'background:{cbg};color:{cfg};{shadow}'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-size:13px;font-weight:700;margin:0 auto;">{ct}</div>'
            )
            label = (
                f'<div style="font-size:9px;color:{lc};font-weight:{lw};'
                f'white-space:nowrap;text-align:center;margin-top:5px;">{name}</div>'
            )

            inner = circle + label

            data_row.append(
                f'<td style="border:0;width:{STEP_W}px;padding:8px 4px 10px;'
                f'text-align:center;vertical-align:top;">{inner}</td>'
            )

            # Within-phase connector
            if i < len(psteps) - 1:
                nxt = psteps[i + 1]
                cline = "#10b981" if nxt <= current_step else "#e5e7eb"
                data_row.append(
                    f'<td style="border:0;width:{CONN_W}px;padding:0;vertical-align:middle;">'
                    f'<div style="height:2px;background:{cline};"></div></td>'
                )

        # Phase-boundary connector
        if idx < len(_PHASES) - 1:
            next_first = _PHASES[idx + 1][2][0]
            cline = "#10b981" if next_first <= current_step else "#e5e7eb"
            data_row.append(
                f'<td style="border:0;width:{CONN_W}px;padding:0;vertical-align:middle;">'
                f'<div style="height:2px;background:{cline};'
                f'border-left:4px solid #fafafa;border-right:4px solid #fafafa;"></div></td>'
            )
            ph_row.append(
                f'<td style="border:0;border-bottom:2px solid #e5e7eb !important;'
                f'width:{CONN_W}px;padding:0 0 6px;"></td>'
            )

    html = (
        '<div style="background:#f0faf8;border-bottom:1px solid #c9e6e1;'
        'padding:12px 0 0;margin-bottom:20px;overflow-x:auto;">'
        '<table cellspacing="0" cellpadding="0" '
        'style="border-collapse:collapse;border:0;margin:0 auto;">'
        f'<tr>{"".join(ph_row)}</tr>'
        f'<tr>{"".join(data_row)}</tr>'
        '</table></div>'
    )
    st.markdown(html, unsafe_allow_html=True)
