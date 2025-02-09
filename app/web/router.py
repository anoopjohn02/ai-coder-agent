"""
Router module
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_controllers import Controller, get

from app.web.controller import TestController
from app.config import App

api = FastAPI()
api.mount("/static", StaticFiles(directory=App.static_path + "/static"), name="static")
templates = Jinja2Templates(directory=App.static_path + "/templates")


def start():
    """
    Start method
    """
    api.include_router(TestController.create_router())
    api.include_router(UIController.create_router())
    uvicorn.run(api, host="0.0.0.0", port=App.PORT)


class UIController(Controller):
    """
    UI Controller
    """

    @get("/ui", response_class=HTMLResponse)
    def read_item(self, request: Request):
        return templates.TemplateResponse(request=request, name="index.html")
