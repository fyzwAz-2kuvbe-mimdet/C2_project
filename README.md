# 🎓 AI 학습 코치 플랫폼

초등 4학년~고등 3학년을 위한 AI 기반 맞춤형 학습 코칭 서비스입니다.
Google Gemini 2.5 Flash를 사용해 관심사 분석 → 자료 추천 → 뉴스 크롤링 → AI 첨삭까지 한 화면에서 완결됩니다.

## 주요 기능

| 단계 | 기능 |
|------|------|
| 1 | 관심사 입력 → Gemini AI가 탐구 심화 질문 3~5개 생성 |
| 2 | 답변 기반 학년·유형 맞춤 학습 자료 추천 (책/사이트/논문/영상) |
| 3 | 관련 최신 뉴스 헤드라인 + 링크 크롤링 (네이버) |
| 4 | 학습 결과물 제출 → 4유형 평가기준 AI 첨삭 |

## 빠른 시작

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. API 키 설정

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml`을 열고 실제 키를 입력합니다:

```toml
GEMINI_API_KEY = "AIza..."
```

> API 키는 [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료로 발급받을 수 있습니다.

### 3. 실행

```bash
cd study_coach
streamlit run app.py
```

## Streamlit Cloud 배포

1. GitHub에 업로드 (`.streamlit/secrets.toml`은 **절대 포함 금지** — `.gitignore`에 이미 등록됨)
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 **New app** 생성
3. **Settings → Secrets**에 아래 내용 추가:

```toml
GEMINI_API_KEY = "AIza..."
```

## 학습 유형 안내

| 유형 | 핵심 역량 |
|------|-----------|
| 🎯 하나고형 | 자기주도성 + 수학적 사고 |
| 🌏 민사고형 | 영어 서술 + 글로벌 맥락 |
| 🔬 과학고형 | 실험·탐구 + 수학 심화 |
| 📚 외고형   | 언어 활용 + 인문학적 확장 |

## 프로젝트 구조

```
study_coach/
├── app.py                      # Streamlit 엔트리포인트
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml             # Streamlit 테마
│   └── secrets.toml.example   # API 키 형식 예시
├── config/
│   └── learning_types.py      # 4유형 정의 + 평가기준
├── core/
│   ├── llm_client.py          # Gemini API 래퍼
│   ├── interest_diagnosis.py  # 관심사 진단 + 후속 질문
│   ├── resource_recommender.py # 학습자료 추천
│   ├── news_crawler.py        # 네이버 뉴스 크롤링
│   └── feedback_engine.py     # 첨삭 엔진
├── ui/
│   ├── styles.py              # CSS 주입 + 단계 인디케이터
│   ├── sidebar.py             # 학년·유형 선택
│   ├── step1_interest.py      # 관심사 입력 단계
│   ├── step2_resources.py     # 자료 추천 단계
│   ├── step3_news.py          # 뉴스 단계
│   └── step4_feedback.py      # 첨삭 단계
└── utils/
    ├── file_loader.py         # PDF/DOCX/TXT 파싱
    └── session.py             # 세션 상태 헬퍼 + 리포트 생성
```

## 기술 스택

- **UI**: Streamlit
- **LLM**: Google Gemini 2.5 Flash (`google-generativeai`)
- **뉴스 크롤링**: requests + BeautifulSoup4
- **파일 파싱**: pypdf, python-docx
