# 학습 포인트: FastAPI 앱을 만들고 라우터를 연결하는 애플리케이션 시작 파일입니다.
"""Notes API의 시작 파일입니다. 실행: python -m uvicorn app.main:app --reload --port 8011"""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import FastAPI

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.routers.notes_router import router as notes_router


# 학습 포인트: API 서버의 중심이 되는 FastAPI 앱 객체를 만듭니다.
app = FastAPI(
    title="Notes API With Supabase",
    description="초보자를 위한 노트 CRUD 미니 프로젝트",
    version="1.0.0",
)
# 학습 포인트: 라우터를 FastAPI 앱에 연결해 해당 API 주소를 활성화합니다.
app.include_router(notes_router)
