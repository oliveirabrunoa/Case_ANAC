from flask import Flask
from project_anac.views import project_anac
from authenticate.views import auth_blueprint
from db import db
from login import lm
from flask_login import LoginManager

app = Flask(__name__)  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_anac.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'super secret key'

db.init_app(app)
lm.init_app(app)
app.register_blueprint(project_anac)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)