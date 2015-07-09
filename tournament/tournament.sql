-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	gender VARCHAR (255) NOT NULL,
	firstname VARCHAR (255) NOT NULL,
	familyname VARCHAR (255) NOT NULL,
	birthday date,
	country VARCHAR (255) NOT NULL,
	time_created timestamp default current_timestamp
	);

CREATE TABLE tournaments (
	id SERIAL PRIMARY KEY, 
	name varchar(250),
	mode varchar(50),
	time_created timestamp default current_timestamp
	);

CREATE TABLE rounds (
	id SERIAL PRIMARY KEY, 
	tournament_id integer NOT NULL,
	time_created timestamp default current_timestamp
	);

CREATE TABLE matches (
	id SERIAL NOT NULL, 
	round_id integer NOT NULL, 
	player1_id integer NOT NULL, 
	player2_id integer NOT NULL, 
	winner_id integer NOT NULL, 
	time_created timestamp default current_timestamp
	);

CREATE TABLE working_for_swiss (
	id SERIAL NOT NULL, 
	tournament_id integer NOT NULL, 
	player_id integer NOT NULL, 
	points integer NOT NULL, 
	former_opponents varchar(250),
	time_created timestamp default current_timestamp
	);