# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""Redis 멀티턴 채팅 API 모델입니다."""

# 학습 포인트: 겹치지 않는 UUID 식별자를 다루는 기능을 가져옵니다.
from uuid import UUID

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel, Field


# 학습 포인트: ChatRequest 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatRequest(BaseModel):
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    message: str = Field(min_length=1, max_length=1000)
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    conversation_id: UUID | None = None


# 학습 포인트: ChatResponse 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatResponse(BaseModel):
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    conversation_id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    user_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    assistant_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    model: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    context_messages: int
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    ttl_seconds: int


# 학습 포인트: ConversationMessage 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ConversationMessage(BaseModel):
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    role: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    content: str
