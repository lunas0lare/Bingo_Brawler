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
    cur.executemany(sql, data)
    conn.commit()

