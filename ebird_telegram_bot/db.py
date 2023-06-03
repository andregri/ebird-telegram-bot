# Copyright: (c) 2023, Andrea Grillo
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import aiofiles
import aiohttp
import logging
import requests
import sqlite3

logger = logging.getLogger(__name__)


def restore(url: str, db_filename: str):
    """Donwloads a backup of the sqlite db from an online url
    
    Args:
        url (str): url where to download the db
        db_filename (str): name of the file where to save the db   
    """
    headers = {
        'User-Agent': 'curl/7.79.1', # free.keep.sh only receive files uploaded with curl
    }
    r = requests.get(url, allow_redirects=True, headers=headers)
    if r.ok:
        open(db_filename, 'wb').write(r.content)
        logger.info(f"{db_filename} backup downloaded from {url}")
    else:
        logger.error(f"couldn't download backup from {url}")


async def backup(db_filename: str, **kwargs) -> str:
    """
    Upload a backup of db_filename to https://free.keep.sh

    Args:
        db_filename (str): name of file to backup online

    Returns:
        url to download the file if successful, None otherwise
    """

    headers = {
        # free.keep.sh only receive files uploaded from user agent "curl"
        'User-Agent': 'curl/7.79.1',
    }
    async with aiofiles.open(db_filename, 'rb') as file:
        data = await file.read()
        async with aiohttp.ClientSession() as session:
            r = await session.request(method='PUT', url=f'https://free.keep.sh/{db_filename}', data=data, headers=headers, **kwargs)
            if r.ok:
                backup_url = await r.text()
                logger.info(f"ok to upload backup of {db_filename} at {backup_url}")
                return backup_url
            
            logger.error(f"failed to upload backup of {db_filename}: {r.status_code} {r.text}")
            return None


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
            chat_id INTEGER NOT NULL,
            ebird_user CHAR NOT NULL,
            PRIMARY KEY(chat_id, ebird_user))
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
            chat_id (int): the Telegram chat_id
            ebird_id (str): the eBird user id
        """
        self.cur.execute(f"""
            DELETE FROM {self.FOLLOWERS_TABLE}
            WHERE chat_id = {chat_id} AND ebird_user = '{ebird_id}'
        """)
        self.con.commit()

    def is_following(self, chat_id: int, ebird_id: str) -> bool:
        """
        Check if a chat_id is already following an eBird user

        Args:
            chat_id (int): the Telegram chat_id
            ebird_id (str): the eBird user id

        Returns:
            True if chat_id is already following ebird_id, False otherwise
        """
        res = self.cur.execute(f"""
            SELECT chat_id FROM {self.FOLLOWERS_TABLE}
            WHERE chat_id = {chat_id}
            AND ebird_user = '{ebird_id}'
        """)
        return res.fetchone() is not None

    def list_followings(self, chat_id: int) -> list:
        """
        Return a list of followed birdwatchers by chat_id

        Args:
            chat_id (int): the Telegram chat_id

        Returns:
            list of ebird user ids
        """
        res = self.cur.execute(f"""
            SELECT ebird_user FROM {self.FOLLOWERS_TABLE}
            WHERE chat_id = {chat_id}
        """)
        return [item[0] for item in res.fetchall()]

    def all(self) -> list:
        """
        Get all rows from following table

        Returns:
            list of all (chat_id, ebird_user_id) in db
        """
        res = self.cur.execute(f"""
            SELECT chat_id, ebird_user FROM {self.FOLLOWERS_TABLE}
        """)
        all = res.fetchall()
        logger.info(f"fetched {len(all)} rows")
        return all