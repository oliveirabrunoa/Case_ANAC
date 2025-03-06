from flask import Blueprint, render_template, request, redirect
from . import models
from db import db
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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


@project_anac.route('/filtro_data', methods=['GET', 'POST'])
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
def grafico_rpk():
    lista_meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Meses de 1 a 12
    lista_anos = models.Voos.query.with_entities(models.Voos.ano).distinct().all()  # Anos distintos no banco
    anos_unicos = [ano[0] for ano in lista_anos]
    lista_mercados = models.Voos.query.with_entities(models.Voos.mercado).distinct().all()
    mercados_unicos = [mercado[0] for mercado in lista_mercados]

    if request.method == 'POST':
        mes_inicio = int(request.form['mes_inicio'])  # Convertendo para inteiro
        ano_inicio = int(request.form['ano_inicio'])  # Convertendo para inteiro
        mes_final = int(request.form['mes_final'])  # Convertendo para inteiro
        ano_final = int(request.form['ano_final'])  # Convertendo para inteiro
        mercado = request.form['mercado']  # Mercado selecionado

        # Filtrando voos no intervalo de datas
        voos = models.Voos.query.filter(
            (models.Voos.ano > ano_inicio) | 
            ((models.Voos.ano == ano_inicio) & (models.Voos.mes >= mes_inicio)),
            (models.Voos.ano < ano_final) | 
            ((models.Voos.ano == ano_final) & (models.Voos.mes <= mes_final)),
            models.Voos.mercado == mercado
        ).all()

        # Organizando os dados para o gráfico
        datas = []
        rpk_values = []

        for voo in voos:
            # Formatação do mês/ano para o eixo X
            data_formatada = f'{voo.mes}/{voo.ano}'
            datas.append(data_formatada)
            rpk_values.append(voo.rpk)

        # Criando o gráfico com Matplotlib
        fig, ax = plt.subplots(figsize=(13, 6))
        ax.plot(datas, rpk_values, marker='o', linestyle='-', color='b')

        # Adicionando título e rótulos aos eixos
        ax.set_title(f'Gráfico de RPK para o Mercado {mercado}')
        ax.set_xlabel('Data')
        ax.set_ylabel('RPK')

        # Rotacionando os rótulos do eixo X para melhor visualização
        plt.xticks(rotation=45)
        # Adicionando os valores de RPK no gráfico com mais casas decimais
        for i, v in enumerate(rpk_values):
            ax.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontsize=10)  # Ajuste para exibir até 2 casas decimais
        # Convertendo o gráfico para base64 para ser exibido na página HTML
        img_bytes = BytesIO()
        fig.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

        # Retornar o template com o gráfico gerado
        return render_template('grafico_rpk.html', img_base64=img_base64, meses=lista_meses, anos=anos_unicos, mercados=mercados_unicos)

    return render_template('grafico_rpk.html', meses=lista_meses, anos=anos_unicos,mercados=mercados_unicos)



    