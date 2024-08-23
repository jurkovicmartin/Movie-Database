from flask import Blueprint, render_template, request, redirect, url_for, flash

from database import get_database
from functions import check_rating, check_year, get_select_sql_query


views = Blueprint(__name__, "views")


@views.route("/", methods=["GET", "POST"])
def show():
    if request.method == "POST":
        sort = request.form.get("sort")
        # Get title to find
        if sort == "by_title":
            title = request.form.get("title")
        else: title = None
    # GET
    else:
        sort = "default"
        title = None

    db = get_database()
    cursor = db.cursor()
    # Passing variable to "by_title" query
    if sort == "by_title":
        cursor.execute(get_select_sql_query(sort), ("%"+title+"%",))
    else:
        cursor.execute(get_select_sql_query(sort))
        
    movies = cursor.fetchall()
    
    return render_template("index.html", movies=movies, selected_sort=sort, title=title)


@views.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get data from form
        title = request.form.get("title")
        year = request.form.get("year")
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        
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

        # Handle adding same film multiple times
        cursor = db.cursor()
        cursor.execute("SELECT title, year FROM movies")
        data = cursor.fetchall()
        titles = [title.lower() for title, _ in data]
        years = [year for _, year in data]

        if title.lower() in titles and int(year) in years:
            return render_template("add_movie.html", error=f"Movie {title} from {year} already exists.", title=None, year=None, rating=rating, comment=comment)

        # Add the movie
        db.execute("INSERT INTO movies (title, year, rating, comment) VALUES (?, ?, ?, ?)", (title, year, rating, comment))
        db.commit()

        flash(f"{title} movie has been added.", "info")
        return redirect(url_for("views.show"))
    # GET
    else:
        return render_template("add_movie.html", error=None, title=None, year=None, rating=None, comment=None)


@views.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        # Get data from database to show them in the editing form
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM movies WHERE id == ?", (id,))
        movie = cursor.fetchone()
    
        return render_template("edit_movie.html", error=None, title=movie[1], year=movie[2], rating=movie[3], comment=movie[4], id=id)
    # POST
    else:
        # Get data from form
        title = request.form.get("title")
        year = request.form.get("year")
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        
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

        # Handle adding same film multiple times
        # cursor = db.cursor()
        # cursor.execute("SELECT title, year FROM movies")
        # data = cursor.fetchall()
        # titles = [title.lower() for title, _ in data]
        # years = [year for _, year in data]

        # if title.lower() in titles and int(year) in years:
        #     return render_template("edit_movie.html", error=f"Movie {title} from {year} already exists.", title=None, year=None, rating=rating, comment=comment)

        # Edit movie
        db.execute("UPDATE movies SET title=?, year=?, rating=?, comment=? WHERE id == ?", (title, year, rating, comment, id))
        db.commit()

        flash(f"{title} movie has been edited.", "info")
        return redirect(url_for("views.show"))
    

@views.route("/delete/<id>")
def delete(id):
    db = get_database()
    cursor = db.cursor()

    # Get movie title for info message
    cursor.execute("SELECT title FROM movies WHERE id == ?", (id,))
    title = cursor.fetchone()

    # Delete the movie
    db.execute("DELETE FROM movies WHERE id == ?", (id,))
    db.commit()

    flash(f"{title[0]} movie has been deleted.")
    return redirect(url_for("views.show"))