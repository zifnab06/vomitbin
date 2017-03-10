from flask import Flask
from flask_mongoengine import MongoEngine
from apis import blueprint as api
from database import Paste


app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")

db = MongoEngine(app)

@app.route('/')
def main():
    return "moobar"

app.run(debug=True, host='0.0.0.0')
