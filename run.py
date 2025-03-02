from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from project_anac.views import project_anac

app = Flask(__name__)  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.register_blueprint(project_anac)
db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all() 
    
if __name__=='__main__':
    app.run(debug=True)