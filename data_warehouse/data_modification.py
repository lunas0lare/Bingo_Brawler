from psycopg2.extras import Json
def insert_to_staging(conn, cur, data, table) -> None:
    if table == 'season':
        sql = f"""
            INSERT INTO staging.{table} ("Season_id", "Mode", "Link")
            VALUES (%(season_id)s, %(type)s, %(base_url)s)
            ON CONFLICT ("Season_id") DO NOTHING;
        """
    if table == 'leaderboard':
        sql = f"""
            INSERT INTO staging.{table} ("Index", "Team", "Wins", "Loses", "Scores", "Lines")
            VALUES (%(index)s, %(Team)s, %(W)s, %(L)s, %(S)s, %(Ln)s)
            ON CONFLICT ("Index") DO NOTHING;
        """

    if table == 'player':
        sql = f"""
            INSERT INTO staging.{table} ("Name", "Link", "Team")
            VALUES (%(name)s, %(link)s, %(team)s)
            ON CONFLICT ("Name") DO NOTHING;
        """

    if table == 'match':
        sql = f"""
            INSERT INTO staging.{table} ("Date_played", "Team")
            VALUES (%(started)s, %(teams)s)
            ON CONFLICT ("Date_played") DO NOTHING;
        """
        for row in data:
            row['teams'] = Json(row['teams'])

    if table =='playoff':
        sql = f"""
            INSERT INTO staging.{table} ("Date_played", "Team")
            VALUES (%(date_played)s, %(teams)s)
            ON CONFLICT ("Date_played") DO NOTHING;
        """
        #this convert teams into JSOn,
        # passing the team data as a json object instead of a list/dict directly into sql
        for row in data:
            row["teams"] = Json(row["teams"])
       
    cur.executemany(sql, data)
    conn.commit()

def insert_into_core(conn, cur, data, table: str) -> None:
    if table.lower() == "player":
        sql = f"""
            CREATE SEQUENCE IF NOT EXISTS core.{table}_seq start 1;

            ALTER TABLE core.{table}
            ALTER COLUMN "Player_id" SET DEFAULT (
            'P' || LPAD(nextval('core.{table}_seq')::text, 3, '0'));

            INSERT INTO core.{table} ("Name", "Link") 
            VALUES (%(Name)s, %(Link)s)
            ON CONFLICT ("Name") DO NOTHING;
        """
    elif table.lower() == "team":
        sql = f"""
            CREATE SEQUENCE IF NOT EXISTS core.{table}_seq start 1;

            ALTER TABLE core.{table}
            ALTER COLUMN "Team_id" SET DEFAULT(
            'T' || LPAD(nextval('core.{table}_seq')::text, 3, '0'));

            INSERT INTO core.{table} ("Team_name") 
            VALUES (%(Team)s)
            ON CONFLICT ("Team_name") DO NOTHING;
        """
    elif table.lower() == "match":
        sql = f"""
            CREATE SEQUENCE IF NOT EXISTS core.{table}_seq start 1;

            ALTER TABLE core.{table}
            ALTER COLUMN "Match_id" SET DEFAULT(
            'M' || LPAD(nextval('core.{table}_seq')::text, 3, '0'));

            INSERT INTO core.{table} ("Season_id", "Date_played", "Match_type") 
            SELECT 
                s."Season_id",
                %(Date_played)s::timestamp,
                s."Mode"
            FROM 
                core.season as s
            WHERE 
                s."Season_id" = "Season_id";
            
        """
    elif table.lower() == "season":
        sql = f"""
            INSERT INTO core.{table} ("Season_id", "Mode", "Link") 
            VALUES (%(Season_id)s, %(Mode)s, %(Link)s)
            ON CONFLICT DO NOTHING;
        """
    elif table.lower() == "match_participant":
        sql = f"""
            INSERT INTO core.{table} ("Match_id", "Participant_id", "Participant_type", "Result", "Side") 
            VALUES (%(Match_id)s, %(Participant_id)s, %(Participant_type)s, %(Result)s, %(Side)s)
        """
    elif table.lower() == "leaderboard":
        sql = f"""
            INSERT INTO core.{table} ("Season_id", "Participant_id", "Participant_type", "Wins", "Loses", "Scores", "Lines") 
            VALUES (%(Season_id)s, %(Participant_id)s, %(Participant_type)s, %(Wins)s, %(Loses)s, %(Scores)s, %(Lines)s)
            ON CONFLICT "Season_id" DO NOTHING;
        """
    elif table.lower() == "team_member":
        sql = f"""
            INSERT INTO core.{table} ("Season_id", "Team_id", "Player_id") 
            VALUES (%(Season_id)s, %(Team_id)s, %(Player_id)s)
        """
    else:
        raise ValueError(f"Unknown table: {table}")
    cur.execute(sql, data)
    conn.commit()