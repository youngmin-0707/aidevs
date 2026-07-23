# 학습 포인트: API 동작을 pytest로 자동 확인하는 테스트 파일입니다.
r"""01_notes-api-with-supabase 라우트 테스트입니다.

실행 방법:
    cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\01_notes-api-with-supabase
    python -m pytest tests

이 테스트는 실제 Supabase에 데이터를 넣고 조회하는 테스트가 아닙니다.
FastAPI 앱이 정상적으로 import되는지, /health API가 응답하는지,
Swagger/OpenAPI 문서에 notes 관련 URL이 등록되어 있는지를 확인합니다.
초보자는 이 파일을 통해 "API 서버를 직접 실행하지 않아도 TestClient로 API를 호출할 수 있다"는 점을 이해하면 됩니다.
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app


# TestClient는 FastAPI 앱을 테스트 코드 안에서 직접 호출할 수 있게 해 줍니다.
# uvicorn 서버를 따로 켜지 않아도 GET/POST 요청을 흉내 낼 수 있습니다.
# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: test_health_route_is_ready 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_health_route_is_ready() -> None:
    """기본 상태 확인 API인 /health가 정상 응답하는지 확인합니다."""

    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.get("/health")
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["status"] == "ok"


# 학습 포인트: test_openapi_has_notes_routes 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_openapi_has_notes_routes() -> None:
    """OpenAPI 문서에 notes 생성/조회용 URL이 등록되어 있는지 확인합니다."""

    # 학습 포인트: schema 변수에 오른쪽에서 만든 값을 저장합니다.
    schema = client.get("/openapi.json").json()
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/notes" in schema["paths"]
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert "/notes/{note_id}" in schema["paths"]
