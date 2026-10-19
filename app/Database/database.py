from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from app.Settings.SecretSettings import settings

DATABASE_URL=settings.database_url

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(bind=engine,autoflush=False)

Base=declarative_base()

