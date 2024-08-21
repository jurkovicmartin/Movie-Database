from flask import Blueprint, render_template, request, redirect, url_for

from database import get_database
from functions import check_rating, check_year


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
        comment = request.form["comment"]
        
        # Validate input values
        year_error = check_year(int(year))
        rating_error = check_rating(float(rating))
        # Error in both values
        if year_error and rating_error:
            return render_template("add_movie.html", error=year_error+" "+rating_error, title=title, year=None, rating=None, comment=comment)
        # Error in only one value
        elif year_error:
            return render_template("add_movie.html", error=year_error, title=title, year=None, rating=rating, comment=comment)
        elif rating_error:
            return render_template("add_movie.html", error=rating_error, title=title, year=year, rating=None, comment=comment)
        # Values are ok
        else: pass

        db = get_database()
        db.execute("INSERT INTO movies (title, year, rating, comment) VALUES (?, ?, ?, ?)", (title, year, rating, comment))
        db.commit()

        return redirect(url_for("views.show"))
    
    return render_template("add_movie.html", error=None, title=None, year=None, rating=None, comment=None)


@views.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM movies WHERE id == ?", (id,))
        movie = cursor.fetchone()
    
        return render_template("edit_movie.html", error=None, title=movie[1], year=movie[2], rating=movie[3], comment=movie[4], id=id)
    # POST
    else:
        title = request.form["title"]
        year = request.form["year"]
        rating = request.form["rating"]
        comment = request.form["comment"]
        
        # Validate input values
        year_error = check_year(int(year))
        rating_error = check_rating(float(rating))
        # Error in both values
        if year_error and rating_error:
            return render_template("edit_movie.html", error=year_error+" "+rating_error, title=title, year=None, rating=None, comment=comment, id=id)
        # Error in only one value
        elif year_error:
            return render_template("edit_movie.html", error=year_error, title=title, year=None, rating=rating, comment=comment, id=id)
        elif rating_error:
            return render_template("edit_movie.html", error=rating_error, title=title, year=year, rating=None, comment=comment, id=id)
        # Values are ok
        else: pass

        db = get_database()
        db.execute("UPDATE movies SET title=?, year=?, rating=?, comment=? WHERE id == ?", (title, year, rating, comment, id))
        db.commit()

        return redirect(url_for("views.show"))
    

@views.route("/delete/<id>")
def delete(id):
    db = get_database()
    db.execute("DELETE FROM movies WHERE id == ?", (id))
    db.commit()

    return redirect(url_for("views.show"))