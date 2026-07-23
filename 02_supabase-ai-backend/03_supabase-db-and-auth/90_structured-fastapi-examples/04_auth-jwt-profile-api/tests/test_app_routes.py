# 학습 포인트: API 동작을 pytest로 자동 확인하는 테스트 파일입니다.
r"""04_auth-jwt-profile-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\04_auth-jwt-profile-api
    python -m pytest tests

이 테스트는 실제 회원가입, 로그인, JWT 검증을 수행하지 않습니다.
대신 FastAPI 앱이 정상적으로 준비되는지, /health API가 응답하는지,
Auth와 Profile 관련 URL이 Swagger/OpenAPI 문서에 등록되어 있는지를 확인합니다.
인증 API는 외부 서비스와 연결될 수 있으므로, 처음에는 라우트 존재 여부부터 확인하는 방식이 안전합니다.
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app


# TestClient는 테스트 중에 FastAPI 앱을 직접 호출하는 간단한 클라이언트입니다.
# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: test_health_route_is_ready 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_health_route_is_ready() -> None:
    """인증 예제 앱의 /health API가 정상 응답하는지 확인합니다."""

    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.get("/health")
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["status"] == "ok"


# 학습 포인트: test_openapi_has_auth_and_profile_routes 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_openapi_has_auth_and_profile_routes() -> None:
    """회원가입, 로그인, 내 정보, 프로필 API 경로가 등록되어 있는지 확인합니다."""

    # 학습 포인트: schema 변수에 오른쪽에서 만든 값을 저장합니다.
    schema = client.get("/openapi.json").json()
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/auth/signup" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/auth/signin" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/me" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/profile" in schema["paths"]
