# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""채팅 로그 API에서 사용하는 요청/응답 모델입니다."""

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel, Field


# 학습 포인트: ChatRequest 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatRequest(BaseModel):
    """POST /chat 요청 Body입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    message: str = Field(min_length=1, examples=["오늘 배운 내용을 요약해줘"])


# 학습 포인트: ChatResponse 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatResponse(BaseModel):
    """POST /chat 응답 모델입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    user_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    assistant_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    provider: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    model: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    actual_api_called: bool
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    log_id: str | None = None


# 학습 포인트: ChatLogPublic 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatLogPublic(BaseModel):
    """GET /logs에서 반환하는 로그 1건의 모델입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    user_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    assistant_message: str | None = None
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    provider: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    model: str | None = None
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    actual_api_called: bool = False
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    status: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    error_message: str | None = None
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    created_at: str | None = None
