from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)  
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    with app.app_context():
        db.create_all() 
        return app

if __name__=='__main__':
    app = create_app()
    app.run(debug=True)