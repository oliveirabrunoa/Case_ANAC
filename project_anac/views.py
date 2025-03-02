from flask import Blueprint, render_template
from flask import request

project_anac = Blueprint('project_anac', __name__)

@project_anac.route('/')
def index():
    return render_template('index.html')