from pprint import pprint
import requests
from config import settings


token = settings.NOTION_TOKEN
database_id = settings.DATABASE_ID

headers = {
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
    "Authorization": f"Bearer {token}"
}


def read_db(db_id: str, headrs: dict) -> dict:
    """Read data from a Notion database."""
    read_url = f"https://api.notion.com/v1/databases/{db_id}/query"
    res = requests.post(url=read_url, headers=headrs, timeout=None)
    data = res.json()
    return data

pprint(read_db(db_id=database_id, headrs=headers))
