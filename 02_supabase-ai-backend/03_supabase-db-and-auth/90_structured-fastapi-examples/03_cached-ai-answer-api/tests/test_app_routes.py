# 학습 포인트: API 동작을 pytest로 자동 확인하는 테스트 파일입니다.
r"""03_cached-ai-answer-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\03_cached-ai-answer-api
    python -m pytest tests

이 테스트는 Redis나 외부 LLM을 실제로 호출하지 않습니다.
FastAPI 앱이 정상적으로 import되는지, /health API가 응답하는지,
Gemini 답변 API와 Redis 캐시 API가 문서에 등록되어 있는지를 확인합니다.
초보자는 여기서 "기능 내부 구현을 다 검증하기 전에 API 경로부터 확인할 수 있다"는 흐름을 보면 됩니다.
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app


# TestClient는 FastAPI 앱을 메모리 안에서 실행해 요청과 응답을 확인합니다.
# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: test_health_route_is_ready 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_health_route_is_ready() -> None:
    """기본 상태 확인 API가 200 OK와 status=ok를 반환하는지 확인합니다."""

    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.get("/health")
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["status"] == "ok"


# 학습 포인트: test_openapi_has_cache_routes 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_openapi_has_cache_routes() -> None:
    """Gemini 답변과 캐시 삭제 URL이 OpenAPI 문서에 있는지 확인합니다."""

    # 학습 포인트: schema 변수에 오른쪽에서 만든 값을 저장합니다.
    schema = client.get("/openapi.json").json()
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/ai/answer" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/ai/answer-cache" in schema["paths"]
