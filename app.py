"""
This script interacts with the Notion API to read and update data in a Notion database.
"""
from datetime import datetime, timedelta
# from pprint import pprint
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
    if periodicity == 'Daily':
        next_due_date = datetime.strptime(
            due_date, '%Y-%m-%d') + timedelta(days=1)
        next_set_date = datetime.strptime(due_date, '%Y-%m-%d')
        return next_due_date, next_set_date
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
    # # at least one task on the board should be in the To Do
    # # status only for the first launch of the application
    # if status['name'] == 'TO DO':
    #     todo_status = i['properties']['Status']

# pprint(properties_done)
# pprint(todo_status)

for i in properties_done:
    if i['properties']['Set date']['date'] is not None:
        set_date = i['properties']['Set date']['date']['start']
        due_date = i['properties']['Due Date']['date']['start']
        today = datetime.now().strftime('%Y-%m-%d')
        page_id = i['id']

        if set_date > today:
            continue

        if set_date < today:
            periodicity = i['properties']['Periodicity']['multi_select']
            next_due_date = None
            for period in periodicity:
                if period['name'].find('/') != -1 or period['name'] == 'Daily':
                    period_name = period['name']
                    next_due_date, next_set_date = calculate_next_due_date(
                        due_date, period_name)
                    new_properties = {
                        "Set date": {
                            "date": {
                                "start": next_set_date.strftime('%Y-%m-%d')
                            }
                        },
                        "Due Date": {
                            "date": {
                                "start": next_due_date.strftime('%Y-%m-%d')
                            }
                        }
                    }
                    update_page(headrs=headers, page_id=page_id,
                                properties=new_properties)
        elif set_date == today:
            new_properties = {
                "Status": {'id': 'eA%40u',
                        'select': {
                            'color': 'blue',
                            'id': '1', 
                            'name': 'TO DO'
                            },
                        'type': 'select'}
            }
            update_page(page_id=page_id, headrs=headers, properties=new_properties)
