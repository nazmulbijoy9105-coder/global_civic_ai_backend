import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()
config = context.config
config.set_main_option("sqlalchemy.url", os.environ.get("postgresql://civicuser:eC4wiydQALfMdj9YuRiVMp51n1M7eZCr@dpg-d6nf6ifgi27c7393q0u0-a.oregon-postgres.render.com/civic_ai_lmxt", ""))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import Base
from app import models  # ✅ ensures all models are registered

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()