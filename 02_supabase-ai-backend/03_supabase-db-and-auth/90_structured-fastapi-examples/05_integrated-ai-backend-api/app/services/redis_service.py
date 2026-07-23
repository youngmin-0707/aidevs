# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""Upstash Redis helper입니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os
# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from urllib.parse import quote

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import httpx
# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.


# 학습 포인트: TTL_SECONDS 변수에 오른쪽에서 만든 값을 저장합니다.
TTL_SECONDS = 60


# 학습 포인트: redis_command 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def redis_command(*parts: str) -> dict:
    """Upstash Redis REST API로 Redis 명령을 실행합니다.

    예: redis_command("get", "key")는 Redis의 GET key 명령과 같습니다.
    Upstash REST API는 Redis 명령을 URL 경로 형태로 보낼 수 있습니다.
    """

    # 학습 포인트: rest_url 변수에 오른쪽에서 만든 값을 저장합니다.
    rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
    # 학습 포인트: rest_token 변수에 오른쪽에서 만든 값을 저장합니다.
    rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not rest_url:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=500, detail="UPSTASH_REDIS_REST_URL이 없습니다. .env 파일을 확인하세요.")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not rest_token:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=500, detail="UPSTASH_REDIS_REST_TOKEN이 없습니다. .env 파일을 확인하세요.")
    # 질문에는 한글이나 공백이 들어갈 수 있으므로 URL-safe하게 인코딩합니다.
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


# 학습 포인트: get_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_answer(key: str) -> str | None:
    """Redis에서 캐시된 답변을 조회합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return redis_command("get", key).get("result")


# 학습 포인트: set_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def set_answer(key: str, answer: str) -> None:
    """답변을 Redis에 TTL과 함께 저장합니다.

    ex 옵션은 초 단위 만료 시간입니다.
    현재 예제에서는 60초가 지나면 같은 질문 캐시가 자동으로 사라집니다.
    """

    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    redis_command("set", key, answer, "ex", str(TTL_SECONDS))
