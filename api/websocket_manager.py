import logging

from fastapi import WebSocket

log = logging.getLogger(__name__)


class WebsocketManager:
    def __init__(self):
        self.active_games = {}

    async def connect_player(self, websocket: WebSocket, game_id: str):
        if game_id not in self.games:
            self.games[game_id] = {
                'players': [],
                'dealers': []
            }
        await websocket.accept()
        self.games[game_id]['player'].append(websocket)

    async def connect_admin(self, websocket: WebSocket, game_id: str):
        if game_id not in self.games:
            self.games[game_id] = {
                players: [],
                admin: []
            }
        await websocket.accept()
        self.games[game_id]['dealers'].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        if websocket in self.games[game_id]['players']:
            self.self.games[game_id]['players'].remove(websocket)
        if websocket in self.games[game_id]['dealers']:
            self.self.games[game_id]['dealers'].remove(websocket)

    async def send_game_update(self, game_id: str):
        sql = SqlHandler()
        game = sql.get_game(game_id)
        for socket in self.self.games[game_id]['players']:
            await websocket.send_json(game)
        for socket in self.self.games[game_id]['admin']:
            await websocket.send_json(game)
