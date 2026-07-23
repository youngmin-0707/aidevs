# 학습 포인트: API 동작을 pytest로 자동 확인하는 테스트 파일입니다.
"""Redis 멀티턴 채팅 API의 기본 라우트를 확인합니다."""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app


# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: test_health_route_is_ready 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_health_route_is_ready() -> None:
    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.get("/health")

    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["status"] == "ok"


# 학습 포인트: test_openapi_has_multi_turn_redis_routes 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_openapi_has_multi_turn_redis_routes() -> None:
    # 학습 포인트: schema 변수에 오른쪽에서 만든 값을 저장합니다.
    schema = client.get("/openapi.json").json()

    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/chat" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/conversations/{conversation_id}/messages" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/conversations/{conversation_id}" in schema["paths"]
