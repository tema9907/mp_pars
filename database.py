from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config

# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/tenderok"
Base = declarative_base()
engine = create_async_engine(Config.DB_CONNECTION_STRING, future=True)
Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
