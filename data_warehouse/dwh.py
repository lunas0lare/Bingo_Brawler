from data_utils import get_conn_cursor, close_conn_cursor, create_table, create_schema, create_staging_flat
from data_modification import *
from data_loading import *
from data_transformation import flatten_match, flatten_playoff
conn, cur = get_conn_cursor()

Bingo_data = dict()
Bingo_data = load_data(5)

def staging_table():
    schema = "staging"

    conn, cur = None, None

    conn, cur = get_conn_cursor()

    create_schema(schema)
    create_table(schema)

    for key, value in Bingo_data.items():
        insert_to_staging(conn, cur, value, key)

    create_staging_flat(conn, cur)
    flatten_match(conn, cur)
    flatten_playoff(conn, cur)

    close_conn_cursor(conn, cur)

def core_table():
    schema = 'core'

    conn, cur = None, None

    conn, cur = get_conn_cursor()

    create_schema(schema)
    create_table(schema)

    for table in Bingo_data:
        cur.execute(f"SELECT * FROM staging.{table};")
        rows = cur.fetchall()

        if table == 'player':
            for row in rows:
                insert_into_core(conn, cur, row, 'player')

core_table()