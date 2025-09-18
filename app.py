from flask import Flask, request
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()


    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    ''')


    columns = [col[1] for col in c.execute("PRAGMA table_info(users)").fetchall()]

    if "lastname" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN lastname TEXT")

    if "phone" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN phone TEXT")

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return '''
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Gebruiker toevoegen</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(to right, #74ebd5, #ACB6E5);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                    width: 350px;
                    text-align: center;
                }
                input {
                    width: 90%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px;
                    width: 100%;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #45a049;
                }
                a {
                    display: inline-block;
                    margin-top: 15px;
                    text-decoration: none;
                    color: #335;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Nieuwe gebruiker toevoegen</h2>
                <form method="post" action="/add">
                    <input type="text" name="name" placeholder="Voornaam"><br>
                    <input type="text" name="lastname" placeholder="Achternaam"><br>
                    <input type="email" name="email" placeholder="E-mailadres"><br>
                    <input type="text" name="phone" placeholder="Telefoonnummer"><br>
                    <button type="submit">Opslaan</button>
                </form>
                <a href="/list">📜 Bekijk alle gebruikers</a>
            </div>
        </body>
        </html>
    '''

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    phone = request.form["phone"]

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name, lastname, email, phone) VALUES (?, ?, ?, ?)", 
              (name, lastname, email, phone))
    conn.commit()
    conn.close()

    return "✅ Gebruiker opgeslagen <br><a href='/'>🔙 Terug</a>"

@app.route("/list")
def list_users():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    html = '''
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Gebruikerslijst</title>
        <style>
            body { font-family: Arial; background: #f0f0f0; padding: 20px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; border: 1px solid #ccc; text-align: center; }
            th { background: #4CAF50; color: white; }
            tr:nth-child(even) { background: #f9f9f9; }
            a { display: inline-block; margin-top: 20px; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>📜 Gebruikerslijst</h1>
        <table>
            <tr>
                <th>Voornaam</th>
                <th>Achternaam</th>
                <th>E-mailadres</th>
                <th>Telefoonnummer</th>
            </tr>
    '''
    for user in users:

        html += f"<tr><td>{user[1]}</td><td>{user[3]}</td><td>{user[2]}</td><td>{user[4]}</td></tr>"
    html += "</table><a href='/'>🔙 Terug</a></body></html>"
    return html

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
