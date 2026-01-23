truncate staging.playoff_flatten;

insert into staging.playoff_flatten("Date_played", "Team", "Side", "Scores", "Wins", "Loses")
select 
p."Date_played" as Date_played,
t->>'Team' as Team,
t->>'side' as Side,
(t->>'S')::int as Scores,
(t->>'W')::int as Wins,
(t->>'L')::int as Loses
from staging.playoff as p, jsonb_array_elements(p."Team") as t;