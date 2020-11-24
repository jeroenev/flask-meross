import asyncio
import sys

sys.path.append('..')
from flask_meross.util import require_appkey
from flask_meross.meross import meross_action
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World, this api runs a simple Meross Gateway owned by Jeroen Evens!"

@app.route("/testauth")
@require_appkey
def test_authentication():
    return "Authentication successfull!"

@app.route('/meross/<name>/<action>')
@require_appkey
def meross_off(name, action):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(meross_action(name, action))
    loop.close()
    return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8079)