# 학습 포인트: API 동작을 pytest로 자동 확인하는 테스트 파일입니다.
r"""05_integrated-ai-backend-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api
    python -m pytest tests

이 테스트는 통합 예제의 모든 기능을 실제로 끝까지 호출하지 않습니다.
FastAPI 앱이 정상적으로 import되는지, /health API가 응답하는지,
인증, 사용자 정보, 채팅, 로그 관련 핵심 URL이 OpenAPI 문서에 등록되어 있는지를 확인합니다.
통합 프로젝트에서는 파일 구조가 많아지기 때문에, 이런 라우트 테스트가 깨지면 main.py 또는 router 연결부터 확인하면 됩니다.
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app


# TestClient는 서버를 따로 실행하지 않고 FastAPI 앱에 요청을 보내는 테스트용 클라이언트입니다.
# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: test_health_route_is_ready 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_health_route_is_ready() -> None:
    """통합 예제 앱의 /health API가 정상 응답하는지 확인합니다."""

    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.get("/health")
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["status"] == "ok"


# 학습 포인트: test_openapi_has_integrated_routes 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_openapi_has_integrated_routes() -> None:
    """통합 예제에 필요한 핵심 API 경로가 모두 등록되어 있는지 확인합니다."""

    # 학습 포인트: schema 변수에 오른쪽에서 만든 값을 저장합니다.
    schema = client.get("/openapi.json").json()
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/auth/signup" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/auth/signin" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/me" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/chat" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/logs" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "HTTPBearer" in schema["components"]["securitySchemes"]
