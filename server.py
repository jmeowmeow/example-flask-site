import re
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    conn = sqlite3.connect("/data/trees/trees.db", isolation_level=None)
    page = int(request.args.get("page") or "0")
    data = conn.execute(
        f"SELECT OBJECTID FROM trees LIMIT 10 OFFSET {page * 10}"
    ).fetchall()
    trees = [row[0] for row in data]
    return render_template("index.html", trees=trees, page=page)


@app.route("/tree/<tree_id>")
def get_tree(tree_id):
    conn = sqlite3.connect("/data/trees/trees.db", isolation_level=None)
    if re.search("^[0-9]+$", tree_id) is None:
        return "Tree not found.", 400
    tree = conn.execute(f"SELECT * FROM trees WHERE OBJECTID={tree_id}").fetchone()
    return render_template("tree.html", species=tree[8], data=tree)

@app.route("/toptrees/<myvariety>")
def get_top_trees(myvariety):
    varieties = [ "oak", "maple", "apple", "linden", "plane", "elm", "hackberry" ]
    conn = sqlite3.connect("/data/trees/trees.db", isolation_level=None)
    if re.search("^[A-Za-z]+$", myvariety) is None:
        myvariety = "elm"
    data = conn.execute(
        f"SELECT GenusSpecies as variety, COUNT(*) as pop FROM trees WHERE GenusSpecies LIKE '%{myvariety}%' GROUP BY variety ORDER BY pop DESC LIMIT 10 "
    ).fetchall()
    specieslist = [row[0] for row in data]
    return render_template("toptrees.html", myvariety=myvariety, specieslist=specieslist, varieties=varieties)

@app.route("/toptrees/")
def get_top_trees_default():
    get_top_trees("elm")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
