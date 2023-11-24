from fastapi import FastAPI
from app.routers import router
from starlette.middleware.sessions import SessionMiddleware

def get_application() -> FastAPI:
    application = FastAPI()
    application.add_middleware(SessionMiddleware, secret_key="secret_key")
    application.include_router(router)
    return application

app = get_application()  #  uvicorn app.main:app
