# 학습 포인트: FastAPI 앱을 만들고 라우터를 연결하는 애플리케이션 시작 파일입니다.
"""Redis multi-turn chat API 실행 파일입니다."""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import FastAPI

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.routers.chat_router import router as chat_router


# 학습 포인트: API 서버의 중심이 되는 FastAPI 앱 객체를 만듭니다.
app = FastAPI(title="Example 02 - Simple Multi-turn Redis Chat API")
# 학습 포인트: 라우터를 FastAPI 앱에 연결해 해당 API 주소를 활성화합니다.
app.include_router(chat_router)
