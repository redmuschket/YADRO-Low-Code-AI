import logging
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine

from core.db.db import Base
from core.db.models import *

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

target_metadata = Base.metadata

DB_USER = os.getenv("POSTGRES_USERNAME", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "notification")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

config.set_main_option("sqlalchemy.url", DATABASE_URL)


def render_item(type_, obj, autogen_context):
    """A function for automatically adding custom type imports."""
    if type_ == "type" and obj.__class__.__module__.startswith("core."):
        autogen_context.imports.add(f"import {obj.__class__.__module__.split('.')[0]}")
    return False


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=False,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        logger.info("=== STARTING MIGRATION ===")
        logger.info(f"Target metadata tables: {list(target_metadata.tables.keys())}")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            compare_type=True,
            compare_server_default=True,
            include_schemas=False,
        )

        with context.begin_transaction():
            context.run_migrations()
        logger.info("=== MIGRATION COMPLETED ===")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
