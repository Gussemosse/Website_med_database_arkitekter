from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
# Database opsætning
DB_ARCHITECTS = "./db/arcitects.db"

# Routes
@app.route("/")
def index():
    return render_template("index.html", title="Home Page")

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)