import logging
import sqlite3

logger = logging.getLogger(__name__)


def init():
    # Connect to db
    con = sqlite3.connect("ebird.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS followers(
        id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        ebird_user CHAR)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        next_schedule TEXT,
        follower_id INTEGER,
        FOREIGN KEY(follower_id) REFERENCES followers(id))
    """)

    logger.info("completed init of sqlite db")