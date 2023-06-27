"""
This code loads environment variables from a .env file and defines a Settings class
to store the values of the environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings():
    """
    Stores the values of environment variables.
    """
    NOTION_TOKEN: str = os.getenv('NOTION_TOKEN')
    DATABASE_ID: str = os.getenv('DATABASE_ID')
    HOST: str = os.getenv('HOST')


settings = Settings()
