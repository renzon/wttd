# wttd

[![Build Status](https://travis-ci.org/renzon/wttd.svg?branch=master)](https://travis-ci.org/renzon/wttd)
[![Code Health](https://landscape.io/github/renzon/wttd/master/landscape.svg?style=flat)](https://landscape.io/github/renzon/wttd/master)
[![Updates](https://pyup.io/repos/github/renzon/wttd/shield.svg)](https://pyup.io/repos/github/renzon/wttd/)
[![Python 3](https://pyup.io/repos/github/renzon/wttd/python-3-shield.svg)](https://pyup.io/repos/github/renzon/wttd/)

Projeto de Estudo do curso Welcome to the Django.

## Como desenvolver?

1. Clone o repositório
2. Cria um virtualenv com Python 3.5
3. Ative o virtualenv
4. Instale as dependências
5. Configure as instâncias com o .env
6. Execute os testes

```console
git clone git@github.com:renzon/wttd.git
cd wttd
python -m venv venv
sourve venv/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample
pytest .
```

## Como fazer deplos?

1. Crie uma instância no Heroku
2. Envie as configurações para o Heroku
3. Defina uma SECRET_KEY segura para a instância
4. Defina DEBUG=False
5. Configure o serviço de email
6. Envie o código para o Heroku

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py
heroku config:set DEBUG=False
# configure o email
git push heroku master
```
