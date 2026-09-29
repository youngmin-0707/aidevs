# Handoff: Tool 없는 콘텐츠 제작 Supervisor

## 작업 요약

외부 검색, MCP, 함수 Tool 없이 OpenAI LLM과 이전 Agent 결과만 사용하는 콘텐츠 제작
Supervisor 예제를 추가했다. 교육용 블로그 글을 기획하고 작성한 뒤 품질을 검토하며,
첫 검토가 실패하면 한 번만 수정하고 재검토한다.

README와 기존 Supervisor 예제는 수정하지 않았다.

## 생성 및 변경 파일

- `08_my_orchestration.py`
  - 역할별 Pydantic 출력 계약
  - YAML 설정 로더와 필수 필드 검증
  - Supervisor 및 Worker LLM 호출
  - 조건부 수정 Loop와 Python Guard
  - State, 종료 결과와 실행 Trace 관리
  - 읽기 쉬운 CLI 출력 함수
- `my_orchestration.yaml`
  - Supervisor, Planner, Writer, Reviewer, Reviser 설정
  - 모든 Agent의 기본 Provider는 `openai`
- `08_my_orchestration_plan.md`
  - 역할, 실행 흐름, 계약, Guard와 검증 계획
- `handoff.md`
  - 현재 작업 상태와 후속 작업 참고사항

## Agent 흐름

첫 검토를 통과하면 최대 7회 LLM을 호출한다.

```text
Supervisor → Planner → Supervisor → Writer → Supervisor → Reviewer
           → Supervisor(finish)
```

첫 검토가 실패하면 수정과 재검토를 추가해 최대 11회 호출한다.

```text
Supervisor → Planner → Supervisor → Writer → Supervisor → Reviewer
           → Supervisor → Reviser → Supervisor → Reviewer
           → Supervisor(finish)
```

재검토도 실패하면 추가 수정 없이 `review_rejected`로 종료한다.

## 주요 실행 정책

- YAML은 Agent의 이름, 목표, 지시문, Provider와 출력 계약만 관리한다.
- Python은 실행 순서, 중복 실행, 수정 횟수, 최대 호출과 종료를 통제한다.
- Supervisor의 선택이 현재 State에서 허용된 행동과 다르면
  `invalid_transition`으로 차단한다.
- Reviewer는 최대 두 번, 다른 Worker는 최대 한 번 실행한다.
- 오류가 발생한 Agent 이후에는 다른 Worker를 실행하지 않는다.
- 실제 실행에는 Mock Mode가 없으며 `run_with_metadata()`가 OpenAI API를 호출한다.

## CLI 출력 개선

초기 구현은 최종 콘텐츠 딕셔너리와 Trace를 그대로 출력해 읽기 어려웠다. 현재는 다음
출력 함수로 표시 책임을 분리했다.

- `print_final_content()`
  - 제목과 본문을 문서 형태로 출력
  - 초안이면 핵심 포인트, 수정본이면 반영된 검토 의견을 목록으로 출력
- `print_trace()`
  - Agent별 실행 단계를 별도 블록으로 출력
  - Provider, 모델과 지연시간 표시
  - Supervisor의 다음 Agent 선택과 이유 표시
  - Reviewer의 통과 여부, 피드백과 문제점 표시
- `print_orchestration_result()`
  - 상태, 종료 이유, 최종 콘텐츠와 Trace를 순서대로 조합

반환되는 `status`, `reason`, `state`, `final_content`, `trace` 구조는 출력 개선 전과
동일하다.

## 검증 결과

- Python 문법 검사 통과
- YAML 로딩과 출력 계약 매핑 통과
- 가짜 LLM 응답을 런타임에 임시 주입한 제어 흐름 검사 결과
  - 첫 검토 통과: `completed`, Trace 7개, 수정 0회
  - 수정 후 통과: `completed`, Trace 11개, 수정 1회
  - 재검토 실패: `review_rejected`, Trace 10개, 수정 1회
- 사용자가 실제 OpenAI API로 실행한 정상 경로
  - `content_approved`로 완료
  - Supervisor, Planner, Writer, Reviewer, Supervisor 순서를 포함해 총 7회 호출

테스트에 사용한 가짜 응답은 소스 코드에 저장되어 있지 않다. 프로그램을 직접 실행하면
실제 OpenAI API를 호출한다.

## 실행 방법

과정 루트에서 다음 명령을 실행한다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
.\.venv\Scripts\Activate.ps1
python .\03_supervisor-and-routing\08_my_orchestration.py
```

실행 전 `.env` 또는 환경 변수에 유효한 `OPENAI_API_KEY`가 필요하다.

## 작업 시 주의사항

- 작업트리에는 이번 예제 외의 기존 사용자 변경이 존재한다.
- 특히 `01_rule_router.py`, `02_llm_router.py`, `04_supervisor_decision.py`,
  `worker_definitions.yaml`과 `shared/`를 임의로 되돌리거나 덮어쓰지 않는다.
- README는 사용자의 요청에 따라 수정하지 않는다.
