from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sql_scheme='mysql+mysqlconnector://crawl:74108520@localhost:3306/crawl'
engine = create_engine(sql_scheme,convert_unicode=True)
db_session=scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()