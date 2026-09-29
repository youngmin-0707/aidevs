"""Lab 03-08: Tool 없이 조건부 수정 Loop를 가진 콘텐츠 제작 Team을 실행합니다.

Supervisor와 Worker는 구조화된 LLM 결과와 이전 Agent Context만 사용합니다.
YAML은 Agent 선언을 관리하고 Python은 실행 순서, 수정 횟수와 종료 조건을 통제합니다.
"""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator

from shared.travel_llm import run_with_metadata


CONFIG_FILE = Path(__file__).resolve().parent / "my_orchestration.yaml"


class ContentSupervisorDecision(BaseModel):
    agent_id: Literal["supervisor_agent"] = "supervisor_agent"
    next_agent: Literal[
        "planner_agent",
        "writer_agent",
        "reviewer_agent",
        "reviser_agent",
        "finish",
    ]
    instruction: str = Field(min_length=1)
    context_keys: list[str] = Field(default_factory=list, max_length=5)
    reason: str = Field(min_length=1)


class ContentPlanResult(BaseModel):
    agent_id: Literal["planner_agent"] = "planner_agent"
    title: str = Field(min_length=1)
    audience: str = Field(min_length=1)
    learning_objectives: list[str] = Field(min_length=1, max_length=5)
    key_points: list[str] = Field(min_length=3, max_length=7)
    tone: str = Field(min_length=1)


class ContentDraftResult(BaseModel):
    agent_id: Literal["writer_agent"] = "writer_agent"
    title: str = Field(min_length=1)
    body: str = Field(min_length=100)
    covered_points: list[str] = Field(min_length=1, max_length=7)


class ContentReviewResult(BaseModel):
    agent_id: Literal["reviewer_agent"] = "reviewer_agent"
    passed: bool
    feedback: str = Field(min_length=1)
    issues: list[str] = Field(default_factory=list, max_length=7)

    @model_validator(mode="after")
    def issues_must_match_decision(self) -> "ContentReviewResult":
        if self.passed and self.issues:
            raise ValueError("통과한 검토 결과에는 issue가 없어야 합니다.")
        if not self.passed and not self.issues:
            raise ValueError("실패한 검토 결과에는 최소 한 개의 issue가 필요합니다.")
        return self


class ContentRevisionResult(BaseModel):
    agent_id: Literal["reviser_agent"] = "reviser_agent"
    title: str = Field(min_length=1)
    body: str = Field(min_length=100)
    applied_feedback: list[str] = Field(min_length=1, max_length=7)


CONTRACTS: dict[str, type[BaseModel]] = {
    "ContentSupervisorDecision": ContentSupervisorDecision,
    "ContentPlanResult": ContentPlanResult,
    "ContentDraftResult": ContentDraftResult,
    "ContentReviewResult": ContentReviewResult,
    "ContentRevisionResult": ContentRevisionResult,
}


def load_agent_definitions() -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    document = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("YAML 최상위 값은 객체여야 합니다.")

    supervisor = document.get("supervisor")
    workers = document.get("workers")
    if not isinstance(supervisor, dict):
        raise ValueError("YAML에 supervisor 설정이 없습니다.")
    if not isinstance(workers, dict) or not workers:
        raise ValueError("YAML에 workers 설정이 없습니다.")

    required_supervisor_fields = {
        "agent_id",
        "name",
        "goal",
        "instructions",
        "provider",
        "output_contract",
    }
    required_worker_fields = {"name", "goal", "instructions", "provider", "output_contract"}
    expected_workers = {"planner_agent", "writer_agent", "reviewer_agent", "reviser_agent"}

    missing = required_supervisor_fields - set(supervisor)
    if missing:
        raise ValueError(f"supervisor에 필요한 설정이 없습니다: {sorted(missing)}")
    if supervisor["agent_id"] != "supervisor_agent":
        raise ValueError("supervisor.agent_id는 supervisor_agent여야 합니다.")
    if set(workers) != expected_workers:
        raise ValueError(f"workers는 다음 Agent와 정확히 일치해야 합니다: {sorted(expected_workers)}")

    for agent_id, config in workers.items():
        if not isinstance(config, dict):
            raise ValueError(f"{agent_id} 설정은 객체여야 합니다.")
        missing = required_worker_fields - set(config)
        if missing:
            raise ValueError(f"{agent_id}에 필요한 설정이 없습니다: {sorted(missing)}")

    all_agents = {"supervisor_agent": supervisor, **workers}
    for agent_id, config in all_agents.items():
        contract_name = config["output_contract"]
        if contract_name not in CONTRACTS:
            raise ValueError(f"{agent_id}의 알 수 없는 출력 계약입니다: {contract_name}")
        if config["provider"] != "openai":
            raise ValueError(f"{agent_id}의 Provider는 openai여야 합니다.")

    return supervisor, workers


def expected_next_action(state: dict[str, object]) -> str | None:
    outputs = state["outputs"]
    if "planner_agent" not in outputs:
        return "planner_agent"
    if "writer_agent" not in outputs:
        return "writer_agent"
    if "review_1" not in outputs:
        return "reviewer_agent"

    first_review = outputs["review_1"]
    if first_review["passed"]:
        return "finish"
    if "reviser_agent" not in outputs:
        return "reviser_agent"
    if "review_2" not in outputs:
        return "reviewer_agent"

    second_review = outputs["review_2"]
    return "finish" if second_review["passed"] else None


def context_for_worker(agent_id: str, outputs: dict[str, object]) -> dict[str, object]:
    if agent_id == "planner_agent":
        return {}
    if agent_id == "writer_agent":
        return {"plan": outputs["planner_agent"]}
    if agent_id == "reviser_agent":
        return {
            "plan": outputs["planner_agent"],
            "draft": outputs["writer_agent"],
            "review": outputs["review_1"],
        }
    if agent_id == "reviewer_agent" and "reviser_agent" in outputs:
        return {
            "plan": outputs["planner_agent"],
            "content": outputs["reviser_agent"],
            "previous_review": outputs["review_1"],
        }
    if agent_id == "reviewer_agent":
        return {
            "plan": outputs["planner_agent"],
            "content": outputs["writer_agent"],
        }
    raise ValueError(f"Context를 만들 수 없는 Worker입니다: {agent_id}")


def supervisor_agent(
    request: str,
    state: dict[str, object],
    expected_next: str,
    config: dict[str, str],
) -> dict:
    prompt = f"""당신은 {config['agent_id']}입니다.
이름: {config['name']}
Goal: {config['goal']}
Instructions: {config['instructions']}
직접 콘텐츠를 기획·작성·검토·수정하지 마세요.
현재 State: {state}
현재 허용된 다음 행동: {expected_next}
사용자 요청: {request}
ContentSupervisorDecision 계약으로 반환하고 agent_id는 supervisor_agent로 작성하세요."""
    return run_with_metadata(config["provider"], prompt, ContentSupervisorDecision)


def selected_worker_agent(
    agent_id: str,
    request: str,
    instruction: str,
    outputs: dict[str, object],
    workers: dict[str, dict[str, str]],
) -> dict:
    if agent_id not in workers:
        raise ValueError(f"허용되지 않은 Worker입니다: {agent_id}")

    worker = workers[agent_id]
    schema = CONTRACTS[worker["output_contract"]]
    context = context_for_worker(agent_id, outputs)
    prompt = f"""당신은 {agent_id}입니다.
이름: {worker['name']}
Goal: {worker['goal']}
Instructions: {worker['instructions']}
Supervisor 지시: {instruction}
사용자 요청: {request}
이전 Agent Context: {context}
{worker['output_contract']} 계약으로 반환하고 agent_id는 반드시 {agent_id}로 작성하세요.
외부 Tool이나 외부 정보를 사용하지 마세요."""
    return run_with_metadata(worker["provider"], prompt, schema)


def trace_event(step: int, actor: str, response: dict) -> dict[str, object]:
    return {
        "step": step,
        "actor": actor,
        "provider": response["provider_requested"],
        "model": response["model"],
        "latency_ms": response["latency_ms"],
        "result": response["result"],
        "error": response["error"],
    }


def orchestration_result(
    status: str,
    reason: str,
    state: dict[str, object],
    trace: list[dict[str, object]],
) -> dict[str, object]:
    final_content = None
    if status == "completed":
        outputs = state["outputs"]
        final_content = outputs.get("reviser_agent", outputs.get("writer_agent"))
    return {
        "status": status,
        "reason": reason,
        "state": state,
        "final_content": final_content,
        "trace": trace,
    }


def content_team_agent(request: str, max_llm_calls: int = 11) -> dict[str, object]:
    supervisor, workers = load_agent_definitions()
    state: dict[str, object] = {
        "completed_agents": [],
        "outputs": {},
        "revision_count": 0,
    }
    trace: list[dict[str, object]] = []

    while len(trace) < max_llm_calls:
        expected_next = expected_next_action(state)
        if expected_next is None:
            return orchestration_result("failed", "review_rejected", state, trace)

        decision = supervisor_agent(request, state, expected_next, supervisor)
        trace.append(trace_event(len(trace) + 1, "supervisor_agent", decision))
        if decision["error"]:
            return orchestration_result("failed", "supervisor_failed", state, trace)
        if decision["result"]["agent_id"] != "supervisor_agent":
            return orchestration_result("blocked", "invalid_transition", state, trace)

        selected = decision["result"]["next_agent"]
        if selected != expected_next:
            return orchestration_result("blocked", "invalid_transition", state, trace)
        if selected == "finish":
            return orchestration_result("completed", "content_approved", state, trace)

        completed_agents = state["completed_agents"]
        allowed_runs = 2 if selected == "reviewer_agent" else 1
        if completed_agents.count(selected) >= allowed_runs:
            return orchestration_result("blocked", "duplicate_worker", state, trace)
        if len(trace) >= max_llm_calls:
            break

        worker = selected_worker_agent(
            selected,
            request,
            decision["result"]["instruction"],
            state["outputs"],
            workers,
        )
        trace.append(trace_event(len(trace) + 1, selected, worker))
        if worker["error"]:
            return orchestration_result("failed", "worker_failed", state, trace)
        if worker["result"]["agent_id"] != selected:
            return orchestration_result("failed", "worker_failed", state, trace)

        completed_agents.append(selected)
        if selected == "reviewer_agent":
            review_number = completed_agents.count("reviewer_agent")
            state["outputs"][f"review_{review_number}"] = worker["result"]
        else:
            state["outputs"][selected] = worker["result"]
            if selected == "reviser_agent":
                state["revision_count"] += 1

    return orchestration_result("failed", "max_llm_calls", state, trace)


def print_final_content(final_content: dict[str, object] | None) -> None:
    print("\n=== 최종 콘텐츠 ===")
    if final_content is None:
        print("승인된 최종 콘텐츠가 없습니다.")
        return

    print(f"\n# {final_content['title']}\n")
    print(final_content["body"])

    list_fields = (
        ("covered_points", "포함된 핵심 포인트"),
        ("applied_feedback", "반영된 검토 의견"),
    )
    for field_name, label in list_fields:
        values = final_content.get(field_name)
        if values:
            print(f"\n--- {label} ---")
            for value in values:
                print(f"- {value}")


def print_trace(trace: list[dict[str, object]]) -> None:
    print("\n=== 실행 Trace ===")
    for event in trace:
        print(f"\n[{event['step']:02d}] {event['actor']}")
        print(f"  Provider : {event['provider']}")
        print(f"  Model    : {event['model']}")
        print(f"  Latency  : {event['latency_ms']} ms")

        if event["error"]:
            print(f"  Error    : {event['error']}")
            continue

        result = event["result"]
        if event["actor"] == "supervisor_agent":
            print(f"  Decision : {result['next_agent']}")
            print(f"  Reason   : {result['reason']}")
        elif event["actor"] == "reviewer_agent":
            print(f"  Passed   : {result['passed']}")
            print(f"  Feedback : {result['feedback']}")
            for issue in result["issues"]:
                print(f"  Issue    : {issue}")
        else:
            print(f"  Output   : {result['title']}")


def print_orchestration_result(result: dict[str, object]) -> None:
    print("=== 실행 결과 ===")
    print(f"상태      : {result['status']}")
    print(f"종료 이유 : {result['reason']}")
    print_final_content(result["final_content"])
    print_trace(result["trace"])


if __name__ == "__main__":
    result = content_team_agent(
        "멀티 에이전트 시스템에서 Router와 Supervisor의 차이를 초보 개발자에게 "
        "설명하는 교육용 블로그 글을 작성해 주세요."
    )
    print_orchestration_result(result)
