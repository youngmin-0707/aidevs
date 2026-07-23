# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""Profile 관련 API 경로입니다."""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.profile_schema import ProfilePublic, ProfileUpdate
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import auth_service, profile_service


# prefix="/profile"을 사용하면 아래 endpoint들이 /profile 경로 아래에 묶입니다.
# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter(prefix="/profile")


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("", response_model=ProfilePublic)
def get_profile(user: auth_service.CurrentUser) -> ProfilePublic:
    """현재 로그인한 사용자의 프로필을 조회합니다."""

    # user는 auth_service.get_current_user가 Bearer token을 검증한 결과입니다.
    # user.access_token을 Supabase REST API에 전달하면 RLS가 auth.uid()를 판단할 수 있습니다.
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return profile_service.get_profile(user.access_token)


# 학습 포인트: 수정 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.put("", response_model=ProfilePublic)
def upsert_profile(
    request: ProfileUpdate,
    user: auth_service.CurrentUser,
) -> ProfilePublic:
    """현재 로그인한 사용자의 프로필을 생성하거나 수정합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return profile_service.upsert_profile(user.id, user.access_token, request)
