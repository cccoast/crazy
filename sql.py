

import pandas as pd
import MySQLdb as mdb
import pandas.io.sql as psql
from  sqlalchemy import *
import numpy as np
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

''' NAIVE '''
query1 = 'select * from dept_manager'
query2 = 'select * from departments order by dept_no'
query3 = 'select * from salaries'
conn1 = mdb.connect(host = '127.0.0.1',user = 'root',passwd = '123',port = 3306,db = 'employees')
cur = conn1.cursor()
cur.execute(query1)
#for row in cur:
#    print row
cur.close()
conn1.commit()
 
cur = conn1.cursor()
cur.execute(query1)
#for row in cur.fetchall():
#    print row
cur.close()
conn1.commit()
cur = conn1.cursor()
cur.execute(query2)
for row in cur:
    print row

session.execute(
    User.__table__.insert(),
    [{'name': `randint(1, 100)`,'age': randint(1, 100)} for i in xrange(10000)]
)
session.commit()

''' PANDAS ''' 
sqldf = psql.read_sql(query1,conn1)
sqldf.index = sqldf['dept_no']
print sqldf
engine = create_engine(r'mysql+mysqldb://root:123@localhost/employees')
sqldf = psql.read_sql(query1,engine)
print sqldf
engine = create_engine(r'mysql+mysqldb://root:123@localhost/employees')
sqldf = psql.read_sql(query3,engine,chunksize = 10)
for i,idf in enumerate(sqldf):
    print i,idf
    if i == 3:
        break
    
engine = create_engine(r'mysql+mysqldb://root:123@localhost/employees')
df = pd.DataFrame(np.random.random(100).reshape(10,10),index = range(10),columns = range(10))
print df
psql.to_sql(df, 'test_table', engine)
engine = create_engine(r'mysql+mysqldb://root:123@localhost/employees')
df = pd.DataFrame({'dept_no':'d013','dept_name':'Cat'},index = range(1))
print df
df.to_sql('departments', engine, if_exists = 'append' ,index =False)

'''META DATA'''
engine = create_engine(r'mysql+mysqldb://root:123@localhost/employees')
metadata = MetaData(engine)
my_table = Table('cat',metadata,autoload=True)
my_table = Table('cat',metadata,
                 Column('age', Integer),
                 Column('name', String(40)),
                 Column('color', String(40))
)
my_table.create()
insert = my_table.insert()
insert.execute(age= 1,name= 'mimi', color = 'yellow')


'''ORM'''
Base = declarative_base()

class User(Base):
   
    __tablename__ = 'fuck'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))

engine = create_engine('mysql+mysqldb://root:123456@localhost:3306/test')
DBSession = sessionmaker(bind=engine)


 
