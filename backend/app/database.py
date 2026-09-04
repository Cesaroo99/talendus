from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import get_settings

settings = get_settings()

connect_args = {}
engine_kwargs: dict = {"pool_pre_ping": settings.app_env != "test"}
use_sqlite = settings.app_env == "test" or settings.database_url.startswith("sqlite")
if use_sqlite:
    connect_args["check_same_thread"] = False
    if settings.app_env == "test" or ":memory:" in settings.database_url or settings.database_url.rstrip("/") == "sqlite:":
        engine_kwargs["poolclass"] = StaticPool
elif settings.app_env != "test":
    engine_kwargs.update(pool_size=5, max_overflow=10, pool_recycle=1800)

engine = create_engine(
    "sqlite://" if settings.app_env == "test" else settings.database_url,
    connect_args=connect_args,
    **{k: v for k, v in engine_kwargs.items() if v is not False},
)

if use_sqlite:
    @event.listens_for(engine, "connect")
    def _sqlite_pragma(dbapi_connection, _connection_record):  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app import models  # noqa: F401 — enregistre les métadonnées
    from app.schema_repair import ensure_contracts_schema, ensure_interviews_schema

    Base.metadata.create_all(bind=engine)
    ensure_contracts_schema(engine)
    ensure_interviews_schema(engine)
