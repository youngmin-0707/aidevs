# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""채팅 로그 API 경로를 정의합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatLogPublic
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import chat_service


# 채팅 로그와 관련된 endpoint를 한 router에 모읍니다.
# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter()


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버 실행 여부와 Supabase/Gemini 환경변수 준비 여부를 확인합니다."""

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
    """사용자 질문을 Gemini로 처리하고 Supabase에 로그를 남깁니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return chat_service.answer_and_log(request)


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/logs")
def list_logs() -> dict[str, int | list[ChatLogPublic]]:
    """최근 채팅 로그 목록을 조회합니다."""

    # 학습 포인트: logs 변수에 오른쪽에서 만든 값을 저장합니다.
    logs = chat_service.list_logs()
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {"count": len(logs), "data": logs}
