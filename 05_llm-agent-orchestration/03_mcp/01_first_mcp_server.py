"""stdio로 실행하는 간단한 여행 MCP Server입니다."""

import sys
from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "travel-tools",
    instructions="현재 도시와 호텔 정보를 제공하는 교육용 MCP Server입니다.",
)


@mcp.tool()
def get_hotels(city: Literal["부산", "서울"], view:str) -> dict:
    """도시와 뷰 조건으로 호텔을 검색합니다."""
    normalized = city.strip()
   
    return [
             {"name": "바다호텔", "city": "부산", "view": "view", "price": 120_000}, 
             {"name": "시티호텔", "city": "부산", "view": "view", "price": 140_000}
    ]
    


@mcp.tool()
def get_current_weather(city: Literal["부산", "서울"]) -> dict:
    """도시의 현재 날씨를 조회합니다."""
    normalized = city.strip()
    if not normalized:
        raise ValueError("city는 빈 문자열일 수 없습니다.")
    return {
        "city": normalized,
        "condition": "맑음",
        "temperature_c": 24,
        "source": "travel-weather-service",
    }


@mcp.tool()
def search_hotels(
    city: Literal["부산", "서울"],
    max_price: int = 150_000,
) -> dict:
    """도시와 1박 최대 가격으로 호텔을 검색합니다."""
    if not city.strip():
        raise ValueError("city는 빈 문자열일 수 없습니다.")
    if max_price < 1:
        raise ValueError("max_price는 1 이상이어야 합니다.")
    hotels = [
        {"name": "바다 호텔", "city": "부산", "price": 120_000},
        {"name": "시티 호텔", "city": "서울", "price": 140_000},
    ]
    matches = [
        hotel for hotel in hotels
        if hotel["city"] == city.strip() and hotel["price"] <= max_price
    ]
    return {"items": matches, "source": "travel-hotel-catalog"}


@mcp.resource("travel://policy/baggage")
def baggage_policy() -> str:
    """교육용 국내선 위탁 수하물 정책을 제공합니다."""
    return "교육용 국내선의 위탁 수하물은 15kg까지 허용됩니다."


if __name__ == "__main__":
    print("MCP server is running on stdio...", file=sys.stderr)
    mcp.run(transport="stdio")
