# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""멀티턴 채팅 API 경로입니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatMessage, ChatRequest, ChatResponse
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import chat_service


# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter()


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버와 필수 환경변수 준비 상태를 확인합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "status": "ok",
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
        and bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


# 학습 포인트: POST 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """이전 대화를 문맥으로 사용해 새 답변을 만듭니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return chat_service.chat(request)


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/conversations/{conversation_id}/messages", response_model=list[ChatMessage])
def messages(conversation_id: str) -> list[ChatMessage]:
    """특정 대화의 전체 이력을 조회합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return chat_service.list_messages(conversation_id)
