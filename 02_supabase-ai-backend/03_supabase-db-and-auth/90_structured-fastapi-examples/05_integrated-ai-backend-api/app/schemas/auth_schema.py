# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""Auth 모델입니다."""

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel, Field


# 학습 포인트: AuthRequest 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class AuthRequest(BaseModel):
    """회원가입과 로그인 요청 Body입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    email: str = Field(min_length=3, examples=["student@example.com"])
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    password: str = Field(min_length=6, examples=["password123"])


# 학습 포인트: UserPublic 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class UserPublic(BaseModel):
    """클라이언트에 공개할 사용자 정보입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    email: str | None = None
    # access_token은 보호 API 호출에 필요한 값입니다.
    # Swagger Authorize에 이 값을 넣으면 /me, /chat, /logs를 이어서 테스트할 수 있습니다.
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
