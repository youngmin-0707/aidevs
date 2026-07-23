# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""Gemini 답변 생성, Redis 캐시, Supabase 로그 저장을 연결합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from dataclasses import dataclass
# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import httpx
# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.gemini import get_gemini_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.auth_schema import UserPublic
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatLogPublic, ChatRequest, ChatResponse
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import redis_service


# 학습 포인트: TABLE_NAME 변수에 오른쪽에서 만든 값을 저장합니다.
TABLE_NAME = "ex90_user_chat_logs"


# 학습 포인트: 아래 함수나 클래스에 추가 동작을 적용하는 데코레이터입니다.
@dataclass(frozen=True)
# 학습 포인트: AnswerResult 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class AnswerResult:
    """AI 답변 생성 결과를 한 묶음으로 전달하기 위한 작은 데이터 클래스입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    answer: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    provider: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    model: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    actual_api_called: bool


# 학습 포인트: table_url 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def table_url() -> str:
    """Supabase REST API에서 채팅 로그 테이블을 호출할 URL을 만듭니다."""

    # 학습 포인트: supabase_url 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase_url = os.getenv("SUPABASE_URL")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not supabase_url:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=500, detail="SUPABASE_URL이 없습니다. .env 파일을 확인하세요.")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return f"{supabase_url.rstrip('/')}/rest/v1/{TABLE_NAME}"


# 학습 포인트: service_headers 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def service_headers() -> dict[str, str]:
    """service role key로 Supabase REST API를 호출할 때 사용하는 헤더입니다.

    service role key는 RLS를 우회할 수 있는 서버 전용 key입니다.
    따라서 이 헤더는 FastAPI 서버 안에서만 사용하고 프론트엔드로 보내면 안 됩니다.
    """

    # 학습 포인트: service_role_key 변수에 오른쪽에서 만든 값을 저장합니다.
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not service_role_key:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=500, detail="SUPABASE_SERVICE_ROLE_KEY가 없습니다. .env 파일을 확인하세요.")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


# 학습 포인트: user_headers 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def user_headers(access_token: str | None) -> dict[str, str]:
    """사용자 access token으로 Supabase REST API를 호출할 때 사용하는 헤더입니다.

    apikey에는 anon key를 넣고 Authorization에는 사용자 access token을 넣습니다.
    이 방식으로 조회하면 Supabase RLS가 auth.uid()를 기준으로 적용됩니다.
    """

    # 학습 포인트: anon_key 변수에 오른쪽에서 만든 값을 저장합니다.
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not anon_key:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=500, detail="SUPABASE_ANON_KEY가 없습니다. .env 파일을 확인하세요.")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not access_token:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=401, detail="Bearer token이 없습니다.")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "apikey": anon_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


# 학습 포인트: cache_key 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def cache_key(user_id: str, message: str) -> str:
    """사용자별/질문별 Redis cache key를 만듭니다.

    user_id를 포함해야 서로 다른 사용자가 같은 질문을 해도 캐시가 섞이지 않습니다.
    """

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return f"ex90:chat:{user_id}:{message}"


# 학습 포인트: create_gemini_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def create_gemini_answer(message: str) -> AnswerResult:
    """Gemini SDK로 답변을 만듭니다."""

    # 학습 포인트: model 변수에 오른쪽에서 만든 값을 저장합니다.
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_gemini_client()
    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.models.generate_content(
        model=model,
        contents=message,
    )
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return AnswerResult(
        answer=response.text or "",
        provider="gemini",
        model=model,
        actual_api_called=True,
    )


# 학습 포인트: create_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def create_answer(message: str) -> AnswerResult:
    """Gemini 답변을 생성합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return create_gemini_answer(message)


# 학습 포인트: insert_log 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def insert_log(
    user: UserPublic,
    request: ChatRequest,
    answer: str | None,
    cached: bool,
    provider: str,
    model: str,
    actual_api_called: bool,
    status: str = "success",
    error_message: str | None = None,
) -> str | None:
    """채팅 처리 결과를 Supabase 로그 테이블에 저장합니다.

    저장은 service role key로 수행합니다.
    이 예제에서는 FastAPI가 먼저 Bearer token을 검증한 뒤,
    검증된 user.id를 user_id 컬럼에 넣어 저장합니다.
    """

    # 학습 포인트: payload 변수에 오른쪽에서 만든 값을 저장합니다.
    payload = {
        "user_id": user.id,
        "user_message": request.message,
        "assistant_message": answer,
        "provider": provider,
        "model": model,
        "actual_api_called": actual_api_called,
        "cached": cached,
        "status": status,
        "error_message": error_message,
    }
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = httpx.post(table_url(), headers=service_headers(), json=payload, timeout=10)
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        response.raise_for_status()
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except httpx.HTTPError as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"로그 저장 실패: {error}") from error
    # 학습 포인트: data 변수에 처리하거나 조회한 결과를 저장합니다.
    data = response.json()
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return str(data[0]["id"]) if data else None


# 학습 포인트: answer_with_cache_and_log 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def answer_with_cache_and_log(user: UserPublic, request: ChatRequest) -> ChatResponse:
    """캐시 확인, 답변 생성, 로그 저장을 하나의 요청 흐름으로 연결합니다."""

    # 학습 포인트: key 변수에 오른쪽에서 만든 값을 저장합니다.
    key = cache_key(user.id, request.message)
    # 1. 먼저 Redis에서 같은 사용자의 같은 질문 답변이 있는지 확인합니다.
    # 학습 포인트: cached_answer 변수에 오른쪽에서 만든 값을 저장합니다.
    cached_answer = redis_service.get_answer(key)

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if cached_answer:
        # 2. 캐시가 있으면 AI를 다시 호출하지 않고 캐시 답변을 반환합니다.
        #    그래도 "캐시를 사용했다"는 사실은 Supabase 로그에 남깁니다.
        # 학습 포인트: log_id 변수에 오른쪽에서 만든 값을 저장합니다.
        log_id = insert_log(
            user=user,
            request=request,
            answer=cached_answer,
            cached=True,
            provider="redis-cache",
            model="cached-answer",
            actual_api_called=False,
        )
        # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
        return ChatResponse(
            user_message=request.message,
            assistant_message=cached_answer,
            cached=True,
            provider="redis-cache",
            model="cached-answer",
            actual_api_called=False,
            log_id=log_id,
        )

    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 3. 캐시가 없으면 Gemini로 새 답변을 만듭니다.
        # 학습 포인트: answer_result 변수에 처리하거나 조회한 결과를 저장합니다.
        answer_result = create_answer(request.message)
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"AI 답변 생성 실패: {error}") from error

    # 4. 새로 만든 답변은 다음 요청에서 재사용할 수 있도록 Redis에 저장합니다.
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    redis_service.set_answer(key, answer_result.answer)
    # 5. 최종 처리 결과를 Supabase에 저장합니다.
    # 학습 포인트: log_id 변수에 오른쪽에서 만든 값을 저장합니다.
    log_id = insert_log(
        user=user,
        request=request,
        answer=answer_result.answer,
        cached=False,
        provider=answer_result.provider,
        model=answer_result.model,
        actual_api_called=answer_result.actual_api_called,
    )
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ChatResponse(
        user_message=request.message,
        assistant_message=answer_result.answer,
        cached=False,
        provider=answer_result.provider,
        model=answer_result.model,
        actual_api_called=answer_result.actual_api_called,
        log_id=log_id,
    )


# 학습 포인트: to_log_public 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def to_log_public(row: dict) -> ChatLogPublic:
    """Supabase row를 ChatLogPublic 응답 모델로 변환합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ChatLogPublic(
        id=str(row["id"]),
        user_id=str(row["user_id"]),
        user_message=row["user_message"],
        assistant_message=row.get("assistant_message"),
        provider=row["provider"],
        model=row.get("model"),
        actual_api_called=bool(row.get("actual_api_called", False)),
        cached=bool(row["cached"]),
        status=row["status"],
        error_message=row.get("error_message"),
        created_at=row.get("created_at"),
    )


# 학습 포인트: list_logs 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def list_logs(access_token: str | None) -> list[ChatLogPublic]:
    """현재 사용자 token으로 조회 가능한 채팅 로그를 가져옵니다.

    이 조회는 anon key + 사용자 access token으로 수행하므로 RLS가 실제로 적용됩니다.
    """

    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = httpx.get(
            table_url(),
            headers=user_headers(access_token),
            params={"select": "*", "order": "created_at.desc", "limit": "20"},
            timeout=10,
        )
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        response.raise_for_status()
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except httpx.HTTPError as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"로그 조회 실패: {error}") from error
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return [to_log_public(row) for row in response.json()]
