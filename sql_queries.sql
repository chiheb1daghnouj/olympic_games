-- 1) How many olympics games have been held?
select count(distinct ("Games")) as total_olympic_games
from athlete_events;

-- 2) List down all Olympics games held so far.
select distinct on ( "Games") "Year", "Season", "City"
from athlete_events
order by "Games", "Year";

-- 3) Mention the total no of nations who participated in each olympics game?
with cte
         as (select a."Games", nr.region
             from athlete_events a
                      join noc_regions nr on a."NOC" = nr."NOC"
             group by "Games", region)
select cte."Games", count(1)
from cte
group by cte."Games"
order by "Games";

-- 4) Which year saw the highest and lowest no of countries participating in olympics
with all_countries
         as (select a."Games", nr.region
             from athlete_events a
                      join noc_regions nr on a."NOC" = nr."NOC"
             group by "Games", region),
     total_countries as
         (select "Games", count(1) as totale_countries
          from all_countries
          group by "Games")
select distinct concat(first_value("Games") over (order by totale_countries asc), ' - ',
                       first_value(totale_countries) over (order by totale_countries asc))  as lowest_countries,
                concat(first_value("Games") over (order by totale_countries desc), ' - ',
                       first_value(totale_countries) over (order by totale_countries desc)) as highest_countries
from total_countries;

-- 5) Which nation has participated in all of the olympic games
with tot_games as
         (select count(distinct ("Games")) as total_games
          from athlete_events),
     countries as
         (select distinct "Games", nr.region as country
          from athlete_events a
                   join noc_regions nr on a."NOC" = nr."NOC"),
     total_countries as
         (select countries.country, count(1) as tot_participations
          from countries
          group by countries.country)
select t.country, t.tot_participations
from total_countries t
         join tot_games g on (t.tot_participations = g.total_games)
order by country;