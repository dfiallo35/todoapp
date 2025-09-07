from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

from app.presentation.api import router
from app.settings import settings


class BaseApp:
    app: FastAPI = None
    settings: BaseSettings = None

    def __init__(self, router: APIRouter, settings: BaseSettings):
        self.setup_settings(settings)
        self.app = self.create_app(router)

    def create_app(self, router: APIRouter):
        app = FastAPI()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(router)
        return app

    def setup_settings(self, settings: BaseSettings):
        self.settings = settings
        self.settings.setup()


base_app = BaseApp(router=router, settings=settings)
app = base_app.app
