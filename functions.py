
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
    elif rating > 5:
        return "Rating cannot be more than 5."
    else:
        return None
    
