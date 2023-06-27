import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings():
    NOTION_TOKEN: str = os.getenv('NOTION_TOKEN')
    DATABASE_ID: str = os.getenv('DATABASE_ID')


settings = Settings()
