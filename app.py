from flask import Flask, render_template, request, redirect
import sqlite3
from db import create_table

app = Flask(__name__)
create_table()

def get_books():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)",
                  (request.form["title"], request.form["author"], request.form["status"]))
        conn.commit()
        conn.close()
        return redirect("/")

    books = get_books()
    return render_template("index.html", books=books)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")