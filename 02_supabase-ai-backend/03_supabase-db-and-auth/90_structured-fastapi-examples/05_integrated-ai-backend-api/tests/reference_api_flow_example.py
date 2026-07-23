# 학습 포인트: API 요청과 응답 흐름을 순서대로 보여 주는 참고 예제입니다.
# 바이브 코딩 프롬프트 예시:
# 이 FastAPI integrated AI backend 예제의 endpoint를 확인해서 tests/test_api_flow.py를 만들어줘.
# 조건:
# 1. test_app_routes.py는 그대로 둔다.
# 2. 실제 Supabase, Redis, Gemini는 호출하지 않는다.
# 3. monkeypatch로 auth_service, chat_service 함수를 가짜 함수로 바꾼다.
# 4. dependency_overrides로 Bearer token 검증을 통과한 가짜 사용자를 만든다.
# 5. /auth/signup, /auth/signin, /chat, /logs 흐름을 테스트한다.
# 6. 인증은 통과했지만 message가 빈 문자열이면 422가 나는지도 테스트한다.
# 7. 초보자가 이해할 수 있도록 상단 주석과 테스트 함수 주석을 자세히 넣는다.
# 8. python -m pytest tests로 실행했을 때 통과해야 한다.
#
# 사용 방법:
# 이 파일은 참고 예시입니다. 실제로 실행하고 싶으면 파일명을 test_api_flow.py로 복사하거나 변경합니다.

r"""05_integrated-ai-backend-api 핵심 API 흐름 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api
    python -m pytest tests

이 테스트는 실제 Supabase, Redis, Gemini를 호출하지 않습니다.
Auth dependency와 chat_service 함수를 가짜 함수로 바꿔서,
통합 프로젝트의 핵심 endpoint가 연결되어 있는지 확인합니다.
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.routers import auth_router, chat_router
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.auth_schema import AuthResponse, UserPublic
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatLogPublic, ChatResponse
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import auth_service


# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: fake_current_user 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def fake_current_user() -> UserPublic:
    """테스트에서 사용할 가짜 로그인 사용자입니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return UserPublic(id="user-1", email="student@example.com", access_token="test-token")


# 학습 포인트: test_auth_chat_and_logs_flow 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_auth_chat_and_logs_flow(monkeypatch) -> None:
    """회원가입/로그인 후 인증 사용자 기준 채팅과 로그 조회 흐름을 확인합니다."""

    # 학습 포인트: user 변수에 오른쪽에서 만든 값을 저장합니다.
    user = UserPublic(id="user-1", email="student@example.com", access_token="test-token")
    # 학습 포인트: auth_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    auth_response = AuthResponse(user=user, access_token="test-token")
    # 학습 포인트: chat_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    chat_response = ChatResponse(
        user_message="Redis 캐시는 언제 쓰나요?",
        assistant_message="반복 질문의 응답을 빠르게 돌려줄 때 사용합니다.",
        cached=False,
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=True,
        log_id="log-1",
    )
    # 학습 포인트: log_row 변수에 오른쪽에서 만든 값을 저장합니다.
    log_row = ChatLogPublic(
        id="log-1",
        user_id="user-1",
        user_message="Redis 캐시는 언제 쓰나요?",
        assistant_message="반복 질문의 응답을 빠르게 돌려줄 때 사용합니다.",
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=True,
        cached=False,
        status="success",
        created_at="2026-07-01T00:00:00Z",
    )

    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    monkeypatch.setattr(auth_router.auth_service, "signup", lambda request: user)
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    monkeypatch.setattr(auth_router.auth_service, "signin", lambda request: auth_response)
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    monkeypatch.setattr(chat_router.chat_service, "answer_with_cache_and_log", lambda user, request: chat_response)
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    monkeypatch.setattr(chat_router.chat_service, "list_logs", lambda access_token: [log_row])
    app.dependency_overrides[auth_service.get_current_user] = fake_current_user

    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: signup_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        signup_response = client.post(
            "/auth/signup",
            json={"email": "student@example.com", "password": "password123"},
        )
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert signup_response.status_code == 200

        # 학습 포인트: signin_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        signin_response = client.post(
            "/auth/signin",
            json={"email": "student@example.com", "password": "password123"},
        )
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert signin_response.status_code == 200
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert signin_response.json()["token_type"] == "bearer"

        # 학습 포인트: chat_api_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        chat_api_response = client.post(
            "/chat",
            headers={"Authorization": "Bearer test-token"},
            json={"message": "Redis 캐시는 언제 쓰나요?"},
        )
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert chat_api_response.status_code == 200
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert chat_api_response.json()["provider"] == "gemini"
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert chat_api_response.json()["actual_api_called"] is True

        # 학습 포인트: logs_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        logs_response = client.get("/logs", headers={"Authorization": "Bearer test-token"})
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert logs_response.status_code == 200
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert logs_response.json()["count"] == 1
    # 학습 포인트: 오류 여부와 관계없이 마지막에 반드시 실행합니다.
    finally:
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        app.dependency_overrides.clear()


# 학습 포인트: test_chat_rejects_empty_message 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_chat_rejects_empty_message(monkeypatch) -> None:
    """인증은 통과했지만 message가 비어 있으면 422 에러가 나는지 확인합니다."""

    app.dependency_overrides[auth_service.get_current_user] = fake_current_user

    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.post(
            "/chat",
            headers={"Authorization": "Bearer test-token"},
            json={"message": ""},
        )
        # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
        assert response.status_code == 422
    # 학습 포인트: 오류 여부와 관계없이 마지막에 반드시 실행합니다.
    finally:
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        app.dependency_overrides.clear()
