# my_finances

## local development

### banco de dados
- criar um banco de dados no MySQL
- acessar o banco `use <banco>`
- utilizar o arquivo [script_my_finances.sql](script_my_finances.sql) e aplicar seus comandos
- para ativar as paginas do browser, use as intruções de ## local development na linha de comnando

### configuração

Crie um arquivo `app/config.py` com as seguintes informações dentro:

```python
MYSQL_DATABASE='{DATABASE_NAME}'
MYSQL_HOST='{DATABASE_HOST}'
MYSQL_PASSWORD='{DATABASE_PASSWORD}'
MYSQL_USER='{DATABASE_USERNAME}'
MSQL_SECRET_KEY='{CRYPTO_KEY_FOR_SESSION}'
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
