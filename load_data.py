import pandas as pd
from db import db

data = pd.read_csv('Dados_Estatisticos.csv', header=1, sep=';')
filtro= data[(data['EMPRESA_SIGLA'] ==  "GLO")]
print(filtro)