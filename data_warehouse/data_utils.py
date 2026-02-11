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
                "Date_played" TIMESTAMP PRIMARY KEY NOT NULL,
                "Team" JSONB NOT NULL
                );
        """
        ,f"""
                Create TABLE IF NOT EXISTS {schema}.Player(
                "Name" VARCHAR (20) UNIQUE NOT NULL,
                "Link" VARCHAR (200),
                "Team" VARCHAR (20),
                "Season" INT,
                CONSTRAINT player_name_link_UK UNIQUE ("Name", "Link")
                );
        """

        ,f"""
                Create TABLE IF NOT EXISTS {schema}.Playoff(
                "Date_played" TIMESTAMP PRIMARY KEY NOT NULL,
                "Team" JSONB NOT NULL
                );
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Season(
                "Season_id" INT PRIMARY KEY NOT NULL,
                "Mode" VARCHAR (10),
                "Link" VARCHAR (50)
                )
        """
    ]
    if schema == "core":
        ddls =[
        f"""
                CREATE TABLE IF NOT EXISTS {schema}.Player(
                "Player_id" VARCHAR(10) NOT NULL PRIMARY KEY,
                "Name" VARCHAR (20) UNIQUE NOT NULL,
                "Link" VARCHAR (200) 
                )
        """
        
        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Season(
                "Season_id" INT PRIMARY KEY NOT NULL,
                "Mode" VARCHAR (10),
                "Link" VARCHAR (50)
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Team(
                "Team_id" VARCHAR (10) PRIMARY KEY NOT NULL,
                "Team_name" VARCHAR (20) UNIQUE NOT NULL
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Match(
                "Match_id" VARCHAR (10) NOT NULL,
                "Season_id" INT NOT NULL references {schema}.season("Season_id"),
                "Date_played" TIMESTAMP UNIQUE NOT NULL,
                "Match_type" VARCHAR (10),
                constraint match_pk primary key("Match_id")
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Leaderboard_single(
                "Season_id" INT references {schema}.Season("Season_id"),
                "Player_id" VARCHAR (10) references {schema}.Player("Player_id"),
                "Wins" INT,
                "Loses" INT,
                "Scores" INT,
                "Lines" INT,
                constraint Season_single_pk primary key("Season_id", "Player_id")
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Leaderboard_team(
                "Season_id" INT references {schema}.Season("Season_id"), 
                "Team_id" VARCHAR (10) references {schema}.Team("Team_id"),
                "Wins" INT,
                "Loses" INT,
                "Scores" INT,
                "Lines" INT,
                constraint Season_team_pk primary key("Season_id", "Team_id")
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Match_participant_single(
                "Match_id" VARCHAR (10) references {schema}.Match("Match_id"),
                "Player_id" VARCHAR (10) references {schema}.Player("Player_id"),
                "Side" VARCHAR (10),
                "Result" VARCHAR (10),
                constraint match_participant_single_pk primary key("Match_id", "Player_id")
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Match_participant_team(
                "Match_id" VARCHAR (10) references {schema}.Match("Match_id"),
                "Team_id" VARCHAR (10) references {schema}.Team("Team_id"),
                "Side" VARCHAR (10),
                "Result" VARCHAR (10),
                constraint match_participant_team_pk primary key("Match_id", "Team_id")
                )
        """

        ,f"""
                CREATE TABLE IF NOT EXISTS {schema}.Team_member(
                "Season_id" INT NOT NULL references {schema}.Season("Season_id"),
                "Team_id" VARCHAR (10) NOT NULL references {schema}.Team("Team_id"),
                "Player_id" VARCHAR(10) NOT NULL references {schema}.Player("Player_id"),
                constraint member_pk primary key ("Season_id", "Team_id", "Player_id")
                )
        """
        ]
    
    for ddl in ddls:
        cur.execute(ddl)
    conn.commit()

    close_conn_cursor(conn, cur)

def create_staging_flat(conn, cur):
    with open("data_warehouse/sql/staging_flat.sql", 'r', encoding='utf-8') as f:
        try:
            cur.execute(f.read())
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"FAILED SQL: {e}")
            raise

def drop_schema(schema):
    try:
        sql =f"""
        DROP SCHEMA IF EXISTS {schema} CASCADE;"""
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"ERROR: Cannot drop schema {schema}: {e}")    