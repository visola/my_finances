# my_finances

## local development

- Entrar no diretorio correto: `cd <diretório>`
- Para criar um ambiente virtual: `python3 -m venv venv`
  - Para ativar um ambiente já existente: `venv\Scripts\Activate.bat`
- Instalar as dependências: `pip install -r requirements.txt`
- Rodar a aplicação em modo desenvolvimento:
  ```
    set FLASK_ENV=development
    python -m flask run
  ```
- Abrir no browser: http://localhost:5000/
