# Case ANAC

Este projeto foi desenvolvido como etapa de avaliação técnica. Foi desenvolvido em Python, utilizando o framework Flask e SQLAlchemy, e bibliotecas como pandas, plotly, dentre outras.

## Getting Started



### Prerequisites

O que você precisa para instalar o software e como instalá-lo

```
Python 3.5 or superior

```
### Installing

Crie um ambiente virtual 

```
python3 -m venv myvenv
```

Ative o ambiente virtual 

```
source myvenv/bin/activate (linux)

ou

myvenv/Scripts/activate (windows)
```

Instale as dependências do projeto descritas no requirements.txt
```
pip install -r requirements
```

### Running

Faça o download da base de dados "Dados_Estatisticos.csv" disponível em: 

https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/

Em seguida, faça a carga dos dados

```
python load_data.py
```

Execute a aplicação

```
python run.py
```

### Deployment

Acesse a aplicação disponível em: https://brunooliveira.pythonanywhere.com/login

