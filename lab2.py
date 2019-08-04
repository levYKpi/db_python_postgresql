from sqlalchemy import *
from sqlalchemy.sql import select
from sqlalchemy.orm import relationship
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2


# metadata = MetaData()
# it_companies = Table('it_companies', metadata,
#                      Column('id_it', Integer, primary_key=True),
#                      Column('emps', Integer),
#                      Column('type_of_products', String),
#                      Column('it_name', String)
#                      )
#
# pu = Table('pu', metadata,
# #relationship("it_companies", cascade="delete"),
#            Column('pu_id', Integer, primary_key=True),
#            Column('cores', Integer),
#            Column('price', Integer),
#            Column('id_it', Integer, ForeignKey('it_companies.id_it')),
#            Column('it_name', String)
#            )
#
# buyer = Table('buyer', metadata,
#               Column('b_id', Integer, primary_key=True),
#               Column('pu_id', Integer, ForeignKey('pu.pu_id')),
#               Column('b_name', String),
#               #relationship("buyer", cascade="delete")
#               )
#
# engine = create_engine("sqlite://")
# metadata.create_all(engine)
#
# ins = it_companies.insert().values(id_it = 1, it_name = "amd", type_of_products = "pu", emps = 1000)
# conn = engine.connect()
# rt = conn.execute(ins)
# s = select([it_companies])
# result = conn.execute(s)
# for _ in result:
#     print(_)
Base = declarative_base()


class Itcompanies(Base):
    __tablename__ = 'it_companies'
    id_it = Column(Integer, primary_key=True)
    it_name = Column(String)
    emps = Column(Integer)
    type_of_product = Column(String)
    pu = relationship("Pu", back_populates='itb', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<it_companies(%s, %s, %s, %s)>" % \
               (self.id_it, self.it_name, self.emps, self.type_of_product)


class Pu(Base):
    __tablename__ = 'pu'
    pu_id = Column(Integer, primary_key=True)
    pu_name = Column(String)
    cores = Column(Integer)
    price = Column(Integer)
    id_it = Column(Integer, ForeignKey("it_companies.id_it"))
    itb = relationship("Itcompanies", back_populates="pu")
    buyer = relationship("Buyer", back_populates='pub', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<pu(%s, %s, %s, %s, %s)>" % (
            self.pu_id, self.pu_name, self.cores, self.price, self.id_it
        )


class Buyer(Base):
    __tablename__ = 'buyer'
    b_id = Column(Integer, primary_key=True)
    b_name = Column(String)
    pu_id = Column(Integer, ForeignKey("pu.pu_id"))
    pub = relationship("Pu", back_populates="buyer")

    def __repr__(self):
        return "<buyer(%s, %s, %s)>" % \
               (self.b_id, self.b_name, self.pu_id)


class Database:
    # engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:5432@localhost/DB')
    __engine = sqlalchemy.create_engine('postgresql://postgres:@localhost:5432/')
    _Session = sessionmaker(bind=__engine)

    def __init__(self):
        __engine = sqlalchemy.create_engine('postgresql://postgres:@localhost:5432/')
        _Session = sessionmaker(bind=__engine)
        Base.metadata.create_all(__engine)
        self.session = _Session()

    def get_its(self):
        rows = []
        # if not self.session.query(Itcompanies).filter(sqlalchemy.false()):
        for _p in self.session.query(Itcompanies).order_by(Itcompanies.id_it):
            rows.append(_p)
            self.session.commit()
        self.session.commit()
        return rows

    def get_pus(self):
        rows = []
        for _p in self.session.query(Pu).order_by(Pu.pu_id):
            rows.append(_p)
            self.session.commit()
        self.session.commit()
        return rows

    def get_buy(self):
        rows = []
        for _p in self.session.query(Buyer).order_by(Buyer.b_id):
            rows.append(_p)
            self.session.commit()
        self.session.commit()
        return rows

    def get_it_id(self, _id):
        t = None
        if self.session.query(exists().where(Itcompanies.id_it == _id)).scalar():
            t = self.session.query(Itcompanies).get(_id)
        self.session.commit()
        return t

    def get_pu_id(self, _id):
        t = self.session.query(Pu).get(_id)
        self.session.commit()
        return t

    def get_b_id(self, _id):
        t = self.session.query(Buyer).get(_id)
        self.session.commit()
        return t

    def insert_it(self, _it):
        self.session.add(_it)
        self.session.commit()

    def insert_pu(self, pu):
        self.session.add(pu)
        self.session.commit()

    def insert_b(self, _b):
        self.session.add(_b)
        self.session.commit()

    def update_it_id(self, item, _id):
        _it = self.get_it_id(_id)
        _it.it_name = str(item)
        self.session.flush()
        self.session.commit()

    def update_pu_id(self, item, _id):
        _it = self.get_pu_id(_id)
        _it.pu_name = str(item)
        self.session.flush()
        self.session.commit()

    def update_b_id(self, item, _id):
        _it = self.get_b_id(_id)
        _it.b_name = str(item)
        self.session.flush()
        self.session.commit()

    def delete_it(self, _id):
        t = self.get_it_id(_id)
        if t:
            self.session.delete(t)
        self.session.commit()

    def delete_pu(self, _id):
        self.session.delete(self.get_pu_id(_id))
        self.session.commit()

    def delete_b(self, _id):
        self.session.delete(self.get_b_id(_id))
        self.session.commit()

    def search(self, _txt):
        script = """
        SELECT pu_id, it_name, cores, price, ts_headline(pu_name, q, 'StartSel=<___!Found--->, StopSel=<---Found!___>')
    FROM pu inner join it_companies on pu.id_it = it_companies.id_it,
    plainto_tsquery(%s) AS q
    WHERE tsvector(pu_name) @@ q;
                    """
        return self.__engine.execute(script, (_txt,)).fetchall()

    def find_atts(self, a, b):
        script = """
        select * from 
            ((select * from it_companies where it_name = %s) as a inner join 
            (select * from pu where pu_name = %s) as b on a.id_it = b.id_it)
                    """
        return self.__engine.execute(script, (a, b)).fetchall()

    def select_all(self):
        return self.__engine.execute(
            """
            select b_id, b_name, pu_name, cores, price, it_name, type_of_product, emps
                from  
                (select * from pu 
                            inner join buyer on buyer.pu_id = pu.pu_id) as t 
                                inner join it_companies on t.id_it = it_companies.id_it;
            """
        ).fetchall()

    def dropall(self):
        self.__engine.execute(
            """
            drop table if exists it_companies cascade;
            drop table if exists pu cascade;
            drop table if exists buyer cascade;
            """
        )

    def trigger_fun(self):
        script = """
        create or replace function up_price() returns trigger as $$
        Begin
        if new.price > 100 then
        update pu set price = price / 1.05 where price < new.price;
        end if;
        return new; 
        end;
        $$
        language 'plpgsql';
        create trigger trig after insert on pu for each row EXECUTE PROCEDURE up_price();
        """
        self.__engine.execute(script)
        self.session.commit()


def menu(d):
    _it_id = 0
    _pu_id = 0
    _b_id = 0
    ran = 0
    while 0 == int(input("to continue press '0' or any num to exit: ")):
        it = int(input("""
        to insert it - 1:
                  pu - 2:
               buyer - 3:
          update it - 11:
                 pu - 12:
                  b - 13:
          delete it - 21:
                 pu - 22:
              buyer - 23:
        add random - 100:
         find atts - 200:
          find fts - 300:
             print - 400:
          ------------->:  """))
        if it == 1:
            _it_id += 1
            d.insert_it(Itcompanies(id_it=_it_id, it_name=input("name: "), emps=int(input("emps: ")),
                                    type_of_product=input("type_of_products: ")))
        elif it == 2:
            _pu_id += 1
            d.insert_pu(Pu(pu_id=_pu_id, pu_name=input("name: "), cores=int(input("cores: ")),
                           price=int(input("price: ")), id_it=int(input("it: "))))
        elif it == 3:
            _b_id += 1
            d.insert_b(Buyer(b_id=_b_id, b_name=input("name: "), pu_id=int(input("pu: "))))
        elif it == 11:
            d.update_it_id(input("new it name: "), int(input("id: ")))
        elif it == 12:
            d.update_pu_id(input("new it name: "), int(input("id: ")))
        elif it == 13:
            d.update_b_id(input("new it name: "), int(input("id: ")))
        elif it == 21:
            d.delete_it(int(input("id: ")))
        elif it == 22:
            d.delete_pu(int(input("id: ")))
        elif it == 21:
            d.delete_b(int(input("id: ")))
        elif it == 100:
            ran += 1
            _it_id += 1
            _pu_id += 1
            _b_id += 1
            d.insert_it(Itcompanies(id_it=_it_id, it_name="it"+str(ran), emps=ran,
                                    type_of_product=str(ran)))
            d.insert_pu(Pu(pu_id=_pu_id, pu_name=str("namepu"), cores=ran,
                           price=ran*100, id_it=_it_id))
            d.insert_b(Buyer(b_id=_b_id, b_name='b_name'+str(ran), pu_id=_pu_id))
        elif it == 200:
            for _ in d.find_atts(input("it_name: "), input("pu_name: ")):
                d.session.commit()
                print(_)
            d.session.commit()
        elif it == 300:
            for _ in d.search(input("pu full name: ")):
                d.session.commit()
                print(_)
            d.session.commit()
        elif it == 400:
            for _ in d.select_all():
                d.session.commit()
                print(_)
            d.session.commit()
            print()
            for _ in d.get_its():
                print(_)
            print()
            for _ in d.get_pus():
                print(_)
            print()
            for _ in d.get_buy():
                print(_)
        d.session.commit()


if __name__ == '__main__':
    d = Database()
    d.trigger_fun()
    menu(d)
    # it = Itcompanies(id_it=1, it_name='it', emps=25, type_of_product="pus")
    # d.insert_it(it)
    # it = Itcompanies(id_it=2, it_name='it2', emps=52, type_of_product="sup")
    # d.insert_it(it)
    # p = Pu(pu_id=1, pu_name='x1', cores=10, price=50, id_it=1)
    # d.insert_pu(p)
    # b = Buyer(b_id=1, b_name='b1', pu_id=1)
    # d.insert_b(b)
    # b = Buyer(b_id=2, b_name='b2', pu_id=1)
    # d.insert_b(b)
    # print(d.select_all())
    # print(d.get_its())
    # d.trigger_fun()
    # d.insert_pu(Pu(pu_id=2, pu_name='x22', cores=10, price=300, id_it=1))
    # d.insert_b(Buyer(b_id=3, b_name='b3', pu_id=2))
    # d.insert_pu(Pu(pu_id=3, pu_name='x32', cores=20, price=400, id_it=1))
    # d.insert_b(Buyer(b_id=4, b_name='b4', pu_id=3))
    # d.update_it_id("mytel", 1)
    # print(d.select_all())
    # d.delete_it(1)
    # d.delete_it(2)
    # d.get_it_id(4)
    # print(d.get_its())
    d.dropall()
