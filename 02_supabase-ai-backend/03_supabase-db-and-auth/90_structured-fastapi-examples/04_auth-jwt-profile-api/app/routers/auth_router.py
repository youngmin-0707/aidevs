# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""Auth 관련 API 경로입니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.auth_schema import AuthRequest, AuthResponse, SignupRequest, UserPublic
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import auth_service


# 인증 관련 endpoint를 모은 router입니다.
# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter()


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버 실행 여부와 Supabase Auth 환경변수 준비 상태를 확인합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "status": "ok",
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
        and bool(os.getenv("SUPABASE_ANON_KEY"))
        and bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY")),
    }


# 학습 포인트: POST 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.post("/auth/signup", response_model=UserPublic)
def signup(request: SignupRequest) -> UserPublic:
    """Supabase Auth에 회원가입을 요청합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return auth_service.signup(request)


# 학습 포인트: POST 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.post("/auth/signin", response_model=AuthResponse)
def signin(request: AuthRequest) -> AuthResponse:
    """Supabase Auth에 로그인하고 access token을 반환합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return auth_service.signin(request)


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/me", response_model=UserPublic)
def me(user: auth_service.CurrentUser) -> UserPublic:
    """Authorization Bearer token으로 확인된 현재 사용자 정보를 반환합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return user
