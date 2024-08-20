from flask import Flask

from views import views
from database import close_database

app = Flask(__name__)

app.register_blueprint(views, url_prefix="/")

@app.teardown_appcontext
def teardown_database(exception):
    close_database(exception)



if __name__ == "__main__":
    app.run(debug=True, port=8000)