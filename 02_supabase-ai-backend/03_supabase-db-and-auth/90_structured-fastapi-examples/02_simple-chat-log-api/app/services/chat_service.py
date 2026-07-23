# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""Gemini AI 답변을 만들고 Supabase에 로그를 저장합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException, status

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.gemini import get_gemini_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.supabase import get_supabase_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatLogPublic, ChatRequest, ChatResponse


# 학습 포인트: TABLE_NAME 변수에 오른쪽에서 만든 값을 저장합니다.
TABLE_NAME = "ex90_simple_chat_logs"


# 학습 포인트: create_gemini_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def create_gemini_answer(message: str) -> tuple[str, str]:
    """Gemini SDK로 답변을 만듭니다."""

    # 학습 포인트: model 변수에 오른쪽에서 만든 값을 저장합니다.
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_gemini_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.models.generate_content(model=model, contents=message)
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"Gemini 호출 실패: {error}") from error

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return response.text or "", model


# 학습 포인트: to_log_public 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def to_log_public(row: dict) -> ChatLogPublic:
    """Supabase row를 API 응답 모델로 변환합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ChatLogPublic(
        id=str(row["id"]),
        user_message=row["user_message"],
        assistant_message=row.get("assistant_message"),
        provider=row["provider"],
        model=row.get("model"),
        actual_api_called=bool(row.get("actual_api_called", False)),
        status=row["status"],
        error_message=row.get("error_message"),
        created_at=row.get("created_at"),
    )


# 학습 포인트: answer_and_log 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def answer_and_log(request: ChatRequest) -> ChatResponse:
    """Gemini 답변 생성과 로그 저장을 한 번에 수행합니다."""

    answer, model = create_gemini_answer(request.message)
    # DB에 저장할 컬럼만 명시적으로 구성합니다.
    # 학습 포인트: payload 변수에 오른쪽에서 만든 값을 저장합니다.
    payload = {
        "user_message": request.message,
        "assistant_message": answer,
        "provider": "gemini",
        "model": model,
        "actual_api_called": True,
        "status": "success",
    }
    # 학습 포인트: supabase 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase = get_supabase_client()
  
    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = supabase.table(TABLE_NAME).insert(payload).execute()

    # 학습 포인트: log_id 변수에 오른쪽에서 만든 값을 저장합니다.
    log_id = str(result.data[0]["id"]) if result.data else None

    # API 응답은 DB 저장 결과 전체가 아니라 화면에 필요한 값만 돌려줍니다.
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ChatResponse(
        user_message=request.message,
        assistant_message=answer,
        provider="gemini",
        model=model,
        actual_api_called=True,
        log_id=log_id,
    )


# 학습 포인트: list_logs 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def list_logs() -> list[ChatLogPublic]:
    """최근 채팅 로그 20개를 최신순으로 조회합니다."""

    # 학습 포인트: supabase 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase = get_supabase_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
        result = (
            supabase.table(TABLE_NAME)
            .select("*")
            .order("created_at", desc=True)
            .limit(20)
            .execute()
        )
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Supabase 로그 조회 실패: {error}",
        ) from error
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return [to_log_public(row) for row in result.data]
