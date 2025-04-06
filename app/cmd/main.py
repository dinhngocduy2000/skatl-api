from core.settings import settings
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from loguru import logger
from fastapi import Depends, FastAPI, HTTPException
from typing import Callable
from core.database.postgres import create_pg_engine
from repository.registry import Registry
from controller.auth import AuthController
from handler.auth import AuthHandler
from router.auth import AuthRoute
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class App:
    application: FastAPI

    def on_init_app(self) -> Callable:
        async def start_app() -> None:
            pg_engine = create_pg_engine()
            registry = Registry(pg_engine)

            auth_controller = AuthController(registry)
            # AuthMiddleware.init(auth_controller)
            auth_handler = AuthHandler(auth_controller)
            auth_router = AuthRoute(auth_handler)
            prefix = "/api/v1"
            self.application.include_router(
                auth_router.router, prefix=prefix+"/auth", tags=["Auth"]
            )

        return start_app

    def on_terminate_app(self) -> Callable:
        @logger.catch
        async def stop_app() -> None:
            pass
        return stop_app

    def __init__(self):
        self.application = FastAPI(**settings.fastapi_kwargs)
        self.application.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        self.application.add_event_handler("startup", self.on_init_app())
        self.application.add_event_handler("shutdown", self.on_terminate_app())


app = App().application

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
