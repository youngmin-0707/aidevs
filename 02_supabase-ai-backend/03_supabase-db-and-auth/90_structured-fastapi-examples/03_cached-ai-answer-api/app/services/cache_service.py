# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""Gemini AI 답변을 Upstash Redis에 캐시합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os
# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from urllib.parse import quote

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import httpx
# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException, status

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.gemini import get_gemini_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.cache_schema import CachedAnswerResponse


# 학습 포인트: TTL_SECONDS 변수에 오른쪽에서 만든 값을 저장합니다.
TTL_SECONDS = 600


# 학습 포인트: redis_command 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def redis_command(*parts: str) -> dict:
    """Upstash Redis REST API로 Redis 명령을 실행합니다.

    예: redis_command("get", "my-key")는 Redis의 GET my-key와 같은 의미입니다.
    """

    # 학습 포인트: rest_url 변수에 오른쪽에서 만든 값을 저장합니다.
    rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
    # 학습 포인트: rest_token 변수에 오른쪽에서 만든 값을 저장합니다.
    rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not rest_url:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UPSTASH_REDIS_REST_URL이 없습니다. .env 파일을 확인하세요.",
        )

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not rest_token:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UPSTASH_REDIS_REST_TOKEN이 없습니다. .env 파일을 확인하세요.",
        )

    # key나 value에 한글, 공백, 특수문자가 있어도 URL이 깨지지 않도록 인코딩합니다.
    # 학습 포인트: encoded 변수에 오른쪽에서 만든 값을 저장합니다.
    encoded = [quote(part, safe="") for part in parts]
    # 학습 포인트: url 변수에 오른쪽에서 만든 값을 저장합니다.
    url = f"{rest_url.rstrip('/')}/{'/'.join(encoded)}"
    # 학습 포인트: headers 변수에 오른쪽에서 만든 값을 저장합니다.
    headers = {"Authorization": f"Bearer {rest_token}"}

    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = httpx.get(url, headers=headers, timeout=10)
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        response.raise_for_status()
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except httpx.HTTPError as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"Redis 호출 실패: {error}") from error

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return response.json()


# 학습 포인트: cache_key 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def cache_key(question: str) -> str:
    """질문 문자열을 Redis key로 변환합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return f"ex90:answer:{question}"


# 학습 포인트: create_gemini_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def create_gemini_answer(question: str) -> str:
    """Gemini SDK로 답변을 만듭니다."""

    # 학습 포인트: model 변수에 오른쪽에서 만든 값을 저장합니다.
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_gemini_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.models.generate_content(model=model, contents=question)
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"Gemini 호출 실패: {error}") from error

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return response.text or ""


# 학습 포인트: get_or_create_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_or_create_answer(question: str) -> CachedAnswerResponse:
    """Redis에 답변이 있으면 재사용하고, 없으면 새 답변을 만들어 저장합니다."""

    # 학습 포인트: key 변수에 오른쪽에서 만든 값을 저장합니다.
    key = cache_key(question)
    # 학습 포인트: cached_result 변수에 처리하거나 조회한 결과를 저장합니다.
    cached_result = redis_command("get", key)
    # 학습 포인트: cached_answer 변수에 오른쪽에서 만든 값을 저장합니다.
    cached_answer = cached_result.get("result")

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if cached_answer:
        # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
        return CachedAnswerResponse(
            question=question,
            answer=cached_answer,
            cached=True,
            ttl_seconds=TTL_SECONDS,
        )

    # 학습 포인트: answer 변수에 오른쪽에서 만든 값을 저장합니다.
    answer = create_gemini_answer(question)
    # ex 옵션은 TTL(Time To Live)을 초 단위로 설정합니다.
    # 여기서는 60초 뒤 캐시가 자동 삭제됩니다.
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    redis_command("set", key, answer, "ex", str(TTL_SECONDS))
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return CachedAnswerResponse(
        question=question,
        answer=answer,
        cached=False,
        ttl_seconds=TTL_SECONDS,
    )


# 학습 포인트: clear_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def clear_answer(question: str) -> int:
    """특정 질문에 해당하는 Redis 캐시 key를 삭제합니다."""

    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = redis_command("del", cache_key(question))
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return int(result.get("result", 0))
