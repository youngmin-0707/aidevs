# 기념일 시나리오 프로젝트 실행 방법

## 1. 폴더 구조

```text
0826_lab
├─ backend
│  ├─ api_server.py       # Swagger REST API, MCP Client
│  ├─ ai_agent.py         # LLM Agent
│  ├─ scenario_service.py # 공통 Mock 데이터·계산 로직
│  └─ rag_data.py         # RAG 문서와 검색 함수
├─ frontend
│  └─ app.py              # Streamlit 화면
└─ mcp_server
   └─ mcp_server.py       # Streamable HTTP MCP 서버
```

## 2. 최초 1회 준비

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install "mcp>=1.27,<2"
```

## 3. MCP 서버 실행

첫 번째 터미널에서 프로젝트 루트로 이동한 뒤 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\03_mcp\0826_lab
py -m mcp_server.mcp_server
```

MCP endpoint는 `http://192.100.200.198:8000/mcp`입니다.

팀원 접속을 위해 프로젝트 `.env`의 `TEAM_MCP_HOST`는 이미 `0.0.0.0`으로 설정되어 있습니다.
현재 서버 담당자 주소는 `http://192.100.200.198:8000/mcp`입니다.

## 4. Swagger FastAPI 실행

두 번째 터미널에서 MCP 서버 URL을 설정하고 FastAPI를 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\03_mcp\0826_lab
py -m uvicorn backend.api_server:app --reload --host 0.0.0.0 --port 8001
```

브라우저에서 Swagger를 엽니다.

```text
http://127.0.0.1:8001/docs
```

Swagger 요청은 FastAPI가 MCP Tool 호출로 전달합니다. 따라서 Swagger에서 테스트하면
첫 번째 터미널의 MCP 서버 로그에도 Tool 호출·완료 내용이 표시됩니다.

## 5. Streamlit 화면 실행

세 번째 터미널에서 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\03_mcp\0826_lab
py -m streamlit run .\frontend\app.py --server.address 0.0.0.0
```

브라우저에서 기본 Streamlit 주소 `http://localhost:8501`을 엽니다.

## 6. AI Agent 실행

`.env` 파일에 OpenAI 설정과 MCP URL을 넣습니다.

```env
OPENAI_API_KEY=발급받은_API_KEY
OPENAI_MODEL=gpt-4.1-mini
TEAM_MCP_URL=http://192.100.200.198:8000/mcp
```

네 번째 터미널에서 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\03_mcp\0826_lab
py -m backend.ai_agent
```

## 7. 팀 공유 시 포트

| 서비스 | 기본 포트 | 팀원 접속 주소 예시 |
| --- | ---: | --- |
| MCP 서버 | 8000 | `http://192.100.200.198:8000/mcp` |
| Swagger API | 8001 | `http://192.100.200.198:8001/docs` |
| Streamlit | 8501 | `http://192.100.200.198:8501` |

다른 PC에서 Swagger 또는 Streamlit을 보게 하려면 각각 `--host 0.0.0.0`,
`--server.address 0.0.0.0`으로 실행하고 Windows 방화벽에서 해당 TCP 포트를 허용합니다.
