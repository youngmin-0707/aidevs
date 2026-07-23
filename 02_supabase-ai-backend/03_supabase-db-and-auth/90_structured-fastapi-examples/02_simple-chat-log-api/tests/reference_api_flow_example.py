# 학습 포인트: API 요청과 응답 흐름을 순서대로 보여 주는 참고 예제입니다.
# 바이브 코딩 프롬프트 예시:
# 이 FastAPI simple chat log 예제의 endpoint를 확인해서 tests/test_api_flow.py를 만들어줘.
# 조건:
# 1. test_app_routes.py는 그대로 둔다.
# 2. 실제 Supabase는 호출하지 말고 monkeypatch로 chat_service 함수를 가짜 함수로 바꾼다.
# 3. /chat 성공 흐름과 /logs 조회 흐름을 테스트한다.
# 4. message가 빈 문자열일 때 422가 나는지도 테스트한다.
# 5. 초보자가 이해할 수 있도록 상단 주석과 테스트 함수 주석을 자세히 넣는다.
# 6. python -m pytest tests로 실행했을 때 통과해야 한다.
#
# 사용 방법:
# 이 파일은 참고 예시입니다. 실제로 실행하고 싶으면 파일명을 test_api_flow.py로 복사하거나 변경합니다.

r"""02_simple-chat-log-api 핵심 API 흐름 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\02_simple-chat-log-api
    python -m pytest tests

이 테스트는 실제 Supabase 로그 테이블에 데이터를 저장하지 않습니다.
chat_service 함수를 monkeypatch로 바꿔서 /chat, /logs endpoint가
요청과 응답을 올바르게 처리하는지만 확인합니다.
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi.testclient import TestClient

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.main import app
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.routers import chat_router
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatLogPublic, ChatResponse


# 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
client = TestClient(app)


# 학습 포인트: test_chat_and_logs_flow 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_chat_and_logs_flow(monkeypatch) -> None:
    """채팅 요청 후 로그 목록을 조회하는 기본 흐름을 확인합니다."""

    # 학습 포인트: chat_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    chat_response = ChatResponse(
        user_message="오늘 배운 내용을 요약해줘",
        assistant_message="Gemini 응답입니다.",
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=True,
        log_id="log-1",
    )
    # 학습 포인트: log_row 변수에 오른쪽에서 만든 값을 저장합니다.
    log_row = ChatLogPublic(
        id="log-1",
        user_message="오늘 배운 내용을 요약해줘",
        assistant_message="Gemini 응답입니다.",
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=True,
        status="success",
        created_at="2026-07-01T00:00:00Z",
    )

    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    monkeypatch.setattr(chat_router.chat_service, "answer_and_log", lambda request: chat_response)
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    monkeypatch.setattr(chat_router.chat_service, "list_logs", lambda: [log_row])

    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.post("/chat", json={"message": "오늘 배운 내용을 요약해줘"})
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["provider"] == "gemini"
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.json()["actual_api_called"] is False

    # 학습 포인트: logs_response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    logs_response = client.get("/logs")
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert logs_response.status_code == 200
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert logs_response.json()["count"] == 1
    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert logs_response.json()["data"][0]["id"] == "log-1"


# 학습 포인트: test_chat_rejects_empty_message 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def test_chat_rejects_empty_message() -> None:
    """message가 빈 문자열이면 Pydantic 검증으로 422 에러가 나는지 확인합니다."""

    # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
    response = client.post("/chat", json={"message": ""})

    # 학습 포인트: 실제 결과가 예상값과 같은지 확인하고 다르면 테스트를 실패시킵니다.
    assert response.status_code == 422
