# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""Redis 멀티턴 채팅 API 경로입니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatRequest, ChatResponse, ConversationMessage
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import chat_service


# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter()


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/health")
def health() -> dict[str, str | bool]:
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "status": "ok",
        "redis_configured": bool(os.getenv("UPSTASH_REDIS_REST_URL"))
        and bool(os.getenv("UPSTASH_REDIS_REST_TOKEN")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


# 학습 포인트: POST 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return chat_service.chat(request)


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/conversations/{conversation_id}/messages", response_model=list[ConversationMessage])
def messages(conversation_id: str) -> list[ConversationMessage]:
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return chat_service.get_messages(conversation_id)


# 학습 포인트: DELETE 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.delete("/conversations/{conversation_id}")
def clear_conversation(conversation_id: str) -> dict[str, int | str]:
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "conversation_id": conversation_id,
        "deleted_count": chat_service.clear_conversation(conversation_id),
    }
