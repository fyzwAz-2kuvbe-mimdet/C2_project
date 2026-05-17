from core.llm_client import ask
from config.learning_types import get_type

_GRADE_NAMES = {
    "초4": "초등학교 4학년 (만 9-10세)",
    "초5": "초등학교 5학년 (만 10-11세)",
    "초6": "초등학교 6학년 (만 11-12세)",
    "중1": "중학교 1학년 (만 13세)",
    "중2": "중학교 2학년 (만 14세)",
    "중3": "중학교 3학년 (만 15세)",
    "고1": "고등학교 1학년 (만 16세)",
    "고2": "고등학교 2학년 (만 17세)",
    "고3": "고등학교 3학년 (만 18세)",
}

_SYSTEM_TEMPLATE = """당신은 {grade_name} 학생을 위한 학습 자료 추천 전문가입니다.
학습 유형: {type_name} — {type_core}
선호 자료 유형: {preferred}

[규칙]
- 학생의 답변에서 드러난 관심 방향과 키워드를 최우선으로 반영하세요.
- 처음 공부하는 입문자도 바로 시작할 수 있는 쉬운 자료를 반드시 포함하세요.
- 학생 학년에 맞는 난이도의 자료만 추천하세요. 너무 어렵거나 쉬운 자료는 제외하세요.
- 실제로 존재하는 자료만 추천하세요. 가짜 URL을 절대 생성하지 마세요.
- URL을 알 수 없으면 "저자명, 출판사, 출판연도" 형태의 출판 정보를 제공하세요.
- 5~8개의 다양한 유형(책/사이트/논문/영상) 자료를 추천하세요.
- 입문 자료를 먼저, 심화·전문 자료를 나중에 배치하세요.

반드시 아래 JSON 배열 형식으로만 응답하세요:
[
  {{
    "title": "자료 제목 (실제 존재하는 책·논문·채널명)",
    "type": "책 또는 사이트 또는 논문 또는 영상",
    "level": "입문 또는 심화 또는 전문",
    "source_url": "사이트는 실제 URL / 책은 저자명+출판사 / 논문은 저자명+저널명+연도 / 영상은 채널명 또는 URL",
    "why": "왜 이 자료가 학생에게 도움이 되는지 한 줄 (40자 이내)",
    "duration": "예상 학습 시간 (예: 2-3시간, 1주일)"
  }}
]

[추가 주의사항]
- 책·논문은 실제로 출판된 것만 추천하세요. 제목을 지어내지 마세요.
- 논문 제목은 검색하면 나오는 실제 논문 제목으로 적으세요.
- 확실하지 않은 자료는 추천 목록에서 제외하고 사이트·영상으로 대체하세요."""


def recommend(
    refined_interest: str, grade: str, learning_type_id: str, answers: dict
) -> list:
    grade_name = _GRADE_NAMES.get(grade, grade)
    type_info = get_type(learning_type_id)
    preferred = ", ".join(type_info.get("preferred_sources", []))

    answers_text = "\n".join(
        f"Q: {q}\nA: {a}" for q, a in answers.items() if a.strip()
    )

    system_prompt = _SYSTEM_TEMPLATE.format(
        grade_name=grade_name,
        type_name=type_info.get("name", ""),
        type_core=type_info.get("core", ""),
        preferred=preferred,
    )

    user_message = f"관심 주제: {refined_interest}\n\n학생 답변:\n{answers_text}"

    result = ask(system_prompt, user_message, max_tokens=8192, json_mode=True)

    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        for key in ("resources", "items", "data"):
            if key in result and isinstance(result[key], list):
                return result[key]
    return []
