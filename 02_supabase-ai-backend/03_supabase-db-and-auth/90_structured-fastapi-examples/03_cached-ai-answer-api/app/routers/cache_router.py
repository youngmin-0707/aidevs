# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""Redis 캐시 API 경로를 정의합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter, Query

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.cache_schema import CachedAnswerResponse
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import cache_service


# 캐시 관련 endpoint만 모아 둔 router입니다.
# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter()


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버와 Redis/Gemini 환경변수 설정 상태를 확인합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "status": "ok",
        "redis_configured": bool(os.getenv("UPSTASH_REDIS_REST_URL"))
        and bool(os.getenv("UPSTASH_REDIS_REST_TOKEN")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/ai/answer", response_model=CachedAnswerResponse)
def answer(question: str = Query(min_length=1)) -> CachedAnswerResponse:
    """질문에 대한 Gemini 답변을 Redis에서 찾거나 새로 만들어 저장합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return cache_service.get_or_create_answer(question)


# 학습 포인트: DELETE 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.delete("/ai/answer-cache")
def clear_cache(question: str = Query(min_length=1)) -> dict[str, str | int]:
    """실습 중 특정 질문의 캐시를 지우고 싶을 때 사용합니다."""

    # 학습 포인트: deleted_count 변수에 오른쪽에서 만든 값을 저장합니다.
    deleted_count = cache_service.clear_answer(question)
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {"question": question, "deleted_count": deleted_count}
