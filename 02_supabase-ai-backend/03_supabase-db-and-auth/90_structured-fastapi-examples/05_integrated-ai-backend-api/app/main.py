# 학습 포인트: FastAPI 앱을 만들고 라우터를 연결하는 애플리케이션 시작 파일입니다.
r"""Integrated AI Backend API 구조화 예제입니다.

실행:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8015
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8015
"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import FastAPI

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.routers.auth_router import router as auth_router
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.routers.chat_router import router as chat_router


# 통합 예제의 앱 시작점입니다.
# auth_router는 로그인/token 확인, chat_router는 AI 답변/캐시/로그 조회를 담당합니다.
# 학습 포인트: API 서버의 중심이 되는 FastAPI 앱 객체를 만듭니다.
app = FastAPI(title="Example 05 - Integrated AI Backend API")
# 학습 포인트: 라우터를 FastAPI 앱에 연결해 해당 API 주소를 활성화합니다.
app.include_router(auth_router)
# 학습 포인트: 라우터를 FastAPI 앱에 연결해 해당 API 주소를 활성화합니다.
app.include_router(chat_router)
