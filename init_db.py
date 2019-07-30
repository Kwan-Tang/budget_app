from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import config

Base = declarative_base()
meta= MetaData()
engine = create_engine(config.uri_keys)
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

class Transactions(Base):
    __tablename__ ='transactions'
    __table_args__={"extend_existing":True}
    id = Column(Integer,primary_key=True)
    date = Column(DateTime)
    description = Column(String(250),nullable=False)
    original_description = Column(String(250),nullable=False)
    amount = Column(Integer,nullable=False)
    transaction_type = Column(String(50),nullable=False)
    categories = Column(Integer,ForeignKey('expense_categories.id'))
    bank = Column(Integer,ForeignKey('accounts.id'))

Base.metadata.create_all(engine)

def add_accounts():
    session.query(Accounts).delete()
    bank_accounts = ['Bank of America','Citibank','Chase','Wellsfargo','US Bank','PNC','American Express','Cash']
    status = 'active'
    engine.execute(Accounts.__table__.insert(),[dict(name=bank_account,status=status) for bank_account in bank_accounts])

def add_categories():
    session.query(Categories).delete()
    expense_categories = ["Credit Card Payment","Transfer","Groceries","Shopping","Utilities","Food & Dining"
                          ,"Doctor","Mortgage & Rent","Cash & ATM","Gas & Fuel","Income","Travel","Entertainment"]
    engine.execute(Categories.__table__.insert(),[dict(name=expense_category) for expense_category in expense_categories])

add_accounts()
add_categories()
session.commit()

accounts = session.query(Accounts.name).all()
print(accounts)
