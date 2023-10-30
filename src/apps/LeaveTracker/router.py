from fastapi import APIRouter, HTTPException
import threading
from ...core.manager import Manager
from .leave_tracker import LeaveTracker
from starlette.requests import Request
from starlette.responses import Response
from urllib.parse import parse_qs
import asyncio

class LeaveTrackerRouter(Manager, LeaveTracker):
    def __init__(self) -> None:
        super().__init__()
        self.manager = Manager()
        self.leave_tracker = LeaveTracker()
        self.router = APIRouter(prefix='/leaves')
        self.router.add_api_route( '/all', self.get_all_leaves, methods=['POST'] )
        self.router.add_api_route( '/apply', self.apply_leave, methods=['POST'] )

    async def get_all_leaves(self, request: Request):
        request_body = await request.body()
        parsed_data = parse_qs(request_body.decode())

        channel_id = parsed_data.get('channel_id', [''])[0]

        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.get_all_leaves_helper(channel_id))
            loop.close()

        thread = threading.Thread(target=run_in_thread)
        thread.start()

        return "Please wait, I am fetching the details :hourglass_flowing_sand:"


    async def apply_leave(self):
        return "Apply leave"
    

    async def get_all_leaves_helper(self, channel_id):
        table, status = await self.leave_tracker.get_leaves()
        if status == 200: 
            self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text=table)
        else: raise HTTPException(status_code=status, detail=table)

    async def apply_leaves_helper(self, channel_id):
        table, status = await self.leave_tracker.get_leaves()
        if status == 200: 
            self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text=table)
        else: raise HTTPException(status_code=status, detail=table)