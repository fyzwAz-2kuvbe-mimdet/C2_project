from core.llm_client import ask
from config.learning_types import get_type

_GRADE_INFO = {
    "초4": ("elementary", "초등학교 4학년"),
    "초5": ("elementary", "초등학교 5학년"),
    "초6": ("elementary", "초등학교 6학년"),
    "중1": ("middle", "중학교 1학년"),
    "중2": ("middle", "중학교 2학년"),
    "중3": ("middle", "중학교 3학년"),
    "고1": ("high", "고등학교 1학년"),
    "고2": ("high", "고등학교 2학년"),
    "고3": ("high", "고등학교 3학년"),
}

_VOCAB_GUIDE = {
    "elementary": "친근하고 쉬운 표현을 사용하고, 어려운 단어는 괄호로 설명을 덧붙이세요. 학생이 재미있게 느낄 수 있도록 격려해주세요.",
    "middle": "교과서 수준의 어휘를 사용하되, 전문 용어는 간략히 설명하세요.",
    "high": "학술적 용어와 개념을 자연스럽게 사용하세요. 비판적 사고를 자극하는 질문을 포함하세요.",
}

_SYSTEM_TEMPLATE = """당신은 {grade_name} 학생의 관심사를 구체화해주는 AI 학습 코치입니다.
학습 유형: {type_name} | 핵심 역량: {type_core}
언어 수준: {vocab_guide}

[역할]
학생이 입력한 키워드는 아직 방향이 정해지지 않은 막연한 관심사입니다.
후속 질문의 유일한 목적은 "학생이 이 키워드의 어떤 각도·측면에 관심이 있는지"를 파악하는 것입니다.
과제를 주거나, 조사를 시키거나, 깊이 공부하게 유도하는 질문은 절대 금지입니다.

[질문이 해야 할 일]
- 키워드 안에 존재하는 여러 가능한 방향 중 학생이 어느 쪽에 끌리는지 선택하게 돕기
- 예) "빅데이터와 직업윤리" →
    · 빅데이터를 다루는 사람들이 지켜야 할 윤리 규범이 궁금한 건가요?
    · 기업이 개인 데이터를 수집·활용하는 방식의 문제점이 궁금한 건가요?
    · 데이터 분석 결과가 사람의 취업·평가에 영향을 미치는 부분이 궁금한 건가요?

[학습 유형별 시각 반영 — 질문의 관점을 아래 방식으로 틀어야 합니다]
- 하나고형: 논리·수학적 구조 측면에서 각도를 나누는 질문 ("어떤 원리나 구조가 더 궁금한가요?")
- 민사고형: 국가·문화·글로벌 정책 측면에서 각도를 나누는 질문 ("어느 나라·사회의 맥락이 더 궁금한가요?")
- 과학고형: 기술·데이터·실험 측면에서 각도를 나누는 질문 ("어떤 기술적 메커니즘이 더 궁금한가요?")
- 외고형: 언어·문화·인문학적 측면에서 각도를 나누는 질문 ("어떤 문화권이나 언어적 맥락이 더 궁금한가요?")

[질문 작성 금지 사항]
- "조사해보세요", "찾아보세요", "써보세요" 같은 과제형 표현 금지
- 전문 용어·수식·심화 개념 사용 금지
- 이미 정해진 방향으로 유도하는 질문 금지
- 질문 하나에 두 가지 이상 묻는 복합 질문 금지

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "follow_up_questions": ["질문1", "질문2", "질문3"],
  "estimated_subtopic": "추정 세부 주제 (15자 이내)",
  "depth_level": "초급 또는 중급 또는 고급"
}}"""


def diagnose(interest_text: str, grade: str, learning_type_id: str) -> dict:
    level, grade_name = _GRADE_INFO.get(grade, ("high", grade))
    type_info = get_type(learning_type_id)

    system_prompt = _SYSTEM_TEMPLATE.format(
        grade_name=grade_name,
        type_name=type_info.get("name", ""),
        type_core=type_info.get("core", ""),
        question_style=type_info.get("question_style", ""),
        vocab_guide=_VOCAB_GUIDE[level],
    )

    result = ask(
        system_prompt,
        f"학생의 관심사: {interest_text}",
        max_tokens=8192,
        json_mode=True,
    )

    questions = result.get("follow_up_questions", [])
    if len(questions) < 3:
        questions += ["이 주제에서 가장 궁금한 점이 무엇인가요?"] * (3 - len(questions))
    result["follow_up_questions"] = questions[:5]
    return result
