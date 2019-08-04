from tablescripts import tables
import psycopg2


insert_scr = (
        """
        INSERT INTO it_companies (number_of_emps, type_of_products, it_name)
        VALUES (%s, %s, %s) RETURNING id_it;
        """,
        """
        INSERT INTO pu (cores, price, id_it, pu_name)
        VALUES (%s, %s, %s, %s) RETURNING pu_id;
        """,
        """
        INSERT INTO buyer (b_name, pu_id)
        VALUES (%s, %s) RETURNING b_id;
        """)


def config():
    # get section, default to postgresql
    db = {
          'user': 'postgres',
          'password': '0000',
          'host': 'localhost'}
    return db


def create_tables():
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in tables:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_tuple(scr, elements):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(scr, elements)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_id(_id_, tab_id, tab, var, new_var):
    script = "UPDATE " + tab + " set " + var + " = '" + new_var + "' where " + tab_id + " = " + str(_id_) + ";"
    conn = None
    if _id_ and tab_id and tab and var and new_var:
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(script)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    else:
        print("error parameters")


def delete_id(tab, tab_id, _id):
    script = "Delete From " + tab + " where " + tab_id + ' = ' + str(_id) + ";"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(script)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def print_table():
    script = """
             select b_id, b_name, pu_name, cores, price, it_name, type_of_products, number_of_emps
                from  
                (select * from pu 
                            inner join buyer on buyer.pu_id = pu.pu_id) as t 
                                inner join it_companies on t.id_it = it_companies.id_it;
             """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # !!!!!!!!
        cur.execute(script)
        for tup in cur.fetchall():
            print(tup)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def find_company_pu(c, p):
    script = """
    select * from 
            ((select * from it_companies where it_name = %s) as a inner join 
            (select * from pu where pu_name = %s) as b on a.id_it = b.id_it)
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # !!!!!!!!
        cur.execute(script, (c, p))
        for tup in cur.fetchall():
            print(tup)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def fulll_find_text(st):
    script = """
    SELECT pu_id, it_name, cores, price, ts_headline(pu_name, q, 'StartSel=<___!Found--->, StopSel=<---Found!___>')
    FROM pu inner join it_companies on pu.id_it = it_companies.id_it,
    plainto_tsquery(%s) AS q
    WHERE tsvector(pu_name) @@ q;
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # !!!!!!!!
        cur.execute(script, [st])
        for tup in cur.fetchall():
            print(tup)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def destroy_all():
    script = """
    drop table if exists it_companies cascade;
    drop table if exists pu cascade;
    drop table if exists buyer cascade;
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # !!!!!!!!
        cur.execute(script)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
