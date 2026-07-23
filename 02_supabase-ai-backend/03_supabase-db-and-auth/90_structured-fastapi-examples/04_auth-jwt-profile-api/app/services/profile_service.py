# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""RLS가 적용된 `ex90_profiles`를 REST API로 호출합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import httpx
# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.profile_schema import ProfilePublic, ProfileUpdate


# 학습 포인트: TABLE_NAME 변수에 오른쪽에서 만든 값을 저장합니다.
TABLE_NAME = "ex90_profiles"


# 학습 포인트: auth_headers 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def auth_headers(access_token: str | None) -> dict[str, str]:
    """Supabase REST API에 보낼 사용자 인증 헤더를 만듭니다.

    apikey에는 anon key를 넣고, Authorization에는 로그인한 사용자의 access token을 넣습니다.
    이 조합이어야 Supabase RLS가 "현재 사용자"를 판단할 수 있습니다.
    """

    # 학습 포인트: anon_key 변수에 오른쪽에서 만든 값을 저장합니다.
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not anon_key:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=500, detail="SUPABASE_ANON_KEY가 없습니다. .env 파일을 확인하세요.")

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not access_token:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=401, detail="Bearer token이 없습니다.")

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "apikey": anon_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


# 학습 포인트: table_url 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def table_url() -> str:
    """ex90_profiles 테이블의 Supabase REST API URL을 만듭니다."""

    # 학습 포인트: supabase_url 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase_url = os.getenv("SUPABASE_URL")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not supabase_url:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=500, detail="SUPABASE_URL이 없습니다. .env 파일을 확인하세요.")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return f"{supabase_url.rstrip('/')}/rest/v1/{TABLE_NAME}"


# 학습 포인트: to_profile 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def to_profile(row: dict) -> ProfilePublic:
    """Supabase row를 ProfilePublic 응답 모델로 변환합니다."""

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return ProfilePublic(
        id=str(row["id"]),
        display_name=row["display_name"],
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


# 학습 포인트: get_profile 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_profile(access_token: str | None) -> ProfilePublic:
    """현재 token으로 접근 가능한 프로필 1개를 조회합니다."""

    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # select=*로 요청하지만 RLS 때문에 현재 사용자 row만 응답됩니다.
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = httpx.get(
            table_url(),
            headers=auth_headers(access_token),
            params={"select": "*"},
            timeout=10,
        )
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        response.raise_for_status()
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except httpx.HTTPError as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"profile 조회 실패: {error}") from error

    # 학습 포인트: data 변수에 처리하거나 조회한 결과를 저장합니다.
    data = response.json()
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not data:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=404, detail="profile이 없습니다. PUT /profile을 먼저 실행하세요.")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return to_profile(data[0])


# 학습 포인트: upsert_profile 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def upsert_profile(
    user_id: str,
    access_token: str | None,
    request: ProfileUpdate,
) -> ProfilePublic:
    """현재 사용자 id로 프로필을 생성하거나 업데이트합니다."""

    # id는 auth.users.id와 같은 값입니다.
    # RLS 정책은 이 id가 auth.uid()와 같은지 검사합니다.
    # 학습 포인트: payload 변수에 오른쪽에서 만든 값을 저장합니다.
    payload = {"id": user_id, "display_name": request.display_name}
    # 학습 포인트: 오류가 발생할 수 있는 작업을 안전하게 시도합니다.
    try:
        # on_conflict=id는 id가 이미 있으면 update처럼 동작하게 해 줍니다.
        # 그래서 학생은 POST/PUT 차이보다 "내 프로필 저장" 흐름에 집중할 수 있습니다.
        # 학습 포인트: response 변수에 외부 서비스가 돌려준 응답을 저장합니다.
        response = httpx.post(
            f"{table_url()}?on_conflict=id",
            headers=auth_headers(access_token),
            json=payload,
            timeout=10,
        )
        # 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
        response.raise_for_status()
    # 학습 포인트: try에서 지정한 오류가 발생했을 때 대신 실행합니다.
    except httpx.HTTPError as error:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=502, detail=f"profile 저장 실패: {error}") from error

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return to_profile(response.json()[0])
