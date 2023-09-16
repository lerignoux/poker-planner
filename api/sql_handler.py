import logging
import sqlite3
import uuid

log = logging.getLogger(__name__)


class SqlHandler():
    def __init__(self, db_file="poker_planner.sql"):
        self.connection = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        games_table = """
            CREATE TABLE IF NOT EXISTS games (
            id string PRIMARY KEY,
            planner_system string,
            jira_url string
        );
        """
        players_table = """
            CREATE TABLE IF NOT EXISTS players (
            id string PRIMARY KEY,
            game_id string NOT NULL,
            name string NOT NULL,
            password string NOT NULL,
            CONSTRAINT uniquePlayers UNIQUE (game_id, name)
        );
        """
        stories_table = """
            CREATE TABLE IF NOT EXISTS stories (
            id string PRIMARY KEY,
            game_id string NOT NULL,
            jira_id string NOT NULL UNIQUE,
            summary string
        );
        """
        bets_table = """
            CREATE TABLE IF NOT EXISTS bets (
            id string PRIMARY KEY,
            game_id string NOT NULL,
            player_id string NOT NULL,
            story_id string NOT NULL,
            bet integer,
            CONSTRAINT uniqueBets UNIQUE (game_id, player_id, story_id)
        );
        """
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(games_table)
            cursor.execute(players_table)
            cursor.execute(stories_table)
            cursor.execute(bets_table)

    def create_game(self, game):
        game_id = uuid.uuid4()
        planner_system = game['planner_system']
        jira_url = game['jira_url']
        sql = f" INSERT INTO games(id, planner_system, jira_url) VALUES('{game_id}', '{planner_system}', '{jira_url}') "
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)

        for story in game.get('stories', []):
            self.add_story(game_id, story)

        return game_id

    def get_game(self, game_id, stories=True, bets=True, players=True):
        sql = f"SELECT * FROM games WHERE id='{game_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            games = cursor.fetchall()
        assert (len(games) == 1)

        result = {
            'id': games[0][0],
            'planner_system': games[0][1],
            'jira_url': games[0][2]
        }
        if stories:
            result['stories'] = self.get_stories(game_id, bets)
        if players:
            result['players'] = self.get_players(game_id)
        return result

    def add_player(self, game_id, player):
        player_id = uuid.uuid4()
        player_name = player['name']
        player_password = player['password']
        sql = f"INSERT INTO players(id, game_id, name, password) VALUES('{player_id}', '{game_id}', '{player_name}', '{player_password}')"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
        return player_id

    def get_player(self, player_id):
        sql = f"SELECT * FROM players WHERE id='{player_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            players = cursor.fetchall()
        assert(len(players) == 1)

        result = {
            'id':players[0][0],
            'game_id': players[0][1],
            'name': players[0][2]
        }
        return result

    def get_players(self, game_id):
        sql = f"SELECT * FROM players WHERE game_id='{game_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            players = cursor.fetchall()

        result = []
        for player in players:
            result.append({
                'id':player[0],
                'game_id': player[1],
                'name': player[2]
            })
        return result

    def check_player(self, game_id, playername, password):
        sql = f"SELECT password FROM players WHERE game_id='{game_id}' AND name='{player_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            passwords = cursor.fetchall()
        return len(passwords) == 1 and passwords[0] == password

    def add_story(self, game_id, story):
        story_id = uuid.uuid4()
        jira_id = story['jira_id']
        summary = story['summary']
        sql = f" INSERT INTO stories(id, game_id, jira_id, summary) VALUES('{story_id}', '{game_id}', '{jira_id}', '{summary}')"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
        return story_id

    def get_story(self, story_id, bets=True):
        sql = f"SELECT * FROM stories WHERE id='{story_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            stories = cursor.fetchall()
        assert(len(stories) == 1)

        result = {
            'id': stories[0][0],
            'game_id': stories[0][1],
            'jira_id': stories[0][3],
            'summary': stories[0][2]
        }
        if bets:
            result['bets'] = self.get_bets(story_id)
        return result

    def get_stories(self, game_id, bets=False):
        sql = f"SELECT * FROM stories WHERE game_id='{game_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            stories = cursor.fetchall()

        result = []
        for story in stories:
            res = {
                'id': story[0],
                'game_id': story[1],
                'jira_id': story[3],
                'summary': story[2]
            }
            if bets:
                print("fetching bets {story}")
                res['bets'] = self.get_bets(story[0])

            result.append(res)

        return result

    def add_or_update_bet(self, game_id, player_id, story_id, bet):
        sql = f"SELECT id FROM bets WHERE game_id='{game_id}' AND player_id='{player_id}' and story_id='{story_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            previous_bet = cursor.fetchall()

        if previous_bet:
            bet_id = previous_bet[0][0]
            sql = f"UPDATE bets SET bet='{bet}' WHERE id='{bet_id}'"
        else:
            bet_id = uuid.uuid4()
            sql = f"INSERT INTO bets (id, game_id, player_id, story_id, bet) VALUES('{bet_id}', '{game_id}', '{player_id}', '{story_id}', '{bet}') "

        print(sql)
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
        return bet_id

    def played(self, game_id, story_id):
        sql = f"SELECT COUNT(*) FROM players WHERE game_id='{game_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            counts = cursor.fetchall()
        assert(len(counts) == 1)
        players_count = counts[0]

        sql = f"SELECT COUNT(*) FROM bets WHERE story_id='{story_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            counts = cursor.fetchall()
        assert(len(counts) == 1)
        bets_count = counts[0]

        return bets_count == players_count


    def get_bet(self, bet_id):
        sql = f"SELECT * FROM bets WHERE id='{bet_id}'"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            bets = cursor.fetchall()
        assert(len(bets) == 1)

        result = {
            'id': bets[0][0],
            'game_id': bets[0][1],
            'players_id': bets[0][2],
            'story_id': bet[0][3], 
            'bet': bets[0][4],
        }
        return result

    def get_bets(self, story_id):
        sql = f"SELECT * FROM bets WHERE story_id='{story_id}'"
        print(sql)
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            bets = cursor.fetchall()

        result = []
        for bet in bets:
            result.append({
                'id': bet[0],
                'game_id': bet[1],
                'player_id': bet[2],
                'story_id': bet[3],
                'bet': bet[4]
            })
        return result