from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,MetaData,Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import config
import wx
import datetime

Base = declarative_base()
meta= MetaData()
engine = create_engine('postgres://ryynqiogpfhfdv:6f049cb5190bcc742151a7f9dacbfd58dae81913f2f35f627e8fe5030cc4ecde@ec2-54-225-103-167.compute-1.amazonaws.com:5432/d9au2t8fb1nhng')
Session = sessionmaker(bind=engine)
session = Session()

class Accounts(Base):
    __tablename__ = "accounts"
    __table_args__={"extend_existing":False}
    id = Column(Integer,primary_key=True)
    name = Column(String(250),nullable=False)

class Categories(Base):
    __tablename__ ='expense_categories'
    __table_args__={"extend_existing":False}
    id = Column(Integer,primary_key=True)
    name = Column(String(50),nullable=False)

class Transactions(Base):
    __tablename__ ='transactions'
    __table_args__={"extend_existing":False}
    id = Column(Integer,primary_key=True)
    date = Column(DateTime)
    description = Column(String(250),nullable=False)
    amount = Column(Float,nullable=False)
    category = Column(Integer,ForeignKey('expense_categories.id'))
    bank = Column(Integer,ForeignKey('accounts.id'))

Base.metadata.create_all(engine)

def add_accounts():
    bank_account = wx.TextEntryDialog(parent=None,message="Please enter your first account.")
    bank_account.Show()
    if bank_account.ShowModal() == 5101:
        return
    bank_account.Destroy()
    engine.execute(Accounts.__table__.insert(),[dict(name=bank_account.GetValue())])

def add_categories():
    category = wx.TextEntryDialog(parent=None,message="Please enter your first expense category.")
    category.Show()
    if category.ShowModal() == 5101:
        return
    category.Destroy()
    engine.execute(Categories.__table__.insert(),[dict(name=category.GetValue())])

def add_transactions():
    desc = wx.TextEntryDialog(parent=None,message="Please enter the description of the expense.")
    desc.Show()
    if desc.ShowModal() == 5101:
        return
    description = desc.GetValue()
    desc.Destroy()

    amt = wx.TextEntryDialog(parent=None,message="Please enter the amount of the expense.")
    amt.Show()
    if amt.ShowModal() == 5101:
        return
    amount = amt.GetValue()
    amt.Destroy()
    engine.execute(Transactions.__table__.insert(),
                   [dict(date=datetime.date.today(),description=description,amount=amount,category=1,bank=1)])

if __name__=="__main__":
    app = wx.App()
    app.MainLoop()
    add_accounts()
    add_categories()
    add_transactions()
    session.commit()
    session.close()
    engine.dispose()
    print("Success!")
