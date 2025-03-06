import pandas as pd
from db import db
from run import app
from project_anac.models import Voos

def create_database():
    # Criação do banco e tabelas
    with app.app_context():
        db.drop_all() #deletar o banco a cada execução do script load_data.py     
        db.create_all()
    print("Banco de dados e tabelas criados com sucesso!")

def load_data_csv():
    data_frame = pd.read_csv('Dados_Estatisticos.csv', header=1, sep=';')
    filtro = data_frame[(data_frame['EMPRESA_SIGLA'] == 'GLO') & 
                        (data_frame['GRUPO_DE_VOO'] == 'REGULAR') &
                        (data_frame['NATUREZA']== 'DOMÉSTICA')]

    colunas_selecionadas = filtro[['EMPRESA_SIGLA','GRUPO_DE_VOO','NATUREZA',
                                'AEROPORTO_DE_ORIGEM_SIGLA','AEROPORTO_DE_DESTINO_SIGLA',
                                'MES','ANO','RPK']]
    
    colunas_selecionadas = colunas_selecionadas.copy()
    colunas_selecionadas['RPK'].fillna(0, inplace=True)

    dados_voos = colunas_selecionadas.values.tolist()
    insert_database(dados_voos)

def insert_database(dados_voos):
    voos_filtrados = []
    for voo in dados_voos:
        rpk = voo[7] if voo[7] not in [None, "NULL", ""] else 0
        voo = Voos(ano = voo[6],
            mes = voo[5],
            mercado = ''.join(sorted([voo[3], voo[4]])),
            rpk = rpk)
        voos_filtrados.append(voo)

    with app.app_context():
        db.session.add_all(voos_filtrados)  # Adiciona o objeto à sessão
        db.session.commit()        # Confirma a transação no banco
        print("Novos voos inseridos com sucesso!")


if __name__ == '__main__':
    create_database()
    load_data_csv()