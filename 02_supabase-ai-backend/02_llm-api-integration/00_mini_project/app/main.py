from fastapi import FastAPI

from app.core import chat_config  # .env 파일을 로드합니다.
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router


app = FastAPI(title="Main App")
app.include_router(product_router)
app.include_router(chat_router)
