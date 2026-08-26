"""기념일 서프라이즈 시나리오 에이전트가 사용하는 MCP Tool 서버입니다."""

import sys
from datetime import date
from typing import Any

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "anniversary-scenario-tools",
    instructions="기념일 계산, 선물 검색, 예산과 일정 검증을 제공하는 교육용 MCP Server입니다.",
)

GIFT_CATALOG = [
    {"name": "질문 카드 세트", "price": 12_000, "tags": ["대화", "소규모"], "avoid_for": []},
    {"name": "손편지 키트", "price": 8_000, "tags": ["편지", "감성"], "avoid_for": []},
    {"name": "사진 인화권", "price": 18_000, "tags": ["사진", "추억"], "avoid_for": []},
    {"name": "취미 소품", "price": 45_000, "tags": ["취미", "실용"], "avoid_for": ["과한 서프라이즈 비선호"]},
    {"name": "커플 게임", "price": 25_000, "tags": ["대화", "게임"], "avoid_for": ["조용한 활동 선호"]},
]


@mcp.tool()
def calculate_anniversary(start_date: str, reference_date: str) -> dict[str, Any]:
    """관계 시작일과 기준일 사이의 날짜를 계산합니다.

    날짜는 ``YYYY-MM-DD`` 형식으로 입력합니다. LLM은 100일 또는 1주년처럼
    날짜를 정확히 계산해야 할 때 이 Tool을 사용합니다.
    """
    started = date.fromisoformat(start_date)
    reference = date.fromisoformat(reference_date)
    days = (reference - started).days
    if days < 0:
        raise ValueError("기준일은 관계 시작일보다 빠를 수 없습니다.")
    return {"days_together": days, "is_100_days": days == 100, "is_anniversary": days in {100, 365, 730, 1095}}


@mcp.tool()
def search_gift_candidates(tags: list[str], budget: int, avoid_for: list[str] | None = None) -> dict[str, Any]:
    """취향 태그와 예산에 맞는 Mock 선물 후보를 찾습니다.

    실제 쇼핑몰을 검색하지 않고 수업용 Mock 데이터만 반환합니다.
    """
    excluded = set(avoid_for or [])
    requested_tags = set(tags)
    items = [
        gift for gift in GIFT_CATALOG
        if gift["price"] <= budget
        and not excluded.intersection(gift["avoid_for"])
        and (not requested_tags or requested_tags.intersection(gift["tags"]))
    ]
    return {"items": items, "count": len(items), "source": "mock-gift-catalog"}


@mcp.tool()
def calculate_budget(items: list[dict[str, Any]], budget_limit: int) -> dict[str, Any]:
    """선택한 항목 가격을 합산하고 예산 초과 여부를 확인합니다.

    각 항목은 ``name``과 ``price``를 가져야 합니다. 최종 금액은 이 Tool의
    결과를 사용해, LLM이 비용을 추측하지 않도록 합니다.
    """
    total = sum(int(item["price"]) for item in items)
    return {"items": items, "total": total, "budget_limit": budget_limit, "remaining": budget_limit - total, "is_within_budget": total <= budget_limit}


@mcp.tool()
def validate_schedule(steps: list[dict[str, Any]], available_minutes: int) -> dict[str, Any]:
    """이벤트 단계의 시간을 더해 제한 시간 안에 가능한지 확인합니다.

    각 단계는 ``title``과 ``duration_minutes``를 가집니다.
    """
    total_minutes = sum(int(step["duration_minutes"]) for step in steps)
    return {"steps": steps, "total_minutes": total_minutes, "available_minutes": available_minutes, "remaining_minutes": available_minutes - total_minutes, "is_within_time": total_minutes <= available_minutes}


if __name__ == "__main__":
    print("MCP server is running on stdio...", file=sys.stderr)
    mcp.run(transport="stdio")
