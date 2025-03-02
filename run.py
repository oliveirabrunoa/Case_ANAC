from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all() 
    
@app.route("/")
def index():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)