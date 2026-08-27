"""LLM, RAG, MCP Tool을 함께 사용하는 기념일 시나리오 AI 에이전트입니다."""

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI

from backend._http_client import connect_to_anniversary_server
from backend.rag_data import retrieve_documents


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
INSTRUCTIONS = """
당신은 기념일 서프라이즈 시나리오를 만드는 AI 에이전트입니다.
사용자의 관계, 기념일, 예산, 성향, 준비 시간을 고려해 한국어로 답합니다.

날짜 계산, 선물 후보, 예산, 일정 시간처럼 정확한 값이 필요하면 반드시 제공된
MCP Tool을 호출하세요. Tool 결과가 없으면 가격이나 날짜를 지어내지 마세요.
최종 답변에는 다음 내용을 포함하세요.
1. 조건 요약
2. 시간 순서 시나리오
3. 사용한 선물과 예상 비용
4. 예산과 시간 검증 결과
5. 조건을 만족하지 못할 때의 대안
"""


def to_openai_tool(tool: Any) -> dict[str, Any]:
    """MCP Tool의 입력 스키마를 OpenAI Function Tool 형식으로 바꿉니다."""
    raw = tool.model_dump(by_alias=True)
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": raw["inputSchema"],
        "strict": False,
    }


def text_result(result: Any) -> str:
    """MCP Tool 결과에서 사람이 읽을 수 있는 텍스트만 꺼냅니다."""
    return "\n".join(content.text for content in result.content if hasattr(content, "text"))


def make_rag_context(question: str) -> str:
    """사용자 질문과 관련 있는 RAG 문서를 LLM에 전달할 텍스트로 만듭니다."""
    documents = retrieve_documents(question)
    if not documents:
        return "관련 RAG 문서를 찾지 못했습니다. 일반적인 배려 원칙으로 답하세요."
    return "\n\n".join(f"[{document['title']}]\n{document['content']}" for document in documents)


def tool_payload(trace: list[dict[str, Any]], tool_name: str) -> dict[str, Any] | None:
    """실행 기록에서 특정 Tool의 JSON 결과를 찾아 Python 딕셔너리로 바꿉니다."""
    for item in reversed(trace):
        if item["tool"] == tool_name:
            try:
                return json.loads(item["result"])
            except json.JSONDecodeError:
                return None
    return None


def print_terminal_result(result: dict[str, Any]) -> None:
    """JSON 전체 대신 사람이 읽기 쉬운 텍스트 화면으로 결과를 출력합니다."""
    line = "=" * 50
    print(line)
    print("🎉 기념일 서프라이즈 시나리오")
    print(line)

    print("\n[사용자 요청]")
    print(result["question"])

    print("\n[AI 추천 시나리오]")
    print(result["answer"].strip())

    budget = tool_payload(result["trace"], "calculate_budget")
    if budget:
        print("\n[예산 검증]")
        for item in budget["items"]:
            print(f"• {item['name']}: {item['price']:,}원")
        print("-" * 32)
        print(f"총 예상 비용: {budget['total']:,}원")
        if budget["is_within_budget"]:
            print(f"✅ 예산 {budget['budget_limit']:,}원 이내입니다. ({budget['remaining']:,}원 남음)")
        else:
            print(f"⚠️ 예산을 {-budget['remaining']:,}원 초과했습니다.")

    schedule = tool_payload(result["trace"], "validate_schedule")
    if schedule:
        print("\n[시간 검증]")
        print(f"총 예상 시간: {schedule['total_minutes']}분 / 가능 시간: {schedule['available_minutes']}분")
        if schedule["is_within_time"]:
            print("✅ 시간 안에 가능합니다.")
        else:
            print("⚠️ 가능 시간을 초과했습니다.")

    print("\n[RAG 참고]")
    titles = [line[1:-1] for line in result["rag_context"].splitlines() if line.startswith("[") and line.endswith("]")]
    if titles:
        for title in titles:
            print(f"• {title}")
    else:
        print("• 관련 문서를 찾지 못해 일반 가이드로 답변했습니다.")

    print("\n[Tool 실행 내역]")
    if result["trace"]:
        for item in result["trace"]:
            status = "⚠️" if item["is_error"] else "✅"
            print(f"{status} {item['tool']}")
    else:
        print("• 이번 요청에는 정확한 계산이 필요한 Tool 호출이 없었습니다.")
    print(line)


async def answer(question: str) -> dict[str, Any]:
    """질문 하나를 받아 RAG 검색, Tool 호출, LLM 답변 생성을 순서대로 수행합니다."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다. RUN.md의 환경 변수 설정을 확인하세요.")

    trace: list[dict[str, Any]] = []
    rag_context = make_rag_context(question)
    agent_input = f"사용자 요청:\n{question}\n\nRAG 참고 자료:\n{rag_context}"

    async with AsyncOpenAI() as client, connect_to_anniversary_server() as session:
        discovered = (await session.list_tools()).tools
        available = {tool.name for tool in discovered}
        openai_tools = [to_openai_tool(tool) for tool in discovered]
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            input=agent_input,
            tools=openai_tools,
            parallel_tool_calls=True,
        )

        for _ in range(5):
            tool_calls = [item for item in response.output if item.type == "function_call"]
            if not tool_calls:
                break

            tool_outputs = []
            for call in tool_calls:
                if call.name not in available:
                    raise ValueError(f"허용되지 않은 Tool입니다: {call.name}")
                arguments = json.loads(call.arguments)
                if not isinstance(arguments, dict):
                    raise ValueError("Tool arguments는 JSON 객체여야 합니다.")

                result = await session.call_tool(call.name, arguments)
                result_text = text_result(result)
                trace.append({
                    "tool": call.name,
                    "arguments": arguments,
                    "is_error": bool(result.isError),
                    "result": result_text,
                })
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": result_text,
                })

            response = await client.responses.create(
                model=OPENAI_MODEL,
                instructions=INSTRUCTIONS,
                previous_response_id=response.id,
                input=tool_outputs,
                tools=openai_tools,
                parallel_tool_calls=True,
            )
        else:
            raise RuntimeError("Tool 호출 횟수가 너무 많아 중단했습니다.")

    return {
        "question": question,
        "model": OPENAI_MODEL,
        "rag_context": rag_context,
        "discovered_tools": sorted(available),
        "trace": trace,
        "answer": response.output_text,
    }


async def main() -> None:
    """초보자가 바로 실행해 볼 수 있는 예시 요청을 실행합니다."""
    # question = (
    #     "사귄 지 100일이고 상대는 내향적이에요. 과한 서프라이즈는 부담스러워하고, "
    #     "예산은 8만 원입니다. 퇴근 후 3시간 안에 할 수 있는 계획을 만들어 주세요."
    # )
    question = "생일을 맞아 친구에게 줄 작은 선물을 추천해 주세요. 예산은 5만 원이고 준비 시간은 2시간입니다."

    result = await answer(question)
    print_terminal_result(result)


if __name__ == "__main__":
    asyncio.run(main())
