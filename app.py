from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
# Database opsætning
DB_ARCHITECTS = "./db/architects.db"

def get_db(db, query, params=()):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

# Routes
@app.route("/", methods=["POST"])
def index():
    if request.method == "POST":
        search_term = request.form.get("search_term", "")
        return db_search(search_term)
    return render_template("index.html", title="Home Page")

def db_search(search_term):
    query = """
        SELECT architects.*, buildings.* 
        FROM architects
        INNER JOIN buildings ON architects.aid = buildings.aid
        WHERE architects.name LIKE ?
    """
    
    data = get_db(DB_ARCHITECTS, query, ('%' + search_term + '%',))
    
    return render_template("index.html", data=data)


# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)