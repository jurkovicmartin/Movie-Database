from flask import Flask

from views import views
from database import close_database

app = Flask(__name__)
# Key because of using flask flash (session)
app.secret_key = b"hzdb5kpi4U"

app.register_blueprint(views, url_prefix="/")

@app.teardown_appcontext
def teardown_database(exception):
    close_database(exception)



if __name__ == "__main__":
    app.run(port=8000)