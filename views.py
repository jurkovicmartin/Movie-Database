from flask import Blueprint, render_template, request, redirect, url_for

from database import get_database


views = Blueprint(__name__, "views")


@views.route("/")
def show():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return render_template("index.html", movies=movies)


@views.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        rating = request.form["rating"]

        db = get_database()
        db.execute("INSERT INTO movies (title, year, rating) VALUES (?, ?, ?)", (title, year, rating))
        db.commit()

        return redirect(url_for("views.show"))
    
    return render_template("add_movie.html")
