import logging
import requests

user_display_name_cache = {}


# Enable logging
logger = logging.getLogger(__name__)


def get_latest(user_id: str, region="world"):
    """
    Downloads at most the last 10 checklists of a user.
    Update the user display name cache.

    Args:
        user_id: user id
        region: region in the world (default is "world")

    Return:
        list of checklists info (max length is 10)
    """
    r = requests.get(f"https://ebird.org/prof/lists?r={region}&username={user_id}")
    if r.status_code >= 400:
        raise Exception(f"Error {r.status_code} from eBird: ID {user_id} may not exists or eBird is not working.")
    json_data = r.json()
    user_display_name_cache[user_id] = json_data[0]['userDisplayName']

    return json_data


def user_display_name(user_id) -> str:
    """
    Returns the display name of a user from its user id

    Args:
        user_id: user id

    Returns:
        user display name
    """
    if not user_id in user_display_name_cache:
        try:
            get_latest(user_id)
        except:
            logger.info(f"{user_id} not found on eBird")
            return None
        
    return user_display_name_cache[user_id]