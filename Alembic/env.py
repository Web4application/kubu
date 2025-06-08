from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, MetaData
from alembic import context

# Import your various declarative bases
from app.models import Base as AppBase
from user.models import Base as UserBase
from another.models import Base as AnotherBase

# Alembic Config object
config = context.config

# Configure Python logging
fileConfig(config.config_file_name)

# Merge multiple metadata instances
merged_metadata = MetaData()
for base in [AppBase, UserBase, AnotherBase]:
    for table in base.metadata.tables.values():
        table.tometadata(merged_metadata)

# Assign merged metadata
target_metadata = merged_metadata

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# Run migrations depending on the mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
