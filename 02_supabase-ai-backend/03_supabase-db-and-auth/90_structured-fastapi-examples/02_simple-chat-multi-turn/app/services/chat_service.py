# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""이전 대화를 읽어 Gemini 멀티턴 질문을 처리합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os
# 학습 포인트: 겹치지 않는 UUID 식별자를 다루는 기능을 가져옵니다.
from uuid import uuid4

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException, status

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.gemini import get_gemini_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.supabase import get_supabase_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatMessage, ChatRequest, ChatResponse


# 학습 포인트: TABLE_NAME 변수에 오른쪽에서 만든 값을 저장합니다.
TABLE_NAME = "ex90_multi_turn_chat_logs"
# 학습 포인트: HISTORY_LIMIT 변수에 오른쪽에서 만든 값을 저장합니다.
HISTORY_LIMIT = 6


# 학습 포인트: to_chat_message 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def to_chat_message(row: dict) -> ChatMessage:
    """Supabase row를 API 응답 모델로 바꿉니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ChatMessage(
        id=str(row["id"]),
        conversation_id=str(row["conversation_id"]),
        user_message=row["user_message"],
        assistant_message=row["assistant_message"],
        model=row["model"],
        created_at=row.get("created_at"),
    )


# 학습 포인트: get_recent_history 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_recent_history(conversation_id: str) -> list[dict]:
    """현재 대화의 최근 질문/답변을 오래된 순서로 가져옵니다."""

    # 학습 포인트: supabase 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase = get_supabase_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
        result = (
            supabase.table(TABLE_NAME)
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=True)
            .limit(HISTORY_LIMIT)
            .execute()
        )
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(500, f"대화 이력 조회 실패: {error}") from error

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return list(reversed(result.data))


# 학습 포인트: make_prompt 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def make_prompt(history: list[dict], message: str) -> str:
    """이전 대화와 새 질문을 Gemini에 보낼 텍스트로 만듭니다."""

    # 학습 포인트: lines 변수에 오른쪽에서 만든 값을 저장합니다.
    lines = ["당신은 초보자에게 쉽게 설명하는 AI 도우미입니다."]
    # 학습 포인트: 목록의 값을 하나씩 꺼내 같은 작업을 반복합니다.
    for row in history:
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        lines.append(f"사용자: {row['user_message']}")
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        lines.append(f"AI: {row['assistant_message']}")
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    lines.append(f"사용자: {message}")
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    lines.append("AI:")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return "\n".join(lines)


# 학습 포인트: create_gemini_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def create_gemini_answer(prompt: str) -> tuple[str, str]:
    """Gemini SDK로 답변을 만듭니다."""

    # 학습 포인트: model 변수에 오른쪽에서 만든 값을 저장합니다.
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_gemini_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.models.generate_content(model=model, contents=prompt)
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, f"Gemini 호출 실패: {error}") from error

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return response.text or "", model


# 학습 포인트: save_turn 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def save_turn(conversation_id: str, message: str, answer: str, model: str) -> None:
    """새 질문과 답변을 한 턴으로 저장합니다."""

    # 학습 포인트: supabase 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase = get_supabase_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        supabase.table(TABLE_NAME).insert(
            {
                "conversation_id": conversation_id,
                "user_message": message,
                "assistant_message": answer,
                "model": model,
            }
        ).execute()
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(500, f"대화 저장 실패: {error}") from error


# 학습 포인트: chat 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def chat(request: ChatRequest) -> ChatResponse:
    """이전 대화를 문맥으로 사용해 새 답변을 만들고 저장합니다."""

    # 학습 포인트: conversation_id 변수에 오른쪽에서 만든 값을 저장합니다.
    conversation_id = str(request.conversation_id) if request.conversation_id else str(uuid4())
    # 학습 포인트: history 변수에 오른쪽에서 만든 값을 저장합니다.
    history = get_recent_history(conversation_id)
    answer, model = create_gemini_answer(make_prompt(history, request.message))
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    save_turn(conversation_id, request.message, answer, model)

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ChatResponse(
        conversation_id=conversation_id,
        user_message=request.message,
        assistant_message=answer,
        model=model,
        context_turns=len(history),
    )


# 학습 포인트: list_messages 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def list_messages(conversation_id: str) -> list[ChatMessage]:
    """대화 전체 이력을 오래된 순서로 반환합니다."""

    # 학습 포인트: supabase 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase = get_supabase_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
        result = (
            supabase.table(TABLE_NAME)
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at")
            .execute()
        )
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(500, f"대화 이력 조회 실패: {error}") from error

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return [to_chat_message(row) for row in result.data]
