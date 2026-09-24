from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
# Database opsætning
DB_ARCHITECTS = "./db/architects.db"

# Funktion der søger i databasen og finder arkitekt-ID'er baseret på bygningsnavn
def get_aids(search):
    con = sqlite3.connect(DB_ARCHITECTS)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # Henter arkitekt id fra tabellen buildings, hvor like gør, at jeg kun behøver at søge på dele af ordet :)
    query = "select aid from buildings where name like ? or year like ? or location like ?"
    cur.execute(query, (search, search, search,))
    res = cur.fetchall()
    cur.close()
    con.close()
    # Løber alle resultaterne igennem, trækker det allerførste element ud (arkitektens ID-tal) og laver det om til en ren liste af tal
    # Hvis databasen ikke finder noget, så bliver [-1] retuneret som liste med et element.
    return [list(r)[0] for r in res] if res != [] else [-1]

# Her bliver der hentet et specifikt arkitekt navn
def get_architect_from_aid(aid):
    con = sqlite3.connect(DB_ARCHITECTS)
    cur = con.cursor()
    # Henter navnet fra tabellen architects, hvor aid passer præcis med det ID-tal, der sendes med ind.
    query = "select name from architects where aid=?"
    cur.execute(query, (aid,))
    # Da hvert ID er unikt for en arkitekt, bruges fetchone().
    res = cur.fetchone()
    cur.close()
    con.close()
    # Returnerer selve navnestringen (f.eks. "Gustave Eiffel"), så den kan vise den på skærmen.
    return res[0]

# Henter ALT data om en arkitekt, for at blive sendt ind på profilsiden af specifik arkitekt (/architect?aid=X).
def get_architect_info(aid):
    con = sqlite3.connect(DB_ARCHITECTS)
    con.row_factory = sqlite3.Row # <- så jeg kan bruge mine kolonnenavne direkte til bedre styling
    cur = con.cursor()
    #Henter alle kolonner fra tabellen architects, for den specifikke arkitekt-ID.
    query = "select * from architects where aid=?"
    cur.execute(query, (aid,))
    res = cur.fetchall()
    cur.close()
    con.close()
    # Henter dataene og returnerer den første række. Det giver en samlet liste med alle informationerne om arkitekten
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

# Henter alt data, uden et aid - det er til den fulde arkitekt side, med en liste over alle arkitekter.
def get_all_architect_info():
    con = sqlite3.connect(DB_ARCHITECTS)
    cur = con.cursor()
    query = "select * from architects"
    cur.execute(query,)
    res = cur.fetchall()
    cur.close()
    con.close()
    return res

@app.route("/architects")
def architects():
    info = get_all_architect_info()
    return render_template("architects.html", all=info)

@app.route("/dokumentationside")
def dokument():
    return render_template("dokumentationside.html")

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)