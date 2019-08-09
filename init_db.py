from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,MetaData,Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import config

Base = declarative_base()
meta= MetaData()
engine = create_engine(config.uri)
Session = sessionmaker(bind=engine)
session = Session()

class Accounts(Base):
    __tablename__ = "accounts"
    __table_args__={"extend_existing":True}
    id = Column(Integer,primary_key=True)
    name = Column(String(250),nullable=False)

class Categories(Base):
    __tablename__ ='expense_categories'
    __table_args__={"extend_existing":True}
    id = Column(Integer,primary_key=True)
    name = Column(String(50),nullable=False)

class Transactions(Base):
    __tablename__ ='transactions'
    __table_args__={"extend_existing":True}
    id = Column(Integer,primary_key=True)
    date = Column(DateTime)
    description = Column(String(250),nullable=False)
    amount = Column(Float,nullable=False)
    category = Column(Integer,ForeignKey('expense_categories.id'))
    bank = Column(Integer,ForeignKey('accounts.id'))

Base.metadata.create_all(engine)

def add_accounts(bank_account):
    session.query(Accounts).delete()
    status = 'active'
    engine.execute(Accounts.__table__.insert(),[dict(name=bank_account)])

def add_categories(expense_category):
    session.query(Categories).delete()
    engine.execute(Categories.__table__.insert(),[dict(name=expense_category)])

def add_transactions(transactions):
    session.query(Transactions).delete()
    engine.execute(Transactions.__table__.insert(),[dict(date=transactions[0],
                                                        description=transactions[1],
                                                        amount=transactions[2],
                                                        category=transactions[3],
                                                        bank=transactions[4])])

add_accounts('Chase')
add_categories('Expense')
add_transactions(['07/31/2019','Payroll',3000,1,1])
session.commit()
session.close()
engine.dispose()
print("Success!")
