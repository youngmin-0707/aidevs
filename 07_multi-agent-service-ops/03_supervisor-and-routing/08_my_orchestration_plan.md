# Tool 없는 콘텐츠 제작 Supervisor 구현

## 요약

외부 검색, MCP, 함수 Tool 없이 OpenAI LLM과 이전 Agent 결과만 사용해 교육용
블로그 글을 제작한다. `auto` 실행은 `기획 → 작성 → 검토`이며, 첫 검토가 실패하면
한 번만 `수정 → 재검토`를 수행한다. 연습 시나리오에서는 실제 검토 결과를 보존하면서
첫 검토 뒤 종료하거나 수정 경로를 실행할 수 있다.

## Agent 구성

| Agent | 책임 | 출력 계약 |
| --- | --- | --- |
| `supervisor_agent` | 현재 State를 읽고 다음 Worker 또는 종료를 선택 | `ContentSupervisorDecision` |
| `planner_agent` | 독자, 학습 목표, 핵심 포인트와 문체를 설계 | `ContentPlanResult` |
| `writer_agent` | 검증된 기획에 따라 초안을 작성 | `ContentDraftResult` |
| `reviewer_agent` | 정확성, 구성, 가독성과 요구사항 충족 여부를 검토 | `ContentReviewResult` |
| `reviser_agent` | 첫 검토의 문제를 반영하거나 연습 경로에서 초안을 한 번 다듬음 | `ContentRevisionResult` |

반복되는 Agent 설정은 `my_orchestration.yaml`에 선언한다. 실행 순서, 수정 횟수,
최대 호출 수와 종료 조건은 `08_my_orchestration.py`에서 통제한다.

## 실행 흐름

`auto` 시나리오에서 첫 검토를 통과하면 다음 순서로 7회 LLM을 호출한다.

```text
Supervisor → Planner → Supervisor → Writer → Supervisor → Reviewer
           → Supervisor(finish)
```

첫 검토가 실패하면 수정과 재검토를 한 번 추가해 최대 11회 호출한다.

```text
Supervisor → Planner → Supervisor → Writer → Supervisor → Reviewer
           → Supervisor → Reviser → Supervisor → Reviewer
           → Supervisor(finish)
```

두 번째 검토도 실패하면 10회 호출 후 `review_rejected`로 종료하며 추가 수정은 허용하지 않는다.

## 실행 시나리오

| 시나리오 | 첫 검토 뒤 행동 | 결과와 호출 수 |
| --- | --- | --- |
| `auto` | 실제 `passed` 값에 따라 종료 또는 수정 | 통과 시 7회, 실패 후 재검토까지 최대 11회 |
| `first-pass` | 첫 검토 뒤 Supervisor가 종료 | 통과 또는 거절로 7회 |
| `revision` | 첫 검토 뒤 반드시 한 번 수정하고 재검토 | 첫 검토가 통과해도 최대 11회 |
| `alternate` | 한 명령에서 `first-pass`, `revision` 순서로 반복 | 실행별 7회와 최대 11회 |

파일을 옵션 없이 실행하면 `alternate --runs 2`를 사용한다. 따라서 첫 실행은
첫 검토 뒤 7회에 끝나고, 이어지는 두 번째 실행은 수정·재검토까지 최대 11회
호출한다. 실제 검토 결과에 따른 한 번의 실행만 원하면 `--scenario auto`를 지정한다.

`revision`에서 첫 검토가 통과했다면 이를 실패로 변경하지 않는다. Reviser는 연습용
요청에 따라 설명이나 예시를 다듬고, State의 `revision_reason`과 Trace의 `Route`에
`scenario_requested`를 기록한다. 첫 검토가 실제로 실패한 경우에는
`first_review_failed`를 기록한다. `first-pass`에서 검토가 실패했다면 7번째
Supervisor 호출 후 `review_rejected`로 종료하며 승인된 콘텐츠를 반환하지 않는다.

과정 루트에서 실행하는 예:

```bash
cd /Users/son/개발/aidevs/07_multi-agent-service-ops
./.venv/bin/python 03_supervisor-and-routing/08_my_orchestration.py
./.venv/bin/python 03_supervisor-and-routing/08_my_orchestration.py --scenario auto
./.venv/bin/python 03_supervisor-and-routing/08_my_orchestration.py --scenario first-pass
./.venv/bin/python 03_supervisor-and-routing/08_my_orchestration.py --scenario revision
./.venv/bin/python 03_supervisor-and-routing/08_my_orchestration.py --scenario alternate --runs 2
```

`alternate`는 기본값으로 두 번 실행하고 첫 실행은 7회, 두 번째는 최대 11회
호출한다. `--runs`로 횟수를 바꾸면 이 두 시나리오를 순서대로 반복한다. 각 실행은
실제 API를 호출하므로 여러 번 실행하면 그만큼 호출량이 늘어난다.

수정·재검토 경로만 확인하려면 `--scenario revision` 명령을 사용한다. 기본 실행은
두 경로를 연속 실행하므로 호출 횟수와 대기 시간이 더 길다. 현재 프로그램은 각 실행이
끝난 뒤 결과와 Trace를 한꺼번에 출력한다. 따라서 `=== 실행 1/2 ===` 다음에
한동안 출력이 없어도 API 응답을 기다리는 중일 수 있다. 이때 `Ctrl+C`로 중단하면
`KeyboardInterrupt`가 표시되며, 이는 사용자가 실행을 중단했다는 뜻이다.

## 상태와 Guard

State에는 시나리오, 완료된 Agent 목록, 역할별 구조화 결과, 수정 횟수와 수정 사유를 저장한다. Python은
State에서 현재 허용되는 다음 행동을 계산하고 Supervisor의 선택과 일치하는지 확인한다.

- 허용 순서와 조기 `finish` 검증
- Planner, Writer, Reviser의 중복 실행 차단
- Reviewer를 최대 두 번으로 제한
- Worker 결과의 Agent identity 검증
- Supervisor 또는 Worker 오류 이후 실행 중단
- 최대 LLM 호출 수 통제
- 검토 통과 시 빈 문제 목록, 실패 시 한 개 이상의 문제 강제

종료 결과는 `status`, `reason`, `state`, `final_content`, `trace`를 포함한다. 수정이
없으면 Writer 초안, 수정이 있으면 Reviser 결과를 최종 콘텐츠로 사용한다.

## 검증 시나리오

1. YAML에 필수 필드가 없거나 알 수 없는 출력 계약이 있으면 시작 전에 실패한다.
2. `auto`에서 첫 검토 통과 시 Reviser 없이 정상 종료한다.
3. `auto`에서 첫 검토 실패 시 Reviser와 두 번째 Reviewer를 각각 한 번 실행한다.
4. `first-pass`는 첫 검토 결과를 그대로 두고 7회에 종료한다.
5. `revision`은 첫 검토 통과 여부와 관계없이 수정과 재검토를 수행한다.
6. `alternate --runs 2`는 앞의 두 연습 경로를 순서대로 실행한다.
7. 두 번째 검토 실패 시 `review_rejected`로 종료한다.
8. Supervisor가 현재 허용되지 않은 Worker나 조기 `finish`를 선택하면
   `invalid_transition`으로 차단한다.
9. LLM 오류가 발생하면 이후 Worker를 실행하지 않고 오류와 metadata를 Trace에 남긴다.
10. 호출 한도에 도달하면 `max_llm_calls`로 종료한다.

## 범위

- 모든 Agent의 기본 Provider는 OpenAI이다.
- 외부 Tool과 외부 사실 확인은 사용하지 않는다.
- README, 공용 계약과 기존 Supervisor 예제는 수정하지 않는다.
