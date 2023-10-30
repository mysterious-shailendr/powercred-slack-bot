from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from slackeventsapi import SlackEventAdapter
from fastapi.responses import JSONResponse
from http.client import HTTPResponse
from .apps import leaves_tracker_app
from .core.handler import BotHandler
from .core.manager import Manager
import asyncio
import json

app = FastAPI()
origins = ["*"]

@app.post("/slack/interactive")
async def slack_interactive(request: Request):
    payload_data = await request.form()
    payload = json.loads(payload_data["payload"])
    print(payload_data)

    if "U060PP7BB1N" in payload["user"]["id"]:
        return {"status": "success", "message": "No need to respond to self"}
        
    raise HTTPException(status_code=400, detail="Invalid interaction")

@app.post("/slack/events")
async def slack_events(request: Request):
    """
    1. This is the entry point, it receives events from the Slack.
    2. U060PP7BB1N is the Bot's user_id.
    3. We used BotHandler class to handle the events.
    """
    manager = Manager()
    data, timestamp, slack_signature, is_repeating = await request.body(), request.headers.get('X-Slack-Request-Timestamp'), request.headers.get('X-Slack-Signature'), request.headers.get('X-Slack-Retry-Num')
    if bool(is_repeating): return JSONResponse(content={"ok": True}) # <- This will prevent from creating a dead loop
    if not manager.verify_slack_signature(data, timestamp, slack_signature): raise HTTPException(status_code=400, detail="Invalid request")
    json_data = await request.json()
    event_type = json_data.get("event", {}).get("type")
    if ( event_type == "message" and event_type != "message_changed" ) or event_type == "app_mention":
        if "client_msg_id" in json_data["event"] and "bot_id" not in json_data["event"]:
            try:
                user_id = json_data["event"]["user"]
                if str(user_id) != "U060PP7BB1N":
                    bot_handler = BotHandler()
                    asyncio.run(await bot_handler.handler(json_data))
                    return JSONResponse(content={"ok": True})
                else: return JSONResponse(content={"ok": True})
            except: return JSONResponse(content={"ok": True})
    else: return {"challenge": json_data.get("challenge", "")}

app.add_middleware( CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"] )
app.include_router( leaves_tracker_app )

def custom_openapi():
    if app.openapi_schema: return app.openapi_schema
    openapi_schema = get_openapi(
        title="Identity",
        version="0.1.0",
        description="This is OpenAPI v3 for Powercred-identity-verification",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://storage.googleapis.com/powercred/image.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi