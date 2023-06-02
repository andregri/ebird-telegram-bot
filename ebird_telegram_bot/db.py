import logging
import sqlite3

logger = logging.getLogger(__name__)


class Database:
    """
    Database of the Telegram bot
    """
    FOLLOWERS_TABLE = "followers"
    JOBS_TABLE = "jobs"

    con = None
    cur = None

    def __init__(self) -> None:
        # Connect to db
        self.con = sqlite3.connect("ebird.db")
        self.cur = self.con.cursor()

        # Create followers table
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.FOLLOWERS_TABLE}(
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            ebird_user CHAR)
        """)

        # Create scheduled jobs table
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.JOBS_TABLE}(
            next_schedule TEXT,
            follower_id INTEGER,
            FOREIGN KEY(follower_id) REFERENCES followers(id))
        """)

        logger.info("completed init of sqlite db")


    def insert_follower(self, chat_id: int, ebird_id: str) -> None:
        """
        Insert a follower into the "followers" table

        Args:
            chat_id (int): the Telegram chat_id which issued the /follow command
            ebird_id (str): the eBird user id to follow
        """
        self.cur.execute(f"INSERT INTO {self.FOLLOWERS_TABLE} VALUES ({chat_id}, '{ebird_id}')")
        self.con.commit()

    def delete_follower(self, chat_id: int, ebird_id: str) -> None:
        """
        Delete a follower from "followers" table

        Args:
            chat_id (int): the Telegram chat_id which issued the /follow command
            ebird_id (str): the eBird user id to follow
        """
        self.cur.execute(f"""
            DELETE FROM {self.FOLLOWERS_TABLE}
            WHERE chat_id = {chat_id} AND ebird_user = '{ebird_id}'
        """)
        self.con.commit()