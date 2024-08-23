
def check_year(year: int) -> str|None:
    """
    Validates year value.

    In case of error returns error message.
    """
    if year < 0:
        return "Year cannot be negative."
    elif year < 1888:
        return "Year cannot be older than 1888."
    elif len(str(year)) > 4:
        return "Year cannot be 5 digit number."
    else:
        return None


def check_rating(rating: float) -> str|None:
    """
    Validates year value.

    In case of error returns error message.
    """
    if rating < 0:
        return "Rating cannot be negative."
    elif rating > 10:
        return "Rating cannot be more than 10."
    else:
        return None
    

def get_select_sql_query(sort: str) -> str:
    """
    Returns SQL query based on input sort.

    Note: "by_title" sort return query with ?.
    """
    if sort == "default":
        return "SELECT * FROM movies"
    elif sort == "year_ascend":
        return "SELECT * FROM movies ORDER BY year ASC"
    elif sort == "year_descend":
        return "SELECT * FROM movies ORDER BY year DESC"
    elif sort == "rating_ascend":
        return "SELECT * FROM movies ORDER BY rating ASC"
    elif sort == "rating_descend":
        return "SELECT * FROM movies ORDER BY rating DESC"
    elif sort == "by_title":
        return "SELECT * FROM movies WHERE title LIKE ?"
    else:
        raise Exception("Unexpected error")