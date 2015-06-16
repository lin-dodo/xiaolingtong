from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from class_models import *
engine=create_engine('sqlite:///temp.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class db_handle:
    def __init__(self):
        self.session=db_session()
    def __del__(self):
        self.session.close()
if __name__=='__main__':
    d1=db_handle()
    t=d1.session.query(task.status).filter(task.set_date<='2015-5-31 23:00')
    u=t.all()
    #c=contacts(id=None,group_name='banji',username='1234',contact_name='wang',contact='110',type='phone')
    print u[1]

    #d1.session.add(c)
    #d1.session.commit()

