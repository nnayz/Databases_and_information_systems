from database.db import get_session, get_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import inspect
Base = declarative_base()

class ASCII(Base):
    __tablename__ = "ascii"
    id = Column(Integer, primary_key=True)
    letter = Column(String)
    value = Column(Integer)

engine = get_engine()
def create_tables():
    if not inspect(engine).has_table('ascii'):
        Base.metadata.create_all(bind=engine)
        populate_items()
    else:
        print("Table already exists")
    

def populate_items():
    session = get_session()
    for i in range(65, 90, 1): # 65 is the ASCII code for A, 90 is the ASCII code for Z
        session.add(ASCII(id=i, letter=chr(i), value=i))

    for i in range(97, 122, 1): # 97 is the ASCII code for a, 122 is the ASCII code for z
        session.add(ASCII(id=i, letter=chr(i), value=i))

    session.commit()

def get_ascii(letter: str):
    session = get_session()
    return session.query(ASCII.value).filter(ASCII.letter == letter).first().value

create_tables()

letter = input("Enter a letter: ")
print(get_ascii(letter))






