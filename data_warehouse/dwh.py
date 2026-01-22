from data_utils import get_conn_cursor, close_conn_cursor, create_table, create_schema, create_staging_flat
from data_modification import *
from data_loading import *
from data_transformation import flatten_match, flatten_playoff
conn, cur = get_conn_cursor()

Bingo_data = dict()
season_list = dict()
tables = list()

Bingo_data = load_data(5)
season_list = load_season_list()

def staging_table():
    schema = "staging"

    conn, cur = None, None

    conn, cur = get_conn_cursor()

    create_schema(schema)
    create_table(schema)

    for key, value in season_list.items():
        insert_to_staging(conn, cur, value, key)

    for key, value in Bingo_data.items():
        tables.append(key)
        insert_to_staging(conn, cur, value, key)

    create_staging_flat(conn, cur)
    flatten_match(conn, cur)
    flatten_playoff(conn, cur)
    tables.append('match_flatten')
    tables.append('playoff_flatten')

    close_conn_cursor(conn, cur)

def core_table():
    schema = 'core'

    conn, cur = None, None

    conn, cur = get_conn_cursor()

    create_schema(schema)
    create_table(schema)

    for table in tables:
        cur.execute(f"SELECT * FROM staging.{table};")
        rows = cur.fetchall()

        if table == 'player':
            for row in rows:
                insert_into_core(conn, cur, row, 'player')
                insert_into_core(conn, cur, row, 'team')
        elif table == 'match_flatten':
            for row in rows:
                insert_into_core(conn, cur, row, 'match')
        elif table == 'season':
            for row in rows:
                insert_into_core(conn, cur, row, 'season')

staging_table()
core_table()