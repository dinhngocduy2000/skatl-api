import os
import sys
from typing import Callable
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
import uvicorn
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.settings import settings

class App:
    application: FastAPI

    def on_init_app(self)-> Callable:
        async def start_app()->None:

            prefix="/api/v1"
            # self.application.include_router(

            # )
          

        return start_app
    
    def on_terminate_app (self)->Callable:
        @logger.catch
        async def stop_app()->None:
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
        self.application.add_event_handler("startup",self.on_init_app())
        self.application.add_event_handler("shutdown",self.on_terminate_app())

app = App().application
@app.get("/")
async def test():
    return "Test"

if __name__ =="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True) 