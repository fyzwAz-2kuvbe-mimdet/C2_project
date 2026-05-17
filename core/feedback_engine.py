from core.llm_client import ask
from config.learning_types import get_type, get_criteria

_GRADE_STYLE = {
    "초": "초등학생이므로 격려와 칭찬 위주로 평가하되, 개선점은 매우 쉽고 친절하게 설명하세요.",
    "중": "중학생 수준의 기대치로 평가하고, 구체적인 개선 방법을 제시하세요.",
    "고": "고등학생 수준의 냉정하고 객관적인 평가를 제공하고, 대입·자소서에 도움이 되는 구체적 조언을 하세요.",
}

_SYSTEM_TEMPLATE = """당신은 {type_name} 유형의 학습 결과물을 평가하는 전문 첨삭 선생님입니다.
핵심 역량: {type_core}
평가 대상: {grade} 학생
평가 스타일: {style_guide}

[평가 기준 — 각 0~10점]
{criteria_text}

[출력 규칙]
- rewrite_suggestions는 원문에서 실제 인용 가능한 문장으로 최대 3개 제시하세요.
- 원문이 짧으면 rewrite_suggestions를 빈 배열로 두세요.
- 반드시 아래 JSON 형식으로만 응답하세요.

{{
  "overall_score": 1~10 사이 정수,
  "criteria_scores": {{{criteria_keys_placeholder}}},
  "strengths": ["구체적 강점1", "구체적 강점2", "구체적 강점3"],
  "weaknesses": ["구체적 약점1", "구체적 약점2", "구체적 약점3"],
  "rewrite_suggestions": [
    {{"before": "원문 일부", "after": "개선안", "reason": "이유"}}
  ],
  "next_step": "다음 학습 방향 한 단락 (100~200자)"
}}"""


def analyze(student_text: str, learning_type_id: str, grade: str) -> dict:
    type_info = get_type(learning_type_id)
    criteria = get_criteria(learning_type_id)

    grade_prefix = grade[:1]
    style_guide = _GRADE_STYLE.get(grade_prefix, _GRADE_STYLE["고"])

    criteria_text = "\n".join(
        f"- [{c['key']}] {c['label']} (가중치: {c['weight']}%)" for c in criteria
    )
    criteria_keys_placeholder = ", ".join(f'"{c["key"]}": 점수' for c in criteria)

    system_prompt = _SYSTEM_TEMPLATE.format(
        type_name=type_info.get("name", ""),
        type_core=type_info.get("core", ""),
        grade=grade,
        style_guide=style_guide,
        criteria_text=criteria_text,
        criteria_keys_placeholder=criteria_keys_placeholder,
    )

    return ask(
        system_prompt,
        f"학생 제출 글:\n\n{student_text}",
        max_tokens=8192,
        json_mode=True,
    )
