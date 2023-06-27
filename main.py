"""
This is a Flask application that runs a script and logs the output to a file
"""
import subprocess
import logging
from logging import FileHandler
from flask import Flask
from config import settings

app = Flask(__name__)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

file_handler = FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'))

logging.getLogger('').addHandler(file_handler)


@app.route('/', methods=['GET'])
def run_script():
    """Run app.py"""
    try:
        subprocess.Popen(['python', 'app.py'])
        logging.info('Script started')
        return 'Script started'
    except Exception as e:
        logging.error('Error occurred while running the script:', exc_info=True)
        return f'Error: {e}'


if __name__ == '__main__':
    app.run(host=settings.HOST, port=8000)
