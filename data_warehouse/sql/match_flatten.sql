truncate staging.match_flat;

insert into staging.match_flat("Date", "Team", "Side", "Result")
select
 m."date_played",
 t->> 'name' as Team,
 t->> 'side' as Side,
 t->> 'result' as Result
from staging.match as m, jsonb_array_elements(m.team) as t;
