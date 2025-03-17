from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://ArinaKostanyan:IHopeIWill@localhost:3306/scrapping_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print('seccesfull')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
