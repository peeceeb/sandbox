
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_url = os.getenv("DATABASE_URL")
if not db_url:
	raise RuntimeError(
		"DATABASE_URL is not set. Set it to your PostgreSQL connection string "
		"before starting the application."
	)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
