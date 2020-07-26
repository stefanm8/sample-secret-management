from flask import Flask
from os import environ
app = Flask(__name__)

@app.route('/')
def env():
    return f"""
        DB_USERNAME={environ.get('DB_USERNAME')}
        DB_PASSWORD={environ.get('DB_PASSWORD')}
    """

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)
