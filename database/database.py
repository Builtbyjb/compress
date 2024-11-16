from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine


class UploadFiles(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    uploaded: datetime = Field(index=True)
    expired: datetime = Field(index=True)


class DownloadFiles(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    uploaded: datetime = Field(index=True)
    expired: datetime = Field(index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Keeps session opened
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
