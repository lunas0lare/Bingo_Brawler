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

def insert_into_core(conn, cur, data, table) -> None:
    if table == "player":
        sql = f"""
            CREATE SEQUENCE IF NOT EXISTS core.{table}_seq start 1;

            ALTER TABLE core.{table}
            ALTER COLUMN "Player_id" SET DEFAULT (
            'P' || LPAD(nextval('core.{table}_seq')::text, 3, '0'));

            INSERT INTO core.{table} ("Name", "Link") 
            VALUES (%(Name)s, %(Link)s)
        """
    elif table == "Team":
        sql = f"""
            CREATE SEQUENCE IF NOT EXISTS core.Team_seq start 1;

            ALTER TABKE core."Team"
            ALTER COLUMN "Team.Team_id" SET DEFAULT(
            'T' || LPAD(nextval('core.Team_seq')), 3, '0');

            INSERT INTO core.{table} ("Team_name") 
            VALUES (%(Team_name)s)
        """
    elif table == "Match":
        sql = f"""
            CREATE SEQUENCE IF NOT EXISTS core.Match_seq start 1;

            ALTER TABKE core."Match"
            ALTER COLUMN "Match.Match_id" SET DEFAULT(
            'M' || LPAD(nextval('core.Match_seq')), 3, '0');

            INSERT INTO core.{table} ("Season_id", "Date_played", "Match_type") 
            VALUES (%(Season_id)s, %(Date_played)s, %(Match_type)s)
        """
    elif table == "Season":
        sql = f"""
            INSERT INTO core.{table} ("Season_id", "Mode") 
            VALUES (%(Season_id)s, %(Mode)s)
        """
    elif table == "Match_participant":
        sql = f"""
            INSERT INTO core.{table} ("Match_id", "Participant_id", "Participant_type", "Result", "Side") 
            VALUES (%(Match_id)s, %(Participant_id)s, %(Participant_type)s, %(Result)s, %(Side)s)
        """
    elif table == "Leaderboard":
        sql = f"""
            INSERT INTO core.{table} ("Season_id", "Participant_id", "Participant_type", "Wins", "Loses", "Scores", "Lines") 
            VALUES (%(Season_id)s, %(Participant_id)s, %(Participant_type)s, %(Wins)s, %(Loses)s, %(Scores)s, %(Lines)s)
        """
    elif table == "Team_member":
        sql = f"""
            INSERT INTO core.{table} ("Season_id", "Team_id", "Player_id") 
            VALUES (%(Season_id)s, %(Team_id)s, %(Player_id)s)
        """
    else:
        raise ValueError(f"Unknown table: {table}")
    cur.execute(sql, data)
    conn.commit()