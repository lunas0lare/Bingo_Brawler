import psycopg2
from psycopg2.extras import RealDictCursor
import os
host = "localhost"
database = "postgres"
port = 5432
user = "lunamoon"
password = ""

def get_conn_cursor():
    conn = psycopg2.connect(
        host = host,
        port = port,
        database = database,
        user = user,
        password = password
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)

    return conn, cur

conn, cur = get_conn_cursor()

def close_conn_cursor(conn, cur):
    conn.close()
    cur.close()

def create_schema(schema):
    conn, cur = get_conn_cursor()

    schema =f"CREATE SCHEMA IF NOT EXISTS {schema};"

    cur.execute(schema)

    conn.commit()

    close_conn_cursor(conn, cur)
    
def create_table(schema):
    """
    creating tables for staging layer and core layer.
    Total of 4 tables for staging and 7 for core.
    Args:
        schema (_type_): _description_
    """

    conn, cur = get_conn_cursor()
    
    if schema =='staging':
        ddls = [
        f"""
                Create TABLE IF NOT EXISTS {schema}.Leaderboard(
                "Index" INT PRIMARY KEY NOT NULL,
                "Team" VARCHAR (20),
                "Wins" INT,
                "Loses" INT,
                "Scores" INT,
                "Lines" INT
                );
        """

        ,f"""
                Create TABLE IF NOT EXISTS {schema}.Match(
                "date_played" TIMESTAMP NOT NULL,
                "team" JSONB NOT NULL
                );
        """
        ,f"""
                Create TABLE IF NOT EXISTS {schema}.Player(
                "Name" VARCHAR (20) NOT NULL,
                "Link" VARCHAR (200),
                "Team" VARCHAR (20)
                );
        """

        ,f"""
                Create TABLE IF NOT EXISTS {schema}.Playoff(
                "date_played" TIMESTAMP NOT NULL,
                "team" JSONB NOT NULL
                );
        """
    ]
    if schema == "core":
        ddls =[
        f"""
                CREATE TABLE IF NOT EXISTS {schema}.Player(
                "Player_id" VARCHAR(5) NOT NULL,
                "Name" VARCHAR (20),
                "Link" VARCHAR (200)
                )
        """
        
        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Season(
                "Season_id" INT NOT NULL,
                "Mode" VARCHAR (10)
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Team(
                "Team_id" VARCHAR (5) NOT NULL,
                "Team_name" VARCHAR (20)
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Match(
                "Match_id" VARCHAR (5) NOT NULL,
                "Season_id" INT,
                "Date_played" TIMESTAMP,
                "Match_type" VARCHAR (10)
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Leaderboard(
                "Season_id" INT,
                "Participant_id" VARCHAR (5),
                "Participant_Type" VARCHAR (10),
                "Wins" INT,
                "Loses" INT,
                "Scores" INT,
                "Lines" INT
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Match_participant(
                "Match_id" VARCHAR (5) NOT NULL,
                "side" VARCHAR (10),
                "Participant_id" VARCHAR (5),
                "Participant_Type" VARCHAR (10),
                "Result" VARCHAR (5)
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Team_member(
                "Season_id" INT,
                "Team_id" VARCHAR (5),
                "Player_id" VARCHAR(5),
                PRIMARY KEY (Season_id, Team_id, Player_id)
                )
        """
        ]
    
    for ddl in ddls:
        cur.execute(ddl)
    conn.commit()

    close_conn_cursor(conn, cur)

def create_staging_flat(conn, cur):
    with open("data_warehouse/sql/staging_flat.sql", 'r', encoding='utf-8') as f:
        cur.execute(f.read())
        conn.commit()