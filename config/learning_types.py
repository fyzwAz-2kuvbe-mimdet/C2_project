LEARNING_TYPES = {
    "hana": {
        "name": "하나고형",
        "core": "자기주도성 + 수학적 사고",
        "description": "스스로 질문을 만들고 수학·논리로 파고드는 탐구형",
        "color": "#3b82f6",
        "icon": "🎯",
        "evaluation_criteria": [
            {"key": "self_directed", "label": "교과 외 영역을 스스로 찾아 탐구했는가", "weight": 25},
            {"key": "math_logic", "label": "수학적/논리적 원리까지 도달했는가", "weight": 25},
            {"key": "specificity", "label": "구체적 개념명을 적시했는가", "weight": 25},
            {"key": "limit_awareness", "label": "한계 인식 및 확장 의지가 보이는가", "weight": 25},
        ],
        "extra_resources": "관련 수학·과학 경시 문제 및 올림피아드 자료",
        "preferred_sources": ["대학 공개강의", "교과서 심화", "수학/과학 저널"],
    },
    "minsa": {
        "name": "민사고형",
        "core": "영어 서술 + 글로벌 맥락",
        "description": "글로벌 시각으로 인문·사회를 탐구하는 세계시민형",
        "color": "#8b5cf6",
        "icon": "🌏",
        "evaluation_criteria": [
            {"key": "global_context", "label": "글로벌 맥락에서 이슈를 이해했는가", "weight": 25},
            {"key": "english_usage", "label": "영어 자료를 활용·인용했는가", "weight": 25},
            {"key": "multi_perspective", "label": "다양한 관점을 비교·분석했는가", "weight": 25},
            {"key": "proposal", "label": "해결책 또는 자신의 입장을 제시했는가", "weight": 25},
        ],
        "extra_resources": "관련 영문 기사(BBC/NYT) 및 TED 강연 추천",
        "preferred_sources": ["해외 학술지", "TED Talks", "글로벌 뉴스(BBC/NYT)", "국제기구 보고서"],
    },
    "sciencehigh": {
        "name": "과학고형",
        "core": "실험·탐구 + 수학 심화",
        "description": "실험 설계와 데이터 분석으로 과학적 진실을 파고드는 연구자형",
        "color": "#10b981",
        "icon": "🔬",
        "evaluation_criteria": [
            {"key": "hypothesis", "label": "가설을 세우고 검증 방법을 제안했는가", "weight": 25},
            {"key": "data_analysis", "label": "데이터/수치를 근거로 결론을 도출했는가", "weight": 25},
            {"key": "advanced_math", "label": "심화 수학 개념을 적용했는가", "weight": 25},
            {"key": "originality", "label": "기존 연구와 차별화된 시각이 있는가", "weight": 25},
        ],
        "extra_resources": "관련 실험 사례, 논문 초록 및 KISTEP 보고서",
        "preferred_sources": ["arXiv", "PubMed", "사이언스 저널", "KISTEP 보고서"],
    },
    "foreign": {
        "name": "외고형",
        "core": "언어 활용 + 인문학적 확장",
        "description": "언어와 문화를 연결해 인문학적 통찰을 이끌어내는 스토리텔러형",
        "color": "#f59e0b",
        "icon": "📚",
        "evaluation_criteria": [
            {"key": "linguistic_insight", "label": "언어적 특성을 분석·활용했는가", "weight": 25},
            {"key": "cultural_context", "label": "문화적 맥락과 연결지었는가", "weight": 25},
            {"key": "humanities_depth", "label": "인문학적 개념(역사/철학/문학)을 연결했는가", "weight": 25},
            {"key": "narrative", "label": "논리적이고 설득력 있는 서술인가", "weight": 25},
        ],
        "extra_resources": "관련 인문·사회 칼럼 및 문화비평 자료",
        "preferred_sources": ["인문학 도서", "언어학 저널", "문화비평 매체", "외국어 원전"],
    },
}


def get_type(type_id: str) -> dict:
    return LEARNING_TYPES.get(type_id, {})


def get_all_types() -> dict:
    return LEARNING_TYPES


def get_criteria(type_id: str) -> list:
    return LEARNING_TYPES.get(type_id, {}).get("evaluation_criteria", [])
