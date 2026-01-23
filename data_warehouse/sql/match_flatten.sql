truncate staging.match_flatten;

insert into staging.match_flatten("Date_played", "Team", "Side", "Result")
select
 m."Date_played" as Date_played,
 t->> 'name' as Team,
 t->> 'side' as Side,
 t->> 'result' as Result
from staging.match as m, jsonb_array_elements(m."Team") as t;
