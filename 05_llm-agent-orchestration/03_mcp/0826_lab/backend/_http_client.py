"""팀 공용 Streamable HTTP MCP 서버 연결을 제공하는 도우미입니다."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")
MCP_SERVER_URL = os.getenv("TEAM_MCP_URL", "http://127.0.0.1:8000/mcp")


@asynccontextmanager
async def connect_to_anniversary_server():
    """환경 변수의 공용 MCP URL에 연결하고 초기화된 세션을 반환합니다.

    로컬 테스트는 기본 URL을 사용합니다. 팀 공용 서버를 사용할 때는 `.env`의
    ``TEAM_MCP_URL``을 서버 주소로 바꾸면 됩니다.
    """
    async with streamable_http_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session
