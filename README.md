# Movie Database

Web application that allows user to manage a movie database.

## Features

- Adding / editing / deleting movies

- Deleting modal to confirm deletion

- Paging in case of many movies

- Sorting
    - by year
    - by rating
    - by title

## Functionality

Database was made in sqlite.

Web development was done with flask.

When started application runs at localhost address on port 8000.

**Database structure:**

| id                    | title   | year     | rating | comment |
|-----------------------|---------|----------|--------|---------|
| INTEGER + PRIMARY KEY | VARCHAR | SMALLINT | FLOAT  | VARCHAR |