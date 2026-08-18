import sqlite3
from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    conn = sqlite3.connect("/data/trees/trees.db", isolation_level=None)
    return conn.execute('SELECT * FROM trees LIMIT 5').fetchall()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
