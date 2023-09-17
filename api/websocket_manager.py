import logging

from fastapi import WebSocket

from sql_handler import SqlHandler

log = logging.getLogger(__name__)


class WebsocketManager:
    def __init__(self):
        self.games = {}

    async def connect_player(self, websocket: WebSocket, game_id: str):
        if game_id not in self.games:
            self.games[game_id] = {
                'players': [],
                'dealers': []
            }
        await websocket.accept()
        self.games[game_id]['players'].append(websocket)

    async def connect_dealer(self, websocket: WebSocket, game_id: str):
        if game_id not in self.games:
            self.games[game_id] = {
                'players': [],
                'dealers': []
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
        for socket in self.games[game_id]['players']:
            print(f"sending game update to player")
            try:
                await socket.send_json(game)
            except Exception as e:
                log.exception(e, "Failed sending game update, player probably disconnected")

        for socket in self.games[game_id]['dealers']:
            print(f"sending game update to dealer")
            try:
                await socket.send_json(game)
            except Exception as e:
                log.exception(e, "Failed sending game update, dealer probably disconnected")
