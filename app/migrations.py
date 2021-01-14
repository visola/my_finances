import os
from alembic import command
from alembic.config import Config

def run_migrations(migrations_dir: str, dsn: str) -> None:
    print(f"Running migrations from {migrations_dir}")
    alembic_cfg = Config()
    alembic_cfg.config_file_name = f"{os.getcwd()}/alembic.ini"
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')
