from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from login import lm
from flask_login import login_user
from . import models

auth_blueprint = Blueprint('auth_blueprint', __name__)

@lm.user_loader
def user_loader(id):
    usuario = models.User.query.filter_by(id=id).first()
    return usuario

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    #check_user = models.User.filter(email=)
    nome = request.form['nomeForm']
    email = request.form['emailForm']
    senha = request.form['senhaForm']

    '''if models.User.filter_by(email=email).first():
        flash('Já existe um usuário cadastrado com este e-mail')
        return render_template('login.html')
'''
    novo_usuario = models.User(email =email, password = senha, name=nome)
    db.session.add(novo_usuario)
    db.session.commit()
    login_user(novo_usuario)
    return redirect(url_for('project_anac.filtro_data'))