from sqlmodel import Session, SQLModel, create_engine


from sqlmodel import Session, SQLModel, create_engine


DATABASE_URL = "sqlite:///facility_work_orders.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    """Create database tables defined by SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Provide a database session for API requests."""
    with Session(engine) as session:
        yield session
