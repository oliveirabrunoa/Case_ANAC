from flask import Blueprint, render_template, request, redirect, url_for
from . import models
from db import db
import plotly.graph_objects as go
from io import BytesIO
import base64
from flask_login import login_required

project_anac = Blueprint('project_anac', __name__)

@project_anac.route('/', methods=['GET'])
def index():
    voos = models.Voos.query.all()
    return redirect(url_for('auth_blueprint.login'))


@project_anac.route('/filtro_mercado', methods=['GET', 'POST'])
@login_required
def filtro_mercado():
    lista_mercados = models.Voos.query.with_entities(models.Voos.mercado).distinct().all()
    mercados_unicos = [mercado[0] for mercado in lista_mercados]

    if request.method=='POST':
        mercado_selecionado = request.form['mercado']
        print(mercado_selecionado)
        voos = models.Voos.query.filter_by(mercado=mercado_selecionado).all()
        return render_template('mercados.html', voos=voos, mercados=mercados_unicos)
    
    return render_template('mercados.html', mercados=mercados_unicos)


@project_anac.route('/filtro_data', methods=['GET', 'POST'])
@login_required
def filtro_data():
    lista_meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Meses de 1 a 12
    lista_anos = models.Voos.query.with_entities(models.Voos.ano).distinct().all()  # Anos distintos no banco
    anos_unicos = [ano[0] for ano in lista_anos]

    if request.method=='POST':
        mes_inicio = request.form['mes_inicio']
        ano_inicio = request.form['ano_inicio']
        mes_final = request.form['mes_final']
        ano_final = request.form['ano_final']
        
        voos = models.Voos.query.filter(
            (models.Voos.ano > ano_inicio) | 
            ((models.Voos.ano == ano_inicio) & (models.Voos.mes >= mes_inicio)),
            (models.Voos.ano < ano_final) | 
            ((models.Voos.ano == ano_final) & (models.Voos.mes <= mes_final))
            ).all()
        return render_template('datas.html', voos=voos,meses=lista_meses, anos=anos_unicos)
    
    return render_template('datas.html', meses=lista_meses, anos=anos_unicos)


@project_anac.route('/grafico_rpk', methods=['GET', 'POST'])
@login_required
def grafico_rpk():
    lista_meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lista_anos = models.Voos.query.with_entities(models.Voos.ano).distinct().all()
    anos_unicos = [ano[0] for ano in lista_anos]
    lista_mercados = models.Voos.query.with_entities(models.Voos.mercado).distinct().all()
    mercados_unicos = [mercado[0] for mercado in lista_mercados]

    if request.method == 'POST':
        mes_inicio = int(request.form['mes_inicio'])
        ano_inicio = int(request.form['ano_inicio'])
        mes_final = int(request.form['mes_final'])
        ano_final = int(request.form['ano_final'])
        mercado = request.form['mercado']

        voos = models.Voos.query.filter(
            (models.Voos.ano > ano_inicio) | 
            ((models.Voos.ano == ano_inicio) & (models.Voos.mes >= mes_inicio)),
            (models.Voos.ano < ano_final) | 
            ((models.Voos.ano == ano_final) & (models.Voos.mes <= mes_final)),
            models.Voos.mercado == mercado
        ).all()

        if not voos:
            return render_template('grafico_rpk.html', mensagem='Nenhum dado encontrado.', meses=lista_meses, anos=anos_unicos, mercados=mercados_unicos)

        datas = [f'{voo.mes}/{voo.ano}' for voo in voos]
        rpk_values = [voo.rpk for voo in voos]

        fig = go.Figure(data=go.Scatter(x=datas, y=rpk_values, mode='lines+markers', line=dict(color='blue')))
        fig.update_layout(title=f'Gráfico de RPK para o Mercado {mercado}', xaxis_title='Data', yaxis_title='RPK', xaxis_tickangle=-45)

        img_bytes = BytesIO()
        fig.write_image(img_bytes, format='png')
        img_bytes.seek(0)
        img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

        return render_template('grafico_rpk.html', img_base64=img_base64, meses=lista_meses, anos=anos_unicos, mercados=mercados_unicos)

    return render_template('grafico_rpk.html', meses=lista_meses, anos=anos_unicos, mercados=mercados_unicos)




    