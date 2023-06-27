"""
This is a Flask application that runs a script and logs the output to a file
"""
import subprocess
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def run_script():
    """Run app.py"""
    try:
        subprocess.Popen(['python', 'app.py'])
        return 'Script started'
    except Exception as e:
        return f'Error: {e}'


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
