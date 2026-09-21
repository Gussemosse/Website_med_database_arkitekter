from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
# Database opsætning
DB_ARCHITECTS = "./db/architects.db"

def get_aids(search):
    con = sqlite3.connect(DB_ARCHITECTS)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    query = "select aid from buildings where name like ?"
    cur.execute(query, (search,))
    res = cur.fetchall()
    cur.close()
    con.close()
    return [list(r)[0] for r in res] if res != [] else [-1]

def get_architect_from_aid(aid):
    con = sqlite3.connect(DB_ARCHITECTS)
    cur = con.cursor()
    query = "select name from architects where aid=?"
    cur.execute(query, (aid,))
    res = cur.fetchone()
    cur.close()
    con.close()
    return res[0]

def get_architect_info(aid):
    con = sqlite3.connect(DB_ARCHITECTS)
    cur = con.cursor()
    query = "select * from architects where aid=?"
    cur.execute(query, (aid,))
    res = cur.fetchall()
    cur.close()
    con.close()
    return res[0]

# Routes
@app.route("/", methods=["POST", "GET"])
def index():
    names = []
    aids = []
    if request.method == "POST":
        post_input = request.form.get("search_term")
        aids = list(set(get_aids(f"%{post_input}%")))
        if aids[0] != -1:
            for i in aids:
                names.append(get_architect_from_aid(i))
        
    return render_template("index.html", architects=names, ids=aids, count=len(aids))

@app.route("/architect")
def architect():
    architect_data = get_architect_info(int(request.args.get("aid", -1)))
    return render_template("architect.html", data=architect_data)

@app.route("/architects")
def architects():
    return render_template("architects.html")

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)