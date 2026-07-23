# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""Supabase Auth와 Bearer token 확인을 담당합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 자료형을 명확히 표시하는 타입 힌트 도구를 가져옵니다.
from typing import Annotated

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import Depends, HTTPException, status
# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.supabase import get_supabase_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.auth_schema import (
    AuthenticatedUser,
    AuthRequest,
    AuthResponse,
    SignupRequest,
    UserPublic,
)


# Swagger UI에 Authorize 버튼을 표시하고 Bearer token 입력을 지원합니다.
# 학습 포인트: bearer_security 변수에 오른쪽에서 만든 값을 저장합니다.
bearer_security = HTTPBearer(auto_error=False)


# 학습 포인트: signup 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def signup(request: SignupRequest) -> UserPublic:
    """이메일/비밀번호로 Supabase Auth 회원가입을 요청합니다."""

    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_supabase_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 사용자 계정 생성은 FastAPI가 직접 DB에 insert하지 않습니다.
        # Supabase Auth가 auth.users 테이블과 인증 절차를 관리합니다.
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
                # display_name은 auth.users의 raw_user_meta_data에 저장됩니다.
                "options": {"data": {"display_name": request.display_name}},
            }
        )
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=400, detail=f"sign up 실패: {error}") from error

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if response.user is None:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=400, detail="user가 없는 signup 응답입니다.")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return UserPublic(id=response.user.id, email=response.user.email)


# 학습 포인트: signin 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def signin(request: AuthRequest) -> AuthResponse:
    """이메일/비밀번호로 로그인하고 Supabase access token을 받습니다."""

    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_supabase_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 로그인에 성공하면 Supabase가 session과 access_token을 반환합니다.
        # 이 token은 이후 Authorization: Bearer <token> 헤더로 사용합니다.
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=401, detail=f"sign in 실패: {error}") from error

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if response.user is None or response.session is None:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=401, detail="로그인 응답에 user/session이 없습니다.")

    # 학습 포인트: user 변수에 오른쪽에서 만든 값을 저장합니다.
    user = UserPublic(
        id=response.user.id,
        email=response.user.email,
    )
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return AuthResponse(user=user, access_token=response.session.access_token)


# 학습 포인트: get_current_user 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_security),
) -> AuthenticatedUser:
    """Swagger 또는 Authorization 헤더의 Bearer token으로 현재 사용자를 확인합니다."""

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if credentials is None or credentials.scheme.lower() != "bearer":
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization: Bearer <access_token> 헤더가 필요합니다.",
        )

    # 학습 포인트: token 변수에 오른쪽에서 만든 값을 저장합니다.
    token = credentials.credentials.strip()
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not token:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token 값이 비어 있습니다.",
        )
    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_supabase_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # token 검증은 Supabase Auth에 맡깁니다.
        # 유효한 token이면 response.user에 현재 사용자 정보가 들어옵니다.
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.auth.get_user(token)
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=401, detail=f"token 확인 실패: {error}") from error

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if response.user is None:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=401, detail="유효하지 않은 token입니다.")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return AuthenticatedUser(
        id=response.user.id,
        email=response.user.email,
        access_token=token,
    )


# 학습 포인트: CurrentUser 변수에 오른쪽에서 만든 값을 저장합니다.
CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]
