# 기념일 서프라이즈 시나리오 AI 에이전트 실행 방법

## 1. 이 프로젝트가 하는 일

사용자의 기념일, 예산, 상대 성향, 준비 가능 시간을 받아 다음 흐름으로 이벤트 시나리오를 만듭니다.

```text
사용자 질문
  → RAG 문서 검색
  → LLM이 필요한 MCP Tool 선택
  → 기념일·선물·예산·시간 검증
  → 최종 시나리오 출력
```

프로젝트는 실제 쇼핑몰이나 예약 시스템을 사용하지 않습니다. 선물과 가격은 모두 수업용 Mock 데이터입니다.

## 2. 파일 역할

| 파일 | 역할 |
| --- | --- |
| `mcp_server.py` | 날짜 계산, 선물 검색, 예산·시간 검증 Tool을 제공하는 MCP 서버 |
| `_stdio_client.py` | Python 프로그램과 MCP 서버를 stdio로 연결하는 도우미 |
| `rag_data.py` | 기념일·성향 가이드 문서와 간단한 RAG 검색 함수 |
| `ai_agent.py` | LLM, RAG, MCP Tool 결과를 종합해 최종 시나리오를 만드는 프로그램 |

## 3. 최초 1회 준비

PowerShell에서 과정 루트로 이동해 가상환경을 활성화합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\.venv\Scripts\Activate.ps1
```

필요한 패키지를 설치합니다. `mcp`는 현재 `requirements.txt`에 없을 수 있으므로 별도로 설치합니다.

```powershell
python -m pip install -r requirements.txt
python -m pip install "mcp>=1.27,<2"
```

과정 루트의 `.env` 파일에 OpenAI API 키를 설정합니다.

```env
OPENAI_API_KEY=발급받은_API_KEY
OPENAI_MODEL=gpt-4.1-mini
```

`.env` 파일이 없다면 `.env.example`을 참고해 새로 만듭니다. API 키는 Git에 올리면 안 됩니다.

## 4. 실행

`0826_lab` 폴더로 이동한 후, AI 에이전트만 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\03_mcp\0826_lab
python .\ai_agent.py
```

`ai_agent.py`가 MCP 서버를 자식 프로세스로 자동 실행합니다. 따라서 보통은 `mcp_server.py`를 별도 터미널에서 직접 실행하지 않습니다.

정상 실행되면 별도 라이브러리 없이 `print()`로 만든 텍스트 화면에서 아래 내용을 확인할 수 있습니다.

- 사용자 요청과 AI 추천 시나리오
- 예산과 시간 검증 결과
- RAG 참고 문서 제목
- LLM이 선택해 호출한 MCP Tool 목록

## 5. 다른 질문으로 실행하기

`ai_agent.py`의 `main()` 함수에 있는 `question` 문장을 바꾼 뒤 다시 실행합니다.

```python
question = "생일을 맞아 친구에게 줄 작은 선물을 추천해 주세요. 예산은 5만 원이고 준비 시간은 2시간입니다."
```

LLM이 정확한 날짜·가격·시간 검증이 필요하다고 판단하면 MCP Tool을 호출합니다. Tool 호출 내역은 `trace`에서 볼 수 있습니다.

## 6. 문법 검사와 문제 해결

실행 전에 문법만 검사하려면 다음 명령을 사용합니다.

```powershell
python -m py_compile .\mcp_server.py .\rag_data.py .\ai_agent.py .\_stdio_client.py
```

### `ModuleNotFoundError: No module named 'mcp'`

가상환경이 활성화된 상태인지 확인한 뒤 아래 명령을 실행합니다.

```powershell
python -m pip install "mcp>=1.27,<2"
```

### `OPENAI_API_KEY가 필요합니다`

과정 루트 `C:\aidevs\05_llm-agent-orchestration\.env` 파일에 API 키가 있는지 확인합니다.

### `McpError: Connection closed`

`mcp_server.py`의 문법 오류 또는 가상환경 문제일 수 있습니다. 먼저 6장의 문법 검사 명령을 실행합니다. 서버 시작 메시지는 `stderr`로 출력되어야 하며, 일반 `print()`를 stdout에 추가하면 stdio MCP 통신이 깨질 수 있습니다.
