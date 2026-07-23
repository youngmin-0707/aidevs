# 학습 포인트: API 데이터의 필드와 자료형을 검사하는 Pydantic 스키마 파일입니다.
"""Redis 캐시 응답 모델입니다."""

# 학습 포인트: Pydantic의 데이터 검증 및 설정 기능을 가져옵니다.
from pydantic import BaseModel


# 학습 포인트: CachedAnswerResponse 클래스를 정의해 관련 데이터나 기능을 하나로 묶습니다.
class CachedAnswerResponse(BaseModel):
    """캐시 조회 결과를 화면/API에 반환할 때 사용하는 모델입니다."""

    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    question: str
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    answer: str
    # cached=True이면 Redis에서 기존 답변을 읽은 것이고,
    # cached=False이면 이번 요청에서 새 답변을 만든 것입니다.
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    cached: bool
    # 학습 포인트: 필드 이름과 자료형을 선언해 데이터의 형태를 정합니다.
    ttl_seconds: int
