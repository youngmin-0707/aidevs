# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""Auth 요청/응답 모델입니다."""

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel, Field


# 학습 포인트: AuthRequest 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class AuthRequest(BaseModel):
    """로그인 요청 Body입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    email: str = Field(min_length=3, examples=["student@example.com"])
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    password: str = Field(min_length=6, examples=["password123"])


# 학습 포인트: SignupRequest 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class SignupRequest(AuthRequest):
    """회원가입 시 이메일/비밀번호와 함께 받을 사용자 표시 이름입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    display_name: str = Field(min_length=1, max_length=50, examples=["수강생"])


# 학습 포인트: UserPublic 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class UserPublic(BaseModel):
    """API 응답에서 보여 줄 사용자 정보입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    email: str | None = None


# 학습 포인트: AuthenticatedUser 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class AuthenticatedUser(UserPublic):
    """서버 내부에서만 Bearer token을 함께 사용하는 인증 사용자입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    access_token: str | None = None


# 학습 포인트: AuthResponse 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class AuthResponse(BaseModel):
    """로그인 성공 응답입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    user: UserPublic
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    access_token: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    token_type: str = "bearer"
