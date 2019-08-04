tables = (
    """
    CREATE TABLE IF NOT EXISTS it_companies
    (
        id_it serial PRIMARY KEY,
        number_of_emps integer,
        type_of_products character varying(30),
        it_name character varying(30)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS pu
    (
        pu_id SERIAL PRIMARY KEY,
        cores integer,
        price integer,
        pu_name character varying(30),
        id_it integer,
        FOREIGN KEY(id_it)
            REFERENCES it_companies(id_it)
                ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS buyer
    (
        b_name character varying(30),
        pu_id integer,
        b_id SERIAL PRIMARY KEY,
        FOREIGN KEY(pu_id)
            REFERENCES pu(pu_id)
                ON UPDATE CASCADE ON DELETE CASCADE
    )
    """
)
