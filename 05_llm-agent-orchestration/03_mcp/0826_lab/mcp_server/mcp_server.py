"""팀 공용 기념일 시나리오 Streamable HTTP MCP 서버입니다."""

import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from backend.scenario_service import (
    calculate_anniversary as calculate_anniversary_service,
    calculate_budget as calculate_budget_service,
    search_gift_candidates as search_gift_candidates_service,
    validate_schedule as validate_schedule_service,
)

PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")
MCP_HOST = os.getenv("TEAM_MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("TEAM_MCP_PORT", "8000"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "anniversary-scenario-tools",
    instructions="기념일 계산, 선물 검색, 예산과 일정 검증을 제공하는 팀 공용 MCP Server입니다.",
    host=MCP_HOST,
    port=MCP_PORT,
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def calculate_anniversary(start_date: str, reference_date: str) -> dict[str, Any]:
    """관계 시작일과 기준일 사이의 날짜를 계산합니다."""
    logger.info("MCP Tool 호출: calculate_anniversary(start_date=%s, reference_date=%s)", start_date, reference_date)
    result = calculate_anniversary_service(start_date, reference_date)
    logger.info("MCP Tool 완료: calculate_anniversary(days_together=%s)", result["days_together"])
    return result


@mcp.tool()
def search_gift_candidates(
    tags: list[str],
    budget: int,
    avoid_for: list[str] | None = None,
) -> dict[str, Any]:
    """취향 태그와 예산에 맞는 Mock 선물 후보를 찾습니다."""
    logger.info("MCP Tool 호출: search_gift_candidates(tags=%s, budget=%s)", tags, budget)
    result = search_gift_candidates_service(tags, budget, avoid_for)
    logger.info("MCP Tool 완료: search_gift_candidates(count=%s)", result["count"])
    return result


@mcp.tool()
def calculate_budget(items: list[dict[str, Any]], budget_limit: int) -> dict[str, Any]:
    """선택한 항목 가격을 합산하고 예산 초과 여부를 확인합니다."""
    logger.info("MCP Tool 호출: calculate_budget(items=%s, budget_limit=%s)", len(items), budget_limit)
    result = calculate_budget_service(items, budget_limit)
    logger.info("MCP Tool 완료: calculate_budget(total=%s, within_budget=%s)", result["total"], result["is_within_budget"])
    return result


@mcp.tool()
def validate_schedule(steps: list[dict[str, Any]], available_minutes: int) -> dict[str, Any]:
    """이벤트 단계의 시간을 더해 제한 시간 안에 가능한지 확인합니다."""
    logger.info("MCP Tool 호출: validate_schedule(steps=%s, available_minutes=%s)", len(steps), available_minutes)
    result = validate_schedule_service(steps, available_minutes)
    logger.info("MCP Tool 완료: validate_schedule(total_minutes=%s, within_time=%s)", result["total_minutes"], result["is_within_time"])
    return result


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
