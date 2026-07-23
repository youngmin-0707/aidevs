# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""Notes API에서 사용하는 Pydantic 모델입니다."""

# 학습 포인트: 날짜와 시간 값을 다루는 기능을 가져옵니다.
from datetime import datetime
# 학습 포인트: 겹치지 않는 UUID 식별자를 다루는 기능을 가져옵니다.
from uuid import UUID

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel, Field


# 학습 포인트: NoteCreate 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class NoteCreate(BaseModel):
    """POST /notes 요청 Body입니다."""

    # Field의 min_length는 빈 문자열을 막습니다.
    # examples는 Swagger UI에서 예시 입력값으로 표시됩니다.
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    title: str = Field(min_length=1, examples=["FastAPI 구조 정리"])
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    content: str = Field(min_length=1, examples=["router, schema, service를 나누어 봅니다."])


# 학습 포인트: NoteUpdate 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class NoteUpdate(BaseModel):
    """PUT /notes/{note_id} 요청 Body입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    title: str = Field(min_length=1, examples=["수정된 제목"])
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    content: str = Field(min_length=1, examples=["수정된 내용"])


# 학습 포인트: NotePublic 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class NotePublic(BaseModel):
    """클라이언트에 반환하는 노트 응답 모델입니다."""

    # DB 내부 row를 그대로 반환하지 않고, 화면/API에 공개할 필드만 모델로 정의합니다.
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    id: UUID
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    title: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    content: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    created_at: datetime | None = None
