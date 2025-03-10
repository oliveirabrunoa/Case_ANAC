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
with app.app_context(): 
    db.create_all()

lm.init_app(app)
lm.login_view = 'auth_blueprint.login'
app.register_blueprint(project_anac)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 5000)