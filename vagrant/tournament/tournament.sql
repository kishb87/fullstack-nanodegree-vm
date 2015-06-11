-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;


CREATE TABLE players (
	id serial PRIMARY KEY,
	name text UNIQUE NOT NULL
);

CREATE TABLE matches (
	id serial PRIMARY KEY,
	winner int REFERENCES players (id),
	loser int REFERENCES players (id)
);
-- View created by joining players and matches table
CREATE VIEW player_standings AS
SELECT 
    p.id,
    p.name,
    COUNT(m1.winner) AS wins,
    COUNT(m1.winner) + COUNT(m2.loser) AS matches
FROM players AS p
LEFT JOIN matches AS m1
    ON p.id = m1.winner
LEFT JOIN matches AS m2
    ON p.id = m2.loser
GROUP BY p.id, p.name
ORDER BY
    wins DESC;

 CREATE TABLE swiss_pairings (
 	player_1_id int REFERENCES players(id),
 	player_1_name text REFERENCES players(name),
 	player_2_id int REFERENCES players(id),
 	player_2_name text REFERENCES players(name)
);





	