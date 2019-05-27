import time
from sqlalchemy import (Table, Column, Integer, Boolean,
    String, MetaData, ForeignKey, create_engine, select)


meta = MetaData()

user = Table('user', meta,
             Column('id', Integer, primary_key=True),
             Column('foo', Integer),
             Column('name', String))

engine = create_engine('sqlite:///:memory:')
meta.create_all(engine)

con = engine.connect()

for i in range(100):
    con.execute(user.insert().values([i, i, str(i)]))

for i in range(100):
    t0 = time.time()
    for k in range(100):
        [x[0] for x in con.execute(select([user]).where(user.c.foo==0))]
    print time.time() - t0
