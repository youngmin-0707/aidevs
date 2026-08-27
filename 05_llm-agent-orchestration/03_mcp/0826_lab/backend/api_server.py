"""Swagger 요청을 공용 MCP 서버 Tool로 전달하는 FastAPI 백엔드입니다."""

import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from pydantic import BaseModel, Field


PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")
MCP_SERVER_URL = os.getenv("TEAM_MCP_URL", "http://127.0.0.1:8000/mcp")

app = FastAPI(
    title="기념일 서프라이즈 시나리오 API",
    description="Swagger 요청을 공용 MCP 서버의 Tool로 전달합니다.",
    version="1.1.0",
)


class AnniversaryRequest(BaseModel):
    """기념일 계산 API에 전달할 시작일과 기준일입니다."""

    start_date: str = Field(examples=["2026-05-18"])
    reference_date: str = Field(examples=["2026-08-26"])


class GiftSearchRequest(BaseModel):
    """선물 후보 검색 API에 전달할 취향과 예산 조건입니다."""

    tags: list[str] = Field(examples=[["대화", "소규모"]])
    budget: int = Field(ge=1, examples=[80_000])
    avoid_for: list[str] = Field(default_factory=list, examples=[["과한 서프라이즈 비선호"]])


class BudgetItem(BaseModel):
    """예산 계산에 포함할 선물 또는 소품 항목입니다."""

    name: str = Field(examples=["질문 카드 세트"])
    price: int = Field(ge=0, examples=[12_000])


class BudgetRequest(BaseModel):
    """선택 항목과 최대 예산입니다."""

    items: list[BudgetItem]
    budget_limit: int = Field(ge=1, examples=[80_000])


class ScheduleStep(BaseModel):
    """일정 검증에 포함할 하나의 이벤트 단계입니다."""

    title: str = Field(examples=["손편지 전달"])
    duration_minutes: int = Field(ge=1, examples=[15])


class ScheduleRequest(BaseModel):
    """이벤트 단계와 사용자에게 가능한 총 시간입니다."""

    steps: list[ScheduleStep]
    available_minutes: int = Field(ge=1, examples=[180])


def result_to_dict(result: Any) -> dict[str, Any]:
    """MCP Tool 결과를 FastAPI가 반환할 JSON 딕셔너리로 바꿉니다."""
    if result.structuredContent is not None:
        return dict(result.structuredContent)

    text = "\n".join(content.text for content in result.content if hasattr(content, "text"))
    return json.loads(text)


async def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Swagger 요청을 Streamable HTTP MCP 서버의 Tool 호출로 전달합니다."""
    try:
        async with streamable_http_client(MCP_SERVER_URL) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"MCP 서버 연결 또는 Tool 호출 실패: {error}",
        ) from error

    if result.isError:
        message = "\n".join(
            content.text for content in result.content if hasattr(content, "text")
        )
        raise HTTPException(status_code=400, detail=message)
    return result_to_dict(result)


@app.get("/health")
def health() -> dict[str, str]:
    """FastAPI 서버가 실행 중인지 빠르게 확인합니다."""
    return {"status": "ok", "mcp_server_url": MCP_SERVER_URL}


@app.post("/anniversary")
async def anniversary(request: AnniversaryRequest) -> dict[str, Any]:
    """MCP의 기념일 계산 Tool을 호출합니다."""
    return await call_mcp_tool("calculate_anniversary", request.model_dump())


@app.post("/gifts")
async def gifts(request: GiftSearchRequest) -> dict[str, Any]:
    """MCP의 Mock 선물 검색 Tool을 호출합니다."""
    return await call_mcp_tool("search_gift_candidates", request.model_dump())


@app.post("/budget")
async def budget(request: BudgetRequest) -> dict[str, Any]:
    """MCP의 예산 검증 Tool을 호출합니다."""
    return await call_mcp_tool(
        "calculate_budget",
        {"items": [item.model_dump() for item in request.items], "budget_limit": request.budget_limit},
    )


@app.post("/schedule")
async def schedule(request: ScheduleRequest) -> dict[str, Any]:
    """MCP의 시간 검증 Tool을 호출합니다."""
    return await call_mcp_tool(
        "validate_schedule",
        {"steps": [step.model_dump() for step in request.steps], "available_minutes": request.available_minutes},
    )
