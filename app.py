from datetime import datetime, timedelta
from pprint import pprint
import json
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


def update_page(headrs: dict, page_id: int, properties: dict) -> dict:
    """Update the properties of a page in the Notion database."""
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    update_data = {
        "properties": properties
    }

    data = json.dumps(update_data)
    res = requests.patch(url=update_url, headers=headrs,
                         data=data, timeout=None)
    return res.json()


def calculate_next_due_date(due_date: str, periodicity: str) -> tuple:
    """Calculate the next due date and set date based on the periodicity."""
    frequency, interval = periodicity.split('t/')
    frequency = int(frequency)
    if interval == 'w':
        next_due_date = datetime.strptime(
            due_date, '%Y-%m-%d') + timedelta(weeks=1/frequency)
        next_set_date = next_due_date - timedelta(days=1)
        return next_due_date, next_set_date
    if interval == '2w':
        next_due_date = datetime.strptime(
            due_date, '%Y-%m-%d') + timedelta(weeks=1/frequency * 2)
        next_set_date = next_due_date - timedelta(days=3)
        return next_due_date, next_set_date
    if interval == 'm':
        next_due_date = datetime.strptime(
            due_date, '%Y-%m-%d') + timedelta(weeks=1/frequency * 4)
        next_set_date = next_due_date - timedelta(weeks=1)
        return next_due_date, next_set_date
    if interval == '2m':
        next_due_date = datetime.strptime(
            due_date, '%Y-%m-%d') + timedelta(weeks=1/frequency * 8)
        next_set_date = next_due_date - timedelta(weeks=2)
        return next_due_date, next_set_date
    if interval == '3m':
        next_due_date = datetime.strptime(
            due_date, '%Y-%m-%d') + timedelta(weeks=1/frequency * 12)
        next_set_date = next_due_date - timedelta(weeks=2)
        return next_due_date, next_set_date


properties_done = []
todo_status = ""

for i in read_db(db_id=database_id, headrs=headers)['results']:
    status = i['properties']['Status']['select']
    if status is None:
        continue
    if status['name'] == 'DONE':
        properties_done.append(i)
    # at least one task on the board should be in the To Do
    # status only for the first launch of the application
    if status['name'] == 'TO DO':
        todo_status = i['properties']['Status']

pprint(properties_done)
