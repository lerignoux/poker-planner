import logging

from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

from sql_handler import SqlHandler
from websocket_manager import WebsocketManager

log = logging.getLogger(__name__)


app = FastAPI()
websocket_manager = WebsocketManager()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/game")
async def game(planner_system: str, jira_url: str):
    sql = SqlHandler()
    game_id = sql.create_game({'planner_system': planner_system, 'jira_url': jira_url})
    game = sql.get_game(game_id)
    return JSONResponse(content=game)


@app.get("/game/{game_id}")
async def game_session(game_id):
    sql = SqlHandler()
    game = sql.get_game(game_id)
    return JSONResponse(content=game)


@app.post("/game/{game_id}/join")
async def game_submit(game_id, name: str, password: str):
    sql = SqlHandler()
    player = {
      'name': name,
      'password': password
    }
    player_id = sql.add_player(game_id, player)
    player = sql.get_player(player_id)
    game = sql.get_game(game_id)
    return JSONResponse(content={'player': player, 'game':game})


@app.post("/game/{game_id}/submit")
async def game_submit(game_id):
    return {}


@app.put("/game/{game_id}/story")
async def story(game_id, jira_id: str, summary: str):
    sql = SqlHandler()
    story = {
      'jira_id': jira_id,
      'summary': summary
    }
    story_id = sql.add_story(game_id, story)
    story = sql.get_story(story_id)
    return JSONResponse(content=story)


@app.get("/game/{game_id}/story/{story_id}")
async def story(game_id, story_id):
    return {}


@app.post("/game/{game_id}/story/{story_id}/bet")
async def bet(game_id, story_id, player_id: str, bet: str):
    sql = SqlHandler()
    #if not sql.check_user(username, password)
    #  return JSONResponse(content={'error': 'invalid user login'})
    bet_id = sql.add_or_update_bet(game_id, player_id, story_id, bet)
    if (sql.played(game_id, story_id)):
      websocket_manager.send_game_update(game_id, )
    return JSONResponse(content={'id': str(bet_id)})


@app.websocket("/game/{game_id}/socket/player")
async def game_websocket(websocket: WebSocket, game_id):
  sql = SqlHandler()  
  await websocket.accept()
  while True:
    data = await websocket.receive_json()
    player_id = data['player_id']
    player_id = data['story_id']
    bet = data.get('bet')
    if bet:
      bet_id = sql.add_or_update_bet(game_id, story_id, user_id, bet)
    game = sql.get_game(game_id)
    await websocket.send_json(game)
