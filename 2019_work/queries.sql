select f.id, t.name, home_score, t2.name, away_score from fixture f
join team t on f.home_team_id=t.id
join team t2 on f.away_team_id=t2.id
where gameweek_id=13


select f.gameweek_id, points  from player_fixture pf
join player p on p.id = pf.player_id
join fixture f on f.id = pf.fixture_id
where p.second_name='Deulofeu'
order by f.gameweek_id desc

select * from player where second_name like '%ort%'

-- top average score
select p.first_Name, p.second_name, t.id, t.pavg, p.cost, t.pavg*10/p.cost as value, t2.mins, p.position_id from 
(select p.id, avg(cast(points as float)) as pavg  from player_fixture pf
	join player p on p.id = pf.player_id
	join fixture f on f.id=pf.fixture_id
	where f.gameweek_id > 18
	group by p.id) t
join 
(select p.id, sum(minutes_played) as mins  from player_fixture pf
	join player p on p.id = pf.player_id
	join fixture f on f.id=pf.fixture_id
	where f.gameweek_id > 18
	group by p.id)
t2 on t2.id=t.id
join player p  on t.id=p.id
where mins>360 --and position_id = 3
order by pavg desc


-- overall average
select avg(cast(points as float)) as pavg  from player_fixture pf

-- filter by home/away
select avg(cast(points as float)) as pavg from player_fixture pf
	group by was_home

-- filter by position	
select p.position_id, avg(cast(points as float)) as pavg from player_fixture pf
join player p on p.id = pf.player_id
	group by p.position_id
