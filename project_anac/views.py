from flask import Blueprint, render_template, request, redirect
from . import models
from db import db

project_anac = Blueprint('project_anac', __name__)

@project_anac.route('/', methods=['GET'])
def index():
    voos = models.Voos.query.all()
    return render_template('index.html', voos=voos)

@project_anac.route('/filtro_mercado', methods=['GET', 'POST'])
def filtro_mercado():
    lista_mercados = models.Voos.query.with_entities(models.Voos.mercado).distinct().all()
    mercados_unicos = [mercado[0] for mercado in lista_mercados]

    if request.method=='POST':
        mercado_selecionado = request.form['mercado']
        print(mercado_selecionado)
        voos = models.Voos.query.filter_by(mercado=mercado_selecionado).all()
        return render_template('mercados.html', voos=voos, mercados=mercados_unicos)
    
    return render_template('mercados.html', mercados=mercados_unicos)





    