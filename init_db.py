from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,MetaData
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
    status = Column(String(50),nullable=False)

class Categories(Base):
    __tablename__ ='expense_categories'
    __table_args__={"extend_existing":True}
    id = Column(Integer,primary_key=True)
    name = Column(String(50),nullable=False)
    type = Column(String(50),nullable=False)

class Transactions(Base):
    __tablename__ ='transactions'
    __table_args__={"extend_existing":True}
    id = Column(Integer,primary_key=True)
    date = Column(DateTime)
    description = Column(String(250),nullable=False)
    original_description = Column(String(250),nullable=False)
    amount = Column(Integer,nullable=False)
    transaction_type = Column(String(50),nullable=False)
    category = Column(Integer,ForeignKey('expense_categories.id'))
    bank = Column(Integer,ForeignKey('accounts.id'))

Base.metadata.create_all(engine)

def add_accounts(bank_accounts):
    session.query(Accounts).delete()
    status = 'active'
    engine.execute(Accounts.__table__.insert(),[dict(name=bank_account,status=status) for bank_account in bank_accounts])

def add_categories(expense_categories):
    session.query(Categories).delete()
    engine.execute(Categories.__table__.insert(),[dict(name=expense_category[0],type=expense_category[1]) for expense_category in [expense_categories]])

def add_transactions(transactions):
    session.query(Transactions).delete()
    engine.execute(Transactions.__table__.insert(),[dict(date=transaction[0],
                                                        description=transaction[1],
                                                        original_description=transaction[2],
                                                        amount=transaction[3],
                                                        transaction_type=transaction[4],
                                                        category=transaction[5],
                                                        bank=transaction[6]) for transaction in [transactions]])

add_accounts(['Chase'])
add_categories(['Income','Revenue'])
add_transactions(['07/31/2019','Check','Payroll',3000,'credit',1,1])
session.commit()
session.close()
engine.dispose()
print("Success!")
