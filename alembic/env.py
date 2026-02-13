from backend.app.database import engine, Base
import backend.app.models  # ensure models are imported so Alembic sees them

target_metadata = Base.metadata

def run_migrations_online():
    from alembic import context
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()