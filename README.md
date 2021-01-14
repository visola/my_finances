# my_finances

![Build](https://github.com/VinnieApps/my_finances/workflows/Build/badge.svg)

## local development

### banco de dados
- criar um banco de dados no MySQL

### configuração

Crie um arquivo `config.ini` na raíz deste diretório com as seguintes informações dentro:

```ini
[DEFAULT]

APP_SECRET_KEY={CRYPTO_KEY_FOR_SESSION}

MYSQL_DATABASE={DATABASE_NAME}
MYSQL_HOST={DATABASE_HOST}
MYSQL_PASSWORD={DATABASE_PASSWORD}
MYSQL_USER={DATABASE_USERNAME}
```

### instalação

- Entrar no diretorio correto: `cd <diretório>`
- Para criar um ambiente virtual: `python3 -m venv venv`
  - Para ativar um ambiente já existente no Windows: `venv\Scripts\Activate.bat`
  - Para ativar um ambiente já existente no Mac ou Unix: `source venv/bin/activate`
- Instalar as dependências: `python setup.py install`

### rodando a aplicação

- Rodar a aplicação em modo desenvolvimento:
  ```
    set FLASK_ENV=development
    set FLASK_DEBUG=1
    python -m flask run
  ```
- Abrir no browser: http://localhost:5000/login
