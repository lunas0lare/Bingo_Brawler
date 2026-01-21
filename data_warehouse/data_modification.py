from psycopg2.extras import Json
def insert_to_staging(conn, cur, data, table) -> None:
    if table == 'leaderboard':
        sql = f"""
            INSERT INTO staging.{table} ("Index", "Team", "Wins", "Loses", "Scores", "Lines")
            VALUES (%(index)s, %(Team)s, %(W)s, %(L)s, %(S)s, %(Ln)s)
        """

    if table == 'player':
        sql = f"""
            INSERT INTO staging.{table} ("Name", "Link", "Team")
            VALUES (%(name)s, %(link)s, %(team)s)
        """

    if table == 'match':
        sql = f"""
            INSERT INTO staging.{table} ("date_played", "team")
            VALUES (%(started)s, %(teams)s)
        """
        for row in data:
            row['teams'] = Json(row['teams'])

    if table =='playoff':
        sql = f"""
            INSERT INTO staging.{table} ("date_played", "team")
            VALUES (%(date_played)s, %(teams)s)
        """
        #this convert teams into JSOn,
        # passing the team data as a json object instead of a list/dict directly into sql
        for row in data:
            row["teams"] = Json(row["teams"])
       
    cur.executemany(sql, data)
    conn.commit()

def flatten_match(conn, cur):
    with open("data_warehouse/sql/match_flatten.sql", 'r', encoding='utf-8') as f:
        cur.execute(f.read())
        conn.commit()
def flatten_playoff(conn, cur):
    with open("data_warehouse/sql/playoff_flatten.sql", 'r', encoding='utf-8') as f:
        cur.execute(f.read())
        conn.commit()
def flatten_all(conn, cur):
    flatten_playoff(conn, cur)
    flatten_match(conn, cur)