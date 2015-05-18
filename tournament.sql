-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players 
	(
		name varchar(50),
		id SERIAL,
		PRIMARY KEY (id)
	);

CREATE TABLE matches
	(
		p1 integer 
			REFERENCES players(id),
		p2 integer 
			REFERENCES players(id),
		winner integer 
			REFERENCES players(id)
	);

CREATE VIEW match_nr AS
    SELECT 
		name,
		count(p1) AS mnr
	FROM 
		players
	LEFT JOIN
		matches
	ON 
		id = p1 OR 
		id = p2
	GROUP BY
		name
	;

CREATE VIEW win_nr AS
    SELECT 
		name,
		count(winner) AS wins
	FROM 
		players
	LEFT JOIN
		matches
	ON
		id = winner
	GROUP BY
		name
	ORDER BY
		wins DESC
	;

CREATE VIEW standings AS
    SELECT 
		id,
		players.name,
		wins,
		mnr
	FROM 
		players, match_nr, win_nr
	WHERE 
		win_nr.name = players.name AND
		match_nr.name = players.name
	ORDER BY
		wins DESC
	;
