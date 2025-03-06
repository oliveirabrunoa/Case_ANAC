from flask import Flask
from project_anac.views import project_anac
from db import db

app = Flask(__name__)  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_anac.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(project_anac)

if __name__ == '__main__':
    app.run(debug=True)