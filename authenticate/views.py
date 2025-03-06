from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from login import lm
from flask_login import login_user, login_required, logout_user
from . import models
import hashlib

auth_blueprint = Blueprint('auth_blueprint', __name__)

@lm.user_loader
def user_loader(id):
    usuario = models.User.query.filter_by(id=id).first()
    return usuario

@auth_blueprint.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')

    email = request.form['emailForm']
    senha = request.form['senhaForm']

    if models.User.query.filter_by(email=email).first():
        return render_template('cadastro.html', mensagem='Já existe um usuário com este e-mail!')

    novo_usuario = models.User(email =email, password = senha)
    db.session.add(novo_usuario)
    db.session.commit()
    login_user(novo_usuario)
    return redirect(url_for('project_anac.filtro_data'))


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['emailForm']
    senha = request.form['senhaForm']

    usuario = models.User.query.filter_by(email=email, password=senha).first()
    if not usuario:
        return render_template('login.html', mensagem="Usuário e/ou senha incorretos")
    
    login_user(usuario)
    return redirect(url_for('project_anac.filtro_data'))

@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))