import pymysql
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import matplotlib.pyplot as plt

Base = declarative_base()

class BilibiliUser(Base):
    __tablename__ = 'bilibili_user'

    mid = Column(Integer(), nullable=False, primary_key=True)
    birthday = Column(String(30), nullable=False)
    follower = Column(Integer(), nullable=False)
    following = Column(Integer(), nullable=False)
    level = Column(Integer(), nullable=False)
    rank = Column(Integer(), nullable=False)
    sex = Column(String(30), nullable=False)
    view = Column(Integer(), nullable=False)

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

engine = create_engine('mysql+mysqlconnector://root@localhost:3306/bilibili')
DBSession = sessionmaker(bind=engine)
session = DBSession()

level = []
label = []
for i in range(1, 13):
    user = session.query(BilibiliUser).filter(BilibiliUser.birthday.startswith(str(i).zfill(2))).all()
    level.append(len(user))
    label.append(str(i) + "月")

plt.bar(range(1, 13), level)
plt.xticks(range(1, 13), label)
plt.title("哔哩哔哩用户生日分析")
plt.show()
