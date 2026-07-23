# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""Profile 요청/응답 모델입니다.

Profile API에서는 로그인한 사용자의 화면 표시 이름을 저장하고 조회합니다.
"""

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel, Field


# 학습 포인트: ProfileUpdate 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ProfileUpdate(BaseModel):
    """PUT /profile 요청 Body입니다."""

    # display_name은 화면에 보여 줄 이름입니다.
    # 로그인 email과 별도로 사용자에게 보여 줄 이름을 저장한다고 보면 됩니다.
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    display_name: str = Field(min_length=1, examples=["홍길동"])


# 학습 포인트: ProfilePublic 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ProfilePublic(BaseModel):
    """클라이언트에 반환하는 프로필 응답 모델입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    display_name: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    created_at: str | None = None
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    updated_at: str | None = None
