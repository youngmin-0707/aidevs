# 학습 포인트: API 동작을 pytest로 자동 확인하는 테스트 파일입니다.
r"""02_simple-chat-log-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\02_simple-chat-log-api
    python -m pytest tests

이 테스트는 채팅 로그를 실제 Supabase에 저장하는 통합 테스트가 아닙니다.
FastAPI 앱이 정상적으로 준비되는지, /health API가 응답하는지,
Swagger/OpenAPI 문서에 /chat, /logs URL이 등록되어 있는지를 확인합니다.
처음에는 이런 "라우트 존재 확인 테스트"만으로도 프로젝트 구조가 깨졌는지 빠르게 알 수 있습니다.
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app


# TestClient는 브라우저나 Postman 대신 테스트 코드에서 API를 호출하는 도구입니다.
# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: test_health_route_is_ready 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_health_route_is_ready() -> None:
    """서버 상태 확인용 /health API가 정상 동작하는지 확인합니다."""

    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.get("/health")
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["status"] == "ok"


# 학습 포인트: test_openapi_has_chat_routes 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_openapi_has_chat_routes() -> None:
    """채팅 요청과 로그 조회 API가 OpenAPI 문서에 포함되어 있는지 확인합니다."""

    # 학습 포인트: schema 변수에 오른쪽에서 만든 값을 저장합니다.
    schema = client.get("/openapi.json").json()
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/chat" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/logs" in schema["paths"]
