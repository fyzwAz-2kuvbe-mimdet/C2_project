import json
import re
import time

import ollama
import streamlit as st

# ── 모델 설정 ──────────────────────────────────────────
MODEL = "gemma4"          # ollama pull gemma4
_MAX_RETRIES = 3          # JSON 파싱 실패 시 재시도 횟수
_RETRY_DELAY = 2.0        # 재시도 간격(초)


def check_ollama_connection() -> tuple[bool, str]:
    """Ollama 서버 + 모델 존재 여부 확인. (bool, 메시지) 반환."""
    try:
        models = ollama.list()
        names = [m.model for m in models.models]
        # "gemma4", "gemma4:latest" 등 prefix 매칭
        matched = any(n == MODEL or n.startswith(MODEL + ":") for n in names)
        if not matched:
            available = ", ".join(names) if names else "(없음)"
            return False, (
                f"모델 **{MODEL}** 이 Ollama에 없습니다.\n\n"
                f"터미널에서 `ollama pull {MODEL}` 을 실행하세요.\n\n"
                f"설치된 모델: {available}"
            )
        return True, "ok"
    except Exception as e:
        return False, (
            f"Ollama 서버에 연결할 수 없습니다.\n\n"
            f"터미널에서 `ollama serve` 를 실행한 뒤 새로고침하세요.\n\n"
            f"오류: {e}"
        )


def ask(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 8192,
    json_mode: bool = False,
) -> str | dict | list:
    """Ollama Gemma 모델에 요청. json_mode=True 면 dict/list 반환."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_message},
    ]
    options = {"num_predict": max_tokens, "temperature": 0.7}

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = ollama.chat(
                model=MODEL,
                messages=messages,
                format="json" if json_mode else "",
                options=options,
            )
            content = response["message"]["content"]

            if not json_mode:
                return content

            # JSON 파싱 시도
            try:
                return json.loads(_extract_json(content))
            except json.JSONDecodeError:
                if attempt < _MAX_RETRIES:
                    st.toast(f"JSON 형식 오류 — 재시도 중... ({attempt}/{_MAX_RETRIES})")
                    time.sleep(_RETRY_DELAY)
                    continue
                raise ValueError(
                    f"모델이 올바른 JSON을 반환하지 않았습니다.\n\n"
                    f"원본 응답:\n{content[:500]}"
                )

        except ValueError:
            raise
        except Exception as e:
            if attempt < _MAX_RETRIES:
                st.toast(f"오류 발생, 재시도 중... ({attempt}/{_MAX_RETRIES}): {e}")
                time.sleep(_RETRY_DELAY)
            else:
                raise


def _extract_json(text: str) -> str:
    """응답에서 JSON 블록만 추출 (마크다운 코드블록 제거 등)."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    for start, end in [("{", "}"), ("[", "]")]:
        s = text.find(start)
        e = text.rfind(end)
        if s != -1 and e != -1 and e > s:
            candidate = text[s: e + 1]
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                continue
    return text
