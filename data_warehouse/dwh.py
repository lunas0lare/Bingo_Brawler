from data_utils import *
from data_modification import *
from data_loading import *
from data_transformation import flatten_match, flatten_playoff
conn, cur = get_conn_cursor()

Bingo_data = dict()

tables = list()


def staging_table():
    schema = "staging"

    conn, cur = None, None

    conn, cur = get_conn_cursor()

    create_schema(schema)
    create_table(schema)

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
            for row in rows:
                insert_into_core(conn, cur, row, 'team')
            for row in rows:
                insert_into_core(conn, cur, row, 'team_member')
        elif table == 'season':
            for row in rows:
                insert_into_core(conn, cur, row, 'season')
        elif table == 'match_flatten':
            for row in rows:
                insert_into_core(conn, cur, row, 'match')

    insert_into_core(conn, cur, None, 'leaderboard')           
    insert_into_core(conn, cur, None, 'match_participant')
        


# season = int(input("your season: "))

Bingo_data = load_data(5)
drop_schema('staging')
drop_schema('core') 
staging_table()
core_table()
drop_schema('staging')
Bingo_data = load_data(4)
staging_table()
core_table()