# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""Redis List와 TTL로 멀티턴 Gemini 대화를 처리합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import json
# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os
# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from urllib.parse import quote
# 학습 포인트: 겹치지 않는 UUID 식별자를 다루는 기능을 가져옵니다.
from uuid import uuid4

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import httpx
# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.gemini import get_gemini_client
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.chat_schema import ChatRequest, ChatResponse, ConversationMessage


# 학습 포인트: TTL_SECONDS 변수에 오른쪽에서 만든 값을 저장합니다.
TTL_SECONDS = 1800
# 학습 포인트: HISTORY_LIMIT 변수에 오른쪽에서 만든 값을 저장합니다.
HISTORY_LIMIT = 12


# 학습 포인트: redis_command 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def redis_command(*parts: str) -> dict:
    """Upstash Redis REST API로 Redis 명령을 실행합니다."""

    # 학습 포인트: rest_url 변수에 오른쪽에서 만든 값을 저장합니다.
    rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
    # 학습 포인트: rest_token 변수에 오른쪽에서 만든 값을 저장합니다.
    rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not rest_url:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(500, "UPSTASH_REDIS_REST_URL이 없습니다. .env 파일을 확인하세요.")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not rest_token:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(500, "UPSTASH_REDIS_REST_TOKEN이 없습니다. .env 파일을 확인하세요.")

    # 학습 포인트: url 변수에 오른쪽에서 만든 값을 저장합니다.
    url = f"{rest_url.rstrip('/')}/{'/'.join(quote(part, safe='') for part in parts)}"
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = httpx.get(url, headers={"Authorization": f"Bearer {rest_token}"}, timeout=10)
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        response.raise_for_status()
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except httpx.HTTPError as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(502, f"Redis 호출 실패: {error}") from error
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return response.json()


# 학습 포인트: redis_key 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def redis_key(conversation_id: str) -> str:
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return f"ex90:multi-turn:{conversation_id}:messages"


# 학습 포인트: get_messages 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_messages(conversation_id: str) -> list[ConversationMessage]:
    """Redis List에서 현재 세션의 대화 문맥을 읽습니다."""

    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = redis_command("lrange", redis_key(conversation_id), "0", "-1")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return [ConversationMessage(**json.loads(item)) for item in result.get("result", [])]


# 학습 포인트: save_message 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def save_message(conversation_id: str, role: str, content: str) -> None:
    """메시지를 Redis List 끝에 저장하고 TTL을 다시 30분으로 설정합니다."""

    # 학습 포인트: key 변수에 오른쪽에서 만든 값을 저장합니다.
    key = redis_key(conversation_id)
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    redis_command("rpush", key, json.dumps({"role": role, "content": content}))
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    redis_command("expire", key, str(TTL_SECONDS))


# 학습 포인트: make_prompt 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def make_prompt(history: list[ConversationMessage], message: str) -> str:
    """최근 대화와 새 질문을 Gemini 프롬프트로 만듭니다."""

    # 학습 포인트: lines 변수에 오른쪽에서 만든 값을 저장합니다.
    lines = ["당신은 초보자에게 쉽게 설명하는 AI 도우미입니다."]
    # 학습 포인트: 목록의 값을 하나씩 꺼내 같은 작업을 반복합니다.
    for item in history[-HISTORY_LIMIT:]:
        # 학습 포인트: speaker 변수에 오른쪽에서 만든 값을 저장합니다.
        speaker = "사용자" if item.role == "user" else "AI"
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        lines.append(f"{speaker}: {item.content}")
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    lines.append(f"사용자: {message}")
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    lines.append("AI:")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return "\n".join(lines)


# 학습 포인트: create_gemini_answer 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def create_gemini_answer(prompt: str) -> tuple[str, str]:
    # 학습 포인트: model 변수에 오른쪽에서 만든 값을 저장합니다.
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    # 학습 포인트: client 변수에 외부 서비스 클라이언트를 저장합니다.
    client = get_gemini_client()
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = client.models.generate_content(model=model, contents=prompt)
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except Exception as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(502, f"Gemini 호출 실패: {error}") from error
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return response.text or "", model


# 학습 포인트: chat 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def chat(request: ChatRequest) -> ChatResponse:
    """Redis의 이전 문맥을 사용해 Gemini 답변을 만들고 세션을 갱신합니다."""

    # 학습 포인트: conversation_id 변수에 오른쪽에서 만든 값을 저장합니다.
    conversation_id = str(request.conversation_id) if request.conversation_id else str(uuid4())
    # 학습 포인트: history 변수에 오른쪽에서 만든 값을 저장합니다.
    history = get_messages(conversation_id)
    answer, model = create_gemini_answer(make_prompt(history, request.message))
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    save_message(conversation_id, "user", request.message)
    # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
    save_message(conversation_id, "assistant", answer)

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ChatResponse(
        conversation_id=conversation_id,
        user_message=request.message,
        assistant_message=answer,
        model=model,
        context_messages=len(history),
        ttl_seconds=TTL_SECONDS,
    )


# 학습 포인트: clear_conversation 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def clear_conversation(conversation_id: str) -> int:
    """Redis에 저장된 대화 세션을 삭제합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return int(redis_command("del", redis_key(conversation_id)).get("result", 0))
