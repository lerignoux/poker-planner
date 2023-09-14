import logging
from fastapi import FastAPI, WebSocket

from game_db import GameDb

log = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/game")
async def game():
    db = GameDb()
    db.create_game()
    return {}

@app.post("/game/:game_id/submit")
async def game_submit(game_id):
    return {}

@app.get("/game/:game_id")
async def game_session():
    return {}


@app.websocket("/game_socket")
async def game_websocket(websocket: WebSocket):
   await websocket.accept()
   while True:
      data = await websocket.receive_text()
      await websocket.send_text(f"Message text was: {data}")
