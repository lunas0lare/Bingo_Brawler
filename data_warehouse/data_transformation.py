def flatten_match(conn, cur):
    with open("data_warehouse/sql/match_flatten.sql", 'r', encoding='utf-8') as f:
        cur.execute(f.read())
        conn.commit()
        
def flatten_playoff(conn, cur):
    with open("data_warehouse/sql/playoff_flatten.sql", 'r', encoding='utf-8') as f:
        cur.execute(f.read())
        conn.commit()
