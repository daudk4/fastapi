from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as PG
from sqlalchemy.sql import func
from datetime import datetime
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(
            PG.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(
        sa_column=Column(
            PG.TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            PG.TIMESTAMP(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )

    def __repr__(self):
        return f"<Book {self.title}>"
