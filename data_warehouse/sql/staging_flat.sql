create table if not exists staging.match_flatten(
"Date_played" timestamp not null,
"Team" Varchar(20),
"Side" varchar(5),
"Result" Varchar(10)
);

create table if not exists staging.playoff_flatten(
"Date_played" timestamp not null,
"Team" varchar(20),
"Side" varchar(5),
"Wins" int,
"Loses" int,
"Scores" int
);