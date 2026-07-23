# 학습 포인트: Supabase 데이터베이스 클라이언트를 만드는 파일입니다.
"""Supabase client를 만듭니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import HTTPException

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
import app.core.config  # .env 파일을 읽습니다.


# 학습 포인트: get_supabase_client 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_supabase_client():
    """service role key를 사용하는 Supabase client를 만듭니다."""

    # 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
    from supabase import create_client

    # 학습 포인트: supabase_url 변수에 오른쪽에서 만든 값을 저장합니다.
    supabase_url = os.getenv("SUPABASE_URL")
    # 학습 포인트: service_role_key 변수에 오른쪽에서 만든 값을 저장합니다.
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not supabase_url:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(500, "SUPABASE_URL이 없습니다. .env 파일을 확인하세요.")
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not service_role_key:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(500, "SUPABASE_SERVICE_ROLE_KEY가 없습니다. .env 파일을 확인하세요.")

    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return create_client(supabase_url, service_role_key)
