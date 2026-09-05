"""팀원이 브라우저에서 기념일 Tool 결과를 확인하는 Streamlit 화면입니다."""

import os
from pathlib import Path

import httpx
import streamlit as st
from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")
API_URL = os.getenv("TEAM_API_URL", "http://127.0.0.1:8001")


def call_api(path: str, payload: dict) -> dict | None:
    """FastAPI 서버에 요청을 보내고 오류가 있으면 화면에 알려줍니다."""
    try:
        response = httpx.post(f"{API_URL}{path}", json=payload, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as error:
        st.error(f"API 서버에 연결하지 못했습니다: {error}")
        return None


st.set_page_config(page_title="기념일 시나리오 도구", page_icon="🎉")
st.title("🎉 기념일 서프라이즈 시나리오 도구")
st.caption("MCP Tool과 같은 Mock 데이터를 사용하는 팀 확인용 화면입니다.")
st.info(f"연결 API: {API_URL}")

anniversary_tab, gifts_tab, budget_tab, schedule_tab = st.tabs(
    ["기념일 계산", "선물 검색", "예산 검증", "시간 검증"]
)

with anniversary_tab:
    st.subheader("함께한 날짜 계산")
    st.write("관계 시작일과 기준일을 입력하면 100일·기념일 여부를 확인합니다.")
    start_date = st.date_input("관계 시작일")
    reference_date = st.date_input("기준일")
    if st.button("기념일 계산하기", key="anniversary"):
        result = call_api(
            "/anniversary",
            {"start_date": start_date.isoformat(), "reference_date": reference_date.isoformat()},
        )
        if result:
            st.success(f"함께한 날짜: {result['days_together']}일")
            st.json(result)

with gifts_tab:
    st.subheader("Mock 선물 후보 검색")
    st.write("태그와 예산에 맞는 수업용 Mock 선물을 조회합니다.")
    tags = st.multiselect("선호 태그", ["대화", "소규모", "편지", "감성", "사진", "추억", "취미", "실용", "게임"])
    gift_budget = st.number_input("선물 예산", min_value=1, value=80_000, step=1_000)
    avoid = st.multiselect("피해야 할 조건", ["과한 서프라이즈 비선호", "조용한 활동 선호"])
    if st.button("선물 후보 찾기", key="gifts"):
        result = call_api("/gifts", {"tags": tags, "budget": gift_budget, "avoid_for": avoid})
        if result:
            st.write(f"검색 결과: {result['count']}건")
            st.dataframe(result["items"], use_container_width=True)

with budget_tab:
    st.subheader("예산 검증")
    st.write("선물 이름과 가격을 입력하면 총액과 남은 예산을 계산합니다.")
    budget_limit = st.number_input("전체 예산", min_value=1, value=80_000, step=1_000, key="budget_limit")
    item_text = st.text_area("항목 입력", value="질문 카드 세트,12000\n손편지 키트,8000")
    if st.button("예산 검증하기", key="budget"):
        items = []
        try:
            for line in item_text.splitlines():
                name, price = line.rsplit(",", maxsplit=1)
                items.append({"name": name.strip(), "price": int(price.strip())})
        except ValueError:
            st.error("항목은 `이름,가격` 형식으로 한 줄에 하나씩 입력해 주세요.")
        else:
            result = call_api("/budget", {"items": items, "budget_limit": budget_limit})
            if result:
                message = f"총 {result['total']:,}원 / 남은 예산 {result['remaining']:,}원"
                (st.success if result["is_within_budget"] else st.warning)(message)

with schedule_tab:
    st.subheader("시간 검증")
    st.write("이벤트 단계와 각 소요 시간을 입력하면 가능 시간 안인지 확인합니다.")
    available_minutes = st.number_input("가능 시간(분)", min_value=1, value=180, step=10)
    step_text = st.text_area("단계 입력", value="손편지 전달,15\n질문 카드 대화,40", key="steps")
    if st.button("시간 검증하기", key="schedule"):
        steps = []
        try:
            for line in step_text.splitlines():
                title, minutes = line.rsplit(",", maxsplit=1)
                steps.append({"title": title.strip(), "duration_minutes": int(minutes.strip())})
        except ValueError:
            st.error("단계는 `이름,분` 형식으로 한 줄에 하나씩 입력해 주세요.")
        else:
            result = call_api("/schedule", {"steps": steps, "available_minutes": available_minutes})
            if result:
                message = f"총 {result['total_minutes']}분 / 남은 시간 {result['remaining_minutes']}분"
                (st.success if result["is_within_time"] else st.warning)(message)
