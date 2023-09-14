import logging
import sqlite3
import uuid

log = logging.getLogger(__name__)


class GameDb():

    def __init__(self, db_file="poker_planner.sql"):
        self.connection = sqlite3.connect(db_file)

    def create_tables(self):
        create_users = """
            CREATE TABLE IF NOT EXISTS users (
            id string PRIMARY KEY,
            game_id string NOT NULL,
            name string NOT NULL,
            password string NOT NULL
        );
        """
        create_games = """
            CREATE TABLE IF NOT EXISTS games (
            id string PRIMARY KEY,
            admin_id string NOT NULL,
            planner_system string,
            jira_url string
        );
        """
        stories_table = """
            CREATE TABLE IF NOT EXISTS stories (
            id string PRIMARY KEY,
            game_id string NOT NULL,
            summary string,
            jira_id string
        );
        """
        create_users = """
            CREATE TABLE IF NOT EXISTS bets (
            id string PRIMARY KEY,
            game_id string NOT NULL,
            user_id string NOT NULL,
            story_id string NOT NULL,
            bet integer
        );
        """
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(create_users)
            cursor.execute(create_games)
            cursor.execute(create_stories)
            cursor.execute(create_bets)

    def create_user(self, game_id, user):
        user_id = uuid.uuid4()
        user_name = user['username']
        user_password = user['password']
        sql = f"INSERT INTO users(id, game_id, name, password) VALUES({user_id}, {game_id}, {user_name}, {user_password})"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
        return user_id

    def create_game(admin_id, planner_system, jira_url, stories):
        game_id = uuid.uuid4()
        sql = f" INSERT INTO games(id, admin_id, planner_system, jira_url) VALUES({game_id}, {admin_id}, {planner_system}, {jira_url}) "
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)

        for story in stories:
            self.add_story(game_id, story)

        return game_id

    def add_story(game_id, story):
        story_id = uuid.uuid4()
        jira_id = story['jira_id']
        summary = story['summary']
        sql = f" INSERT INTO stories(id, game_id, summary, jira_id) VALUES({uuid}, {admin_id}, {jira_id}, {summary}) "
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
        return story_id


    def add_or_update_bet(game_id, user_id, story_id, bet):
        sql = f"SELECT id FROM bets WHERE game_id={game_id} AND user_id={user_id} and story_id={story_id}"
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            previous_bet = cursor.fetchall()

        if previous_bet:
            bet_id = previous_bet[0]
            sql = f"UPDATE bets SET bet={bet} WHERE id={bet_id}"
        else:
            bet_id = uuid.uuid4()
            sql = f"INSERT INTO bets (id, game_id, user_id, story_id, bet) VALUES({bet_id}, {game_id}, {user_id}, {story_id}, {bet}) "

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
        return ibet_id_id



