# Tool 없는 콘텐츠 제작 Supervisor 구현

## 요약

외부 검색, MCP, 함수 Tool 없이 OpenAI LLM과 이전 Agent 결과만 사용해 교육용
블로그 글을 제작한다. 실행 흐름은 `기획 → 작성 → 검토`이며, 첫 검토가 실패하면
한 번만 `수정 → 재검토`를 수행한다.

## Agent 구성

| Agent | 책임 | 출력 계약 |
| --- | --- | --- |
| `supervisor_agent` | 현재 State를 읽고 다음 Worker 또는 종료를 선택 | `ContentSupervisorDecision` |
| `planner_agent` | 독자, 학습 목표, 핵심 포인트와 문체를 설계 | `ContentPlanResult` |
| `writer_agent` | 검증된 기획에 따라 초안을 작성 | `ContentDraftResult` |
| `reviewer_agent` | 정확성, 구성, 가독성과 요구사항 충족 여부를 검토 | `ContentReviewResult` |
| `reviser_agent` | 첫 검토의 문제를 반영해 초안을 한 번 수정 | `ContentRevisionResult` |

반복되는 Agent 설정은 `my_orchestration.yaml`에 선언한다. 실행 순서, 수정 횟수,
최대 호출 수와 종료 조건은 `08_my_orchestration.py`에서 통제한다.

## 실행 흐름

첫 검토를 통과하면 다음 순서로 최대 7회 LLM을 호출한다.

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

두 번째 검토도 실패하면 `review_rejected`로 종료하며 추가 수정은 허용하지 않는다.

## 상태와 Guard

State에는 완료된 Agent 목록, 역할별 구조화 결과와 수정 횟수를 저장한다. Python은
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
2. 첫 검토 통과 시 Reviser 없이 정상 종료한다.
3. 첫 검토 실패 시 Reviser와 두 번째 Reviewer를 각각 한 번 실행한다.
4. 두 번째 검토 실패 시 `review_rejected`로 종료한다.
5. Supervisor가 현재 허용되지 않은 Worker나 조기 `finish`를 선택하면
   `invalid_transition`으로 차단한다.
6. LLM 오류가 발생하면 이후 Worker를 실행하지 않고 오류와 metadata를 Trace에 남긴다.
7. 호출 한도에 도달하면 `max_llm_calls`로 종료한다.

## 범위

- 모든 Agent의 기본 Provider는 OpenAI이다.
- 외부 Tool과 외부 사실 확인은 사용하지 않는다.
- README, 공용 계약과 기존 Supervisor 예제는 수정하지 않는다.
