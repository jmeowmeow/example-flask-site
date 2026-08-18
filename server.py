import sqlite3
import re
from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    conn = sqlite3.connect("/data/trees/trees.db", isolation_level=None)
    return conn.execute('SELECT * FROM trees LIMIT 5').fetchall()

@app.route("/tree/<tree_id>")
def get_tree(tree_id):
    conn = sqlite3.connect("/data/trees/trees.db", isolation_level=None)
    if re.search("^[0-9]+$", tree_id) is None:
       return "Tree not found.", 400
    return conn.execute(f'SELECT * FROM trees WHERE OBJECTID={tree_id}').fetchall()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
