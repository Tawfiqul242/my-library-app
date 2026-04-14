from flask import Flask, render_template, request, redirect
import sqlite3
from db import create_table

app = Flask(__name__)

def get_books():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()

    # ADD BOOK
    if request.method == "POST":
        c.execute(
            "INSERT INTO books (title, author, status) VALUES (?, ?, ?)",
            (request.form["title"], request.form["author"], request.form["status"])
        )
        conn.commit()
        conn.close()
        return redirect("/")

    # GET FILTER VALUES
    search = request.args.get("search", "")
    status = request.args.get("status", "")

    # BASE QUERY
    query = "SELECT * FROM books WHERE 1=1"
    params = []

    # SEARCH FILTER (title + author)
    if search:
        query += " AND (title LIKE ? OR author LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    # STATUS FILTER (owned/reading/etc)
    if status:
        query += " AND status = ?"
        params.append(status)

    c.execute(query, params)
    books = c.fetchall()
    conn.close()

    return render_template("index.html", books=books, search=search, status=status)


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()

    # UPDATE STATUS
    if request.method == "POST":
        new_status = request.form["status"]
        c.execute("UPDATE books SET status=? WHERE id=?", (new_status, id))
        conn.commit()
        conn.close()
        return redirect("/")

    # GET CURRENT BOOK
    c.execute("SELECT * FROM books WHERE id=?", (id,))
    book = c.fetchone()
    conn.close()

    return render_template("edit.html", book=book)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)