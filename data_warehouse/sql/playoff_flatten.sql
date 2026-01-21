truncate staging.match_flat;

insert into staging.playoff_flat("Date_played", "Team", "Side", "Scores", "Wins", "Loses")
select 
p."date_played",
t->>'Team' as Team,
t->>'side' as Side,
(t->>'S')::int as Scores,
(t->>'W')::int as Wins,
(t->>'L')::int as Loses
from staging.playoff as p, jsonb_array_elements(p.team) as t;