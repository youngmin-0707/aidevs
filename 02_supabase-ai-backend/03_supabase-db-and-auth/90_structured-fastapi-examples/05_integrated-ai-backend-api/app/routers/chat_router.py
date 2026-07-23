# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""인증된 사용자의 채팅 API입니다."""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.auth_schema import UserPublic
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatLogPublic
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import auth_service, chat_service


# 인증이 필요한 채팅/로그 endpoint를 모은 router입니다.
# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter()


# 학습 포인트: POST 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    user: auth_service.CurrentUser,
) -> ChatResponse:
    """현재 사용자 기준으로 AI 답변을 만들고 캐시/로그 저장까지 수행합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return chat_service.answer_with_cache_and_log(user, request)


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/logs")
def logs(user: auth_service.CurrentUser) -> dict[str, int | list[ChatLogPublic]]:
    """현재 사용자 token으로 Supabase RLS가 적용된 로그 목록을 조회합니다."""

    # 학습 포인트: data 변수에 처리하거나 조회한 결과를 저장합니다.
    data = chat_service.list_logs(user.access_token)
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {"count": len(data), "data": data}
