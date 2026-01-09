from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config
from sqlmodel import SQLModel


async_engine = create_async_engine(Config.DATABASE_URL, echo=True)


# THIS FUNCTION IS RESPONSIBLE FOR CREATING TABLES IN DATABASE
async def init_db() -> None:
    async with async_engine.begin() as conn:
        # IMPORTING MODELS INSIDE THE FUNCTION IS IMPORTANT BECAUSE SQLModel ONLY KNOWS ABOUT MODELS THAT HAVE BEEN IMPORTED.
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


# THIS FUNCTION IS HOW YOUR API GETS A DB CONNECTION FOR EACH REQUEST.
# WITHOUT THE SESSION YOU CANNOT QUERY THE DATABASE.
# WITHOUT THE SESSION YOU CANNOT INSERT/UPDATE/DELETE DATA FROM DB.
# WITHOUT THIS YOU CANNOT USE SQLMODEL ORM
async def get_session() -> AsyncSession:
    # SESSIONMAKER IS A FACTORY. IT DOES NOT CREATE A SESSION YET. IT CREATES A FUCNTION THAT CAN CREATE SESSION.
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        yield session
