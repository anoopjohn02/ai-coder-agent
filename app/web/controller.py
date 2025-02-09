"""
Controller module
"""
import logging

from fastapi.responses import StreamingResponse
from fastapi_controllers import Controller, post

from app.models.chat import Request
from app.models.user import LoggedInUser
from app.services import (aanswer)


class TestController(Controller):
    """
    A test class will be removed later
    """
    prefix = "/v1/test"
    tags = ["test chat"]

    @post("/stream")
    async def test_stream(self, request: Request):
        """
        Test AOI method
        """
        user = LoggedInUser(id="c7f0bad7-ca8d-43a3-840f-df19d3c0e974",
                            first_name="Anoop",
                            username="str",
                            email="str",
                            last_name="str",
                            realm_roles=[],
                            client_roles=[],
                            )
        logging.info("New chat = %s", request.new_chat)
        logging.info("User %s asked question: %s", user.first_name, request.question)
        return StreamingResponse(aanswer(request, user), media_type='text/event-stream')
