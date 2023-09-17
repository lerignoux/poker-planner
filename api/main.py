import logging
import sqlite3
from typing import Union

from fastapi import FastAPI, WebSocket
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from sql_handler import SqlHandler
from websocket_manager import WebsocketManager

log = logging.getLogger(__name__)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080', 'http://127.0.0.1:8080', 'http://192.168.2.10:8081'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
websocket_manager = WebsocketManager()

@app.get("/")
async def root():
    return {"message": "Hello World"}


class GameQuery(BaseModel):
    planner_system: str
    jira_url: str
    stories: list = []

class PlayerQuery(BaseModel):
    name: str
    password: str

class StoryQuery(BaseModel):
    jira_id: str
    summary: str

class BetQuery(BaseModel):
    bet: str


@app.put("/game")
async def game(game_query: GameQuery):
    sql = SqlHandler()
    game_id = sql.create_game({'planner_system': game_query.planner_system, 'jira_url': game_query.jira_url})
    game = sql.get_game(game_id)
    for story in game_query.stories:
        story = {
          'jira_id': story['jira_id'],
          'summary': story['summary']
        }
        story_id = sql.add_story(game_id, story)
    return JSONResponse(content=game)


@app.get("/game/{game_id}")
async def game_session(game_id):
    sql = SqlHandler()
    game = sql.get_game(game_id)
    return JSONResponse(content=game)


@app.post("/game/{game_id}/join")
async def game_submit(game_id, user: PlayerQuery):
    sql = SqlHandler()
    player = {
      'name': user.name,
      'password': user.password
    }
    try:
        player_id = sql.add_player(game_id, player)
    except sqlite3.IntegrityError:
        if not sql.check_player(game_id, user.name, user.password):
            raise HTTPException(status_code=404, detail="User missing or password invalid.")
        else:
            player_id = sql.find_player(game_id, user.name)
    player = sql.get_player(player_id)
    await websocket_manager.send_game_update(game_id)
    return JSONResponse(content=player)


@app.post("/game/{game_id}/kick/{player_id}")
async def kick_player(game_id, player_id):
    sql = SqlHandler()
    player_id = sql.remove_player(game_id, player_id)
    await websocket_manager.send_game_update(game_id)
    return JSONResponse(content={})


@app.post("/game/{game_id}/submit")
async def game_submit(game_id):
    return {}


@app.put("/game/{game_id}/story")
async def story(game_id, story: StoryQuery):
    sql = SqlHandler()
    story = {
      'jira_id': story.jira_id,
      'summary': story.summary
    }
    story_id = sql.add_story(game_id, story)
    story = sql.get_story(story_id)
    return JSONResponse(content=story)


@app.get("/game/{game_id}/story/{story_id}")
async def story(game_id, story_id):
    return {}


@app.post("/game/{game_id}/story/{story_id}/bet")
async def bet(game_id, story_id, player_id: str, bet: BetQuery):
    sql = SqlHandler()
    #if not sql.check_user(username, password)
    #  return JSONResponse(content={'error': 'invalid user login'})
    bet_id = sql.add_or_update_bet(game_id, player_id, story_id, bet.bet)
    if (sql.played(game_id, story_id)):
      websocket_manager.send_game_update(game_id)
    return JSONResponse(content={'id': str(bet_id)})


@app.websocket("/game/{game_id}/socket/player")
async def game_websocket(websocket: WebSocket, game_id):
  sql = SqlHandler()
  await websocket_manager.connect_player(websocket, game_id)
  print(f"Sending inital game status")
  game = sql.get_game(game_id)
  await websocket.send_json(game)

  while True:
    data = await websocket.receive_json()
    print(f"received player info: {data}")
    player_id = data['player_id']
    story_id = data['story_id']
    bet = data.get('bet')
    if bet is not None:
      bet_id = sql.add_or_update_bet(game_id, player_id, story_id, bet)
    await websocket_manager.send_game_update(game_id)
    
    await websocket.send_json(game)


@app.websocket("/game/{game_id}/socket/dealer")
async def game_websocket(websocket: WebSocket, game_id):
  sql = SqlHandler()
  await websocket_manager.connect_dealer(websocket, game_id)
  game = sql.get_game(game_id)
  await websocket.send_json(game)

  while True:
    data = await websocket.receive_json()
    print(f"received dealer info: {data}")
    await websocket.send_json(game)