from sqlalchemy import Column, String, create_engine, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from jiangsu.conf.parseconf import scrapy_conf

Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'users'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    username = Column(String)
    pwd = Column(String)
    tel = Column(String)


# 定义User对象:
class TaskInfo(Base):
    # 表的名字:
    __tablename__ = 'task_info'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    url = Column(String)
    taskname = Column(String)
    rulename = Column(String)
    rulecontent = Column(String)
    uuid = Column(String)
    dongtai = Column(String)
    delay_time = Column(String)
    zuhe_link = Column(String)
    zengliang = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))


# 定义TaskStatuss对象:
class TaskStatus(Base):
    # 表的名字:
    __tablename__ = 'task_status'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    pid = Column(Integer)
    status = Column(Integer)
    taskid = Column(Integer)


engine = create_engine(scrapy_conf.get_sqlalchemy())
DBSession = sessionmaker(bind=engine)
# 创建DBSession类型:


if __name__ == '__main__':
    # 初始化数据库连接:
    session = DBSession()
    new_user = TaskStatus(pid=10, taskid=2)
    session.add(new_user)
    session.commit()
    session.close()
