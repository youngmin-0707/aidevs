# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""멀티턴 대화 API의 요청과 응답 모델입니다."""

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel, Field
# 학습 포인트: 겹치지 않는 UUID 식별자를 다루는 기능을 가져옵니다.
from uuid import UUID


# 학습 포인트: ChatRequest 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatRequest(BaseModel):
    """새 질문과 선택적인 대화 ID입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    message: str = Field(min_length=1, max_length=1000, examples=["방금 설명을 예시로 다시 알려줘"])
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    conversation_id: UUID | None = Field(
        default=None,
        description="이전 대화를 이어 갈 UUID입니다. 비우면 새 대화를 시작합니다.",
    )


# 학습 포인트: ChatResponse 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatResponse(BaseModel):
    """Gemini 답변과 현재 대화 ID를 반환합니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    conversation_id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    user_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    assistant_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    model: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    context_turns: int


# 학습 포인트: ChatMessage 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class ChatMessage(BaseModel):
    """저장된 대화 1턴입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    conversation_id: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    user_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    assistant_message: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    model: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    created_at: str | None = None
