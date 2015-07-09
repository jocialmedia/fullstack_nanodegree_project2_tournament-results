#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tournament.py -- tournament simulator
# implementation of Elimination and Swiss-system
#

import os
import sys
import json
import math
import psycopg2
from random import shuffle
from random import randint


def clearScreen():
    """This function should work for linux and mac"""
    os.system('clear')


def connect():
    """Connect to the PostgreSQL database. Returns a database connection."""
    return psycopg2.connect("dbname=tournament user=vagrant")


def countPlayers():
    """Count number of player records in the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT COUNT(id) FROM players """)
    result = cursor.fetchall()
    DB.commit()
    DB.close()
    return result[0][0]


def registerPlayer(country, gender, firstname, familyname, birthday):
    """Register a player record with Country, gender, firstname, familyname and birthday."""
    DB = psycopg2.connect("dbname=tournament")
    cursor = DB.cursor()
    cursor.execute(""" INSERT INTO "players" (gender, firstname, familyname, birthday, country)
        VALUES (%s, %s ,%s ,%s, %s) RETURNING id""", [gender, firstname, familyname, birthday, str(country)])
    id_of_new_player = cursor.fetchall()
    DB.commit()
    DB.close()
    return id_of_new_player[0][0]


def deleteTournaments():
    """Remove all the tournament records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" DELETE FROM tournaments """, )
    DB.commit()
    DB.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" DELETE FROM matches """, )
    DB.commit()
    DB.close()


def deleteRounds():
    """Remove all the round records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" DELETE FROM rounds """, )
    DB.commit()
    DB.close()


def deletePlayers():
    """Delete all player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" DELETE FROM players """, )
    DB.commit()
    DB.close()


def resetDatabase():
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT
        (SELECT count(tournaments.id) FROM tournaments) AS number_of_tournaments_in_db,
        (SELECT count(rounds.id) FROM rounds) AS number_of_rounds_in_db,
        (SELECT count(matches.id) FROM matches) AS number_of_matches_in_db,
        (SELECT count(players.id) FROM players) AS number_of_players_in_db """)
    result = cursor.fetchall()
    clearScreen()
    print 75*"_"
    print "Numbers before the reset"
    print "Tournaments: " + str(result[0][0])
    print "Rounds: " + str(result[0][1])
    print "Matches: " + str(result[0][2])
    print "Players: " + str(result[0][3])
    print 75*"_"
    print "Deleting all tournaments and players"
    deleteTournaments()
    deleteMatches()
    deleteRounds()
    deletePlayers()
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT
        (SELECT count(tournaments.id) FROM tournaments) AS number_of_tournaments_in_db,
        (SELECT count(rounds.id) FROM rounds) AS number_of_rounds_in_db,
        (SELECT count(matches.id) FROM matches) AS number_of_matches_in_db,
        (SELECT count(players.id) FROM players) AS number_of_players_in_db """)
    result = cursor.fetchall()
    print 75*"_"
    print "Numbers after the reset"
    print "Tournaments: " + str(result[0][0])
    print "Rounds: " + str(result[0][1])
    print "Matches: " + str(result[0][2])
    print "Players: " + str(result[0][3])
    print 75*"_"
    print "\n"
    getMainMenu()


def getTournamentStatisticsMenu():
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT
        (SELECT count(tournaments.id) FROM tournaments) AS number_of_tournaments_in_db,
        (SELECT count(tournaments.id) FROM tournaments WHERE mode = 'Elimination') AS number_of_elimination_tournaments_in_db,
        (SELECT count(tournaments.id) FROM tournaments WHERE mode = 'Swiss') AS number_of_swiss_tournaments_in_db,
        (SELECT count(rounds.id) FROM rounds) AS number_of_rounds_in_db,
        (SELECT count(matches.id) FROM matches) AS number_of_matches_in_db,
        (SELECT count(players.id) FROM players) AS number_of_players_in_db """)
    result = cursor.fetchall()
    clearScreen()
    print "\n"
    print 75*"_"
    print "welcome to statistics menu"
    print 75*"_"
    print "Numbers from the database"
    print "Tournaments: " + str(result[0][0]) + " (Elimination Mode: " + str(result[0][1])+ ", Swiss Mode: " + str(result[0][2]) + ")"
    print "Rounds: " + str(result[0][3])
    print "Matches: " + str(result[0][4])
    print "Players: " + str(result[0][5])
    print 75*"_"

    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT t.id, t.name, t.mode, t.time_created,
        (SELECT COUNT(r.id) FROM rounds r WHERE r.tournament_id = t.id) AS round_count,
        (SELECT COUNT(m.id) FROM matches m LEFT JOIN rounds r ON r.id = m.round_id WHERE r.tournament_id = t.id) AS matches_count
        FROM tournaments t""")
    result = cursor.fetchall()
    print getTableField('Nr', 5) + getTableField('Name', 20) + getTableField('Mode', 12) + getTableField('Players', 7) + getTableField('Rounds', 7) + getTableField('Matches', 7) + getTableField('Date', 18)
    i = 0
    for item in result:
        i = i + 1
        if item[2] == "Elimination":
            number_of_players = item[5] + int(1);
        elif item[2] == "Swiss":
            number_of_players = 2 ** item[4];
        print getTableField(int(i), 5) + getTableField(item[1], 20) + getTableField(item[2], 12) + getTableField(number_of_players, 7) + getTableField(item[4], 7) + getTableField(item[5], 7) +  getTableField(item[3].strftime('%Y-%m-%d, %H:%M'), 18)

    getMainMenu()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT
        name,
        birthday,
        country,
        match_count1 + match_count2 AS match_count,
        winner_count
        FROM (
        SELECT
        p.firstname||' '||p.familyname AS name,
        birthday,
        country,
        (SELECT COUNT(m1.id) FROM matches m1 WHERE m1.player1_id = p.id) AS match_count1,
        (SELECT COUNT(m2.id) FROM matches m2 WHERE m2.player2_id = p.id) AS match_count2,
        (SELECT COUNT(m3.id) FROM matches m3 WHERE m3.winner_id = p.id) AS winner_count
        FROM players p
        ) AS q
    ORDER BY winner_count DESC, match_count
        """)
    result = cursor.fetchall()
    return result


def getPlayerStatisticsMenu():
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT
        (SELECT count(tournaments.id) FROM tournaments) AS number_of_tournaments_in_db,
        (SELECT count(tournaments.id) FROM tournaments WHERE mode = 'Elimination') AS number_of_elimination_tournaments_in_db,
        (SELECT count(tournaments.id) FROM tournaments WHERE mode = 'Swiss') AS number_of_swiss_tournaments_in_db,
        (SELECT count(rounds.id) FROM rounds) AS number_of_rounds_in_db,
        (SELECT count(matches.id) FROM matches) AS number_of_matches_in_db,
        (SELECT count(players.id) FROM players) AS number_of_players_in_db """)
    result = cursor.fetchall()
    clearScreen()
    print "\n"
    print 75*"_"
    print "welcome to statistics menu"
    print 75*"_"
    print "Numbers from the database"
    print "Tournaments: " + str(result[0][0]) + " (Elimination Mode: " + str(result[0][1])+ ", Swiss Mode: " + str(result[0][2]) + ")"
    print "Rounds: " + str(result[0][3])
    print "Matches: " + str(result[0][4])
    print "Players: " + str(result[0][5])
    print 75*"_"
    print "\n"

    playerstandingsdata = playerStandings()
    print 90*"_"
    print getTableField('Nr', 5) + getTableField('Name (Country)', 35) + getTableField('Birthdate', 20) + getTableField('Matches', 7) + getTableField('Wins', 7)
    print 90*"_"
    i = 0
    for item in playerstandingsdata:
        i = i + 1
        print getTableField(int(i), 5) + getTableField(str(item[0]) + " (" + str(item[2]) + ")", 35) + getTableField(item[1], 20) + getTableField(item[3], 7) + getTableField(item[4], 7) 

    getMainMenu()


def getInformationAboutPlayer(id):
  DB = connect()
  cursor = DB.cursor()
  cursor.execute(""" SELECT firstname FROM players WHERE id = %s""", [id])
  playerinfo = cursor.fetchall()
  DB.commit()
  DB.close()
  return playerinfo[0][0]


def getDetailInformationAboutPlayer(id):
  DB = connect()
  cursor = DB.cursor()
  cursor.execute(""" SELECT gender, firstname, familyname, birthday, country FROM players WHERE id = %s""", [id])
  playerinfo = cursor.fetchall()
  DB.commit()
  DB.close()
  return playerinfo[0][1] + " " + playerinfo[0][2] + " (" + playerinfo[0][4] + ")"


def eliminationPairings(tournament_id, tournament_players):
    """Running the tournament in elimination mode"""
    """Set round counter to 1"""
    number_of_rounds = 1
    """Save the record for round to the database"""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" INSERT INTO "rounds" (tournament_id) VALUES (%s) RETURNING id""", [int(tournament_id)])
    id_of_new_round = cursor.fetchone()[0]
    DB.commit()
    DB.close()

    """List players"""
    print "This are your " + str(len(tournament_players)) + " players in order of registration:"
    i = 0
    for player_id in tournament_players:
        i += 1
        print str(i) + ". " + str(getDetailInformationAboutPlayer(player_id))

    """Shuffleing array with players"""
    shuffle(tournament_players)

    print 75*"_"
    print "Round " + str(number_of_rounds)
    winner_array = []
    j = 0
    m = 1
    while (j < len(tournament_players)):
        player1_id = tournament_players[j]
        j += 1
        player2_id = tournament_players[j]
        j += 1

        """Get the winner of this pairing"""
        winner = randint(1,2)
        if winner == 1:
            winner_id = player1_id
        elif winner == 2:
            winner_id = player2_id

        """Print out match info"""
        print str(m) + ". " + str(getInformationAboutPlayer(player1_id)) + " vs " + str(getInformationAboutPlayer(player2_id)) + " | Winner: " + str(getDetailInformationAboutPlayer(winner_id))
        m += 1

        winner_array.append(winner_id)

        """Save the results of this round to the database"""
        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" INSERT INTO "matches" (round_id, player1_id, player2_id, winner_id) VALUES (%s, %s, %s, %s) RETURNING id""", [id_of_new_round, player1_id, player2_id, winner_id])
        result = cursor.fetchall()
        DB.commit()
        DB.close()


    n = len(winner_array)
    while n > 1:
        print 75*"_"
        winner_array = []
        number_of_rounds = number_of_rounds + 1

        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" SELECT id FROM "rounds" WHERE tournament_id = %s GROUP BY rounds.id""", [tournament_id])
        result_numbers = cursor.fetchall()
        DB.commit()
        DB.close()

        last_round = max(result_numbers)

        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" SELECT winner_id FROM "matches" WHERE matches.round_id = %s""", [last_round])
        result_winners = cursor.fetchall()
        DB.commit()
        DB.close()

        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" INSERT INTO "rounds" (tournament_id) VALUES (%s) RETURNING id""", [int(tournament_id)])
        id_of_new_round = cursor.fetchone()[0]
        DB.commit()
        DB.close()

        print "Round " + str(number_of_rounds)

        j = 0
        m = 1
        while (j < len(result_winners)):
            player1_id = result_winners[j]
            j += 1
            player2_id = result_winners[j]
            j += 1
   
            """Get the winner of this pairing"""
            winner = randint(1,2)
            if winner == 1:
                winner_id = player1_id
                looser_id = player2_id
            elif winner == 2:
                winner_id = player2_id
                looser_id = player1_id
            """Print out match info"""
            print str(m) + ". " + str(getInformationAboutPlayer(player1_id)) + " vs " + str(getInformationAboutPlayer(player2_id)) + " | Winner: " + str(getDetailInformationAboutPlayer(winner_id))
            m += 1

            winner_array.append(winner_id)
            n = len(winner_array)
            DB = connect()
            cursor = DB.cursor()
            cursor.execute(""" INSERT INTO "matches" (round_id, player1_id, player2_id, winner_id) VALUES (%s, %s, %s, %s) RETURNING id""", [id_of_new_round, player1_id, player2_id, winner_id])
            result = cursor.fetchall()
            DB.commit()
            DB.close()

    """Show final winner"""
    result = []
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT winner_id FROM matches WHERE round_id = %s""", [id_of_new_round])
    result = cursor.fetchall()
    DB.close()
    print "\n" + 75*"#"
    print "And the final winner is: " + str(getDetailInformationAboutPlayer(result[0][0]))
    print 75*"#" + "\n"



def getTableField(content, length):
    content = str(content)
    filling = (length-len(content))*" "
    return content + filling + " | "


def swissPairings(tournament_id, tournament_players):
    """get number of players"""
    number_of_players = len(tournament_players)
    """get final number of rounds"""
    total_number_of_rounds = int(math.log(number_of_players,2))
    """get final number of matches"""
    total_number_of_matches = total_number_of_rounds*(number_of_players/2)
    """Shuffling the array with players"""
    shuffle(tournament_players)
    print "This are your " + str(len(tournament_players)) + " players in order of registration:"
    i = 0
    for player_id in tournament_players:
        i += 1
        print str(i) + ". " + str(getDetailInformationAboutPlayer(player_id))


    """cleaning the workingtable working_for_swiss"""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" DELETE FROM "working_for_swiss" """, )
    DB.commit()
    DB.close()


    """saving players in table working_for_swiss"""
    i = 0
    for player_id in tournament_players:
        i += 1
        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" INSERT INTO "working_for_swiss" (tournament_id, player_id, points) VALUES (%s,%s,%s) RETURNING id""", [int(tournament_id), int(player_id), 0])
        DB.commit()
        DB.close()

    number_of_rounds = 0
    winner_array = []
    j = 0
    m = 1

    """Get other rounds of tournament until total number is reached"""
    while number_of_rounds < total_number_of_rounds:
        number_of_rounds += 1

        print "\n" + 75*"_"
        print "Round " + str(number_of_rounds)

        """registering new round in the table rounds"""
        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" INSERT INTO "rounds" (tournament_id) VALUES (%s) RETURNING id""", [int(tournament_id)])
        id_of_new_round = cursor.fetchone()[0]
        DB.commit()
        DB.close()

        """getting players from table working_for_swiss"""
        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" SELECT player_id,
            points,
            former_opponents
            FROM working_for_swiss
            WHERE tournament_id = %s
            ORDER BY points DESC """, [tournament_id])
        tournament_players = cursor.fetchall()
        DB.commit()
        DB.close()


        """Run matches for each player in the array"""
        winner_array = []
        j = 0
        m = 1
        while (j < len(tournament_players)):
            player1_id = tournament_players[j][0]
            player1_points = tournament_players[j][1]
            j += 1
            player2_id = tournament_players[j][0]
            player2_points = tournament_players[j][1]
            j += 1

            """Get winner of pairing"""
            winner = randint(1,2)
            if winner == 1:
                winner_id = player1_id
                winner_points = player1_points + 1
                looser_id = player2_id
            elif winner == 2:
                winner_id = player2_id
                winner_points = player2_points + 1
                looser_id = player1_id
            """Print out match info"""
            print str(m) + ". " + str(getInformationAboutPlayer(player1_id)) + " vs " + str(getInformationAboutPlayer(player2_id)) + " | Winner: " + str(getDetailInformationAboutPlayer(winner_id))
            m += 1


            DB = connect()
            cursor = DB.cursor()
            cursor.execute(""" UPDATE "working_for_swiss" SET points = %s, former_opponents = %s WHERE player_id = %s """, [int(winner_points), int(looser_id), int(winner_id)])
            DB.commit()
            DB.close()

            winner_array.append(winner_id)

            DB = connect()
            cursor = DB.cursor()
            cursor.execute(""" INSERT INTO "matches" (round_id, player1_id, player2_id, winner_id) VALUES (%s, %s, %s, %s) RETURNING id""", [id_of_new_round, player1_id, player2_id, winner_id])
            result = cursor.fetchall()
            DB.commit()
            DB.close()

        """getting players from table working_for_swiss"""
        DB = connect()
        cursor = DB.cursor()
        cursor.execute(""" SELECT player_id,
        points,
        former_opponents
        FROM working_for_swiss
        WHERE tournament_id = %s
        ORDER BY points DESC """, [tournament_id])
        tournament_players = cursor.fetchall()
        DB.commit()
        DB.close()

        """showing table with players and wins"""
        print 75*"_"
        print getTableField('Position', 10) + getTableField('Player', 35) + getTableField('Wins', 15)
        i = 0
        for row in tournament_players:
            i = i + 1
            print getTableField(int(i), 10) + getTableField(getDetailInformationAboutPlayer(row[0]), 35) + getTableField(row[1], 15)

    print "\n" + 75*"#"
    print "And the final winner is: " + str(getDetailInformationAboutPlayer(tournament_players[0][0]))
    print 75*"#" + "\n"


def checkIfPlayerNameAlreadyExists(random_firstname, random_familyname):
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT id FROM players WHERE firstname = %s AND familyname = %s""", [random_firstname, random_familyname])
    player_already_exists = cursor.fetchall()
    DB.commit()
    DB.close()
    if player_already_exists:
        return True
    else:
        return False


def createPlayer():
    """let the user decide the number of players for the tournament"""
    namesarray = json.loads(open("tournament_ressources.json").read())
    countryarray = ["Germany", "Russia", "United States", "France"]
    genderarray = ["female", "male"]
    random_country = countryarray[randint(0,3)]
    random_gender = str(genderarray[randint(0,1)])
    random_birthdaymonth = str(randint(1,12))
    random_birthdayday = str(randint(1,28))
    random_birthdayyear = str(randint(1960,2000))
    random_firstname = namesarray['data_for_names']['country'][random_country][random_gender+'_firstnames'][str(randint(0,9))]
    random_familyname = namesarray['data_for_names']['country'][random_country]['family_names'][str(randint(0,9))]

    """In case the player name already exists, create a new player name"""
    player_already_exists = checkIfPlayerNameAlreadyExists(random_firstname, random_familyname)
    if player_already_exists:
        random_familyname = namesarray['data_for_names']['country'][random_country]['family_names'][str(randint(0,9))]
        random_firstname = namesarray['data_for_names']['country'][random_country][random_gender+'_firstnames'][str(randint(0,9))]

    """Save information about new player in the database and return the id."""
    dataset = random_country, random_gender, random_familyname, random_firstname, random_birthdayyear + "-" + random_birthdaymonth + "-" + random_birthdayday
    id_of_new_player = registerPlayer(random_country, random_gender, random_firstname, random_familyname, random_birthdayyear + "-" + random_birthdaymonth + "-" + random_birthdayday)
    return id_of_new_player


def functionAskNumberOfPlayers():
    """let the user decide the number of players for the tournament"""
    number_of_players_for_tournament=raw_input("Please choose the number of players (4,8,16 or 32): ")
    if number_of_players_for_tournament =='4':
        return number_of_players_for_tournament
    elif number_of_players_for_tournament == '8':
        return number_of_players_for_tournament
    elif number_of_players_for_tournament == '16':
        return number_of_players_for_tournament
    elif number_of_players_for_tournament == '32':
        return number_of_players_for_tournament
    else:
        print "Nope. Please start again and choose 4,8,16 or 32."
        getTournament()


def getTournamentPlayers():
    """get number of players for tournament"""
    number_of_players_for_tournament = functionAskNumberOfPlayers()
    print "\nNumber of players for the new tournament: " + str(number_of_players_for_tournament)

    """save number of players to the database"""
    number_of_players_in_database = countPlayers()
    print "\nNumber of players registered in the database: " + str(number_of_players_in_database)

    """initiate array to collect playerdata"""
    array_of_players = []

    if number_of_players_in_database == 0:
        """If players database is empty or under 32, generate 32 players"""
        print "No players in database, so I create 32 random ones"
        i = 0
        while i <= 31:
            id_of_new_player = createPlayer()
            i += 1
            print "Created new player: " + str(getDetailInformationAboutPlayer(id_of_new_player))

    """Take random players from database"""
    print "Choosing random players from the database"
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(""" SELECT id FROM players LIMIT %s""", [str(number_of_players_for_tournament)])
    result = cursor.fetchall()

    k = 0
    while k < int(number_of_players_for_tournament):
        array_of_players.append(result[k][0])
        k = k + 1

    """Shuffling the array_of_players"""
    shuffle(array_of_players)

    """Returning the array_of_players"""
    return array_of_players


def getTournament():
    clearScreen()
    """Getting the name of the tournament"""
    tournament_name=raw_input("Please enter the name of the tournament: \n")    

    """Saving the name of the tournament to the database"""
    db = connect()
    cursor = db.cursor()
    cursor.execute(""" INSERT INTO "tournaments" (name) VALUES (%s) RETURNING id""", [str(tournament_name)])
    tournament_id = cursor.fetchone()[0]
    db.commit()
    print "Ok, the new tournament is called: " + tournament_name

    """Getting the tournament mode"""
    print "An now please choose from two tournament modes"
    print "1. Elimination Mode."
    print "2. Swiss Mode."
    selected_tournament_system=raw_input("Your choice: ")
    if selected_tournament_system =='1':
        print "Ok, you want Elimination mode."
        tournament_system = "Elimination"
    elif selected_tournament_system == '2':
        print "Ok, you want Swiss mode."
        tournament_system = "Swiss"
    else:
        print "Ok, seems like you could not decide so the automatic setting is Elimination mode." 
        tournament_system = "Elimination"

    """Saving the mode of the tournament to the database"""
    cursor = db.cursor()
    cursor.execute(""" UPDATE tournaments SET mode = %s WHERE id = %s""", [str(tournament_system),str(tournament_id)])
    db.commit()

    """Get the players for the tournament"""
    tournament_players = getTournamentPlayers()

    print "\n" + 75*"_"
    print "Welcome to your Tournament: " + str(tournament_name)
    if tournament_system == 'Elimination':
        print "Your tournament mode is: " + str(tournament_system)
        eliminationPairings(tournament_id, tournament_players)
    elif tournament_system == 'Swiss':
        print "Your tournament mode is: " + str(tournament_system)
        swissPairings(tournament_id, tournament_players)
    getMainMenu()


def showInfoAboutThisProject():
    clearScreen()
    print "This script simulates a tournament in elimination or swiss mode."
    print "The exercise is to develop a database schema to store the game"
    print "matches between players and write code to query this data and"
    print "determine the winners of various games."
    print ""
    print "This was done for Project 2 - Tournament Results"
    print "as part of the Full Stack Web Developer Nanodegree at Udacity.com"
    print "(https://www.udacity.com/course/nd004) June 2015"
    print ""
    print "Joachim Dethlefs (https://github.com/jocialmedia/fullstack_nanodegree_project2_tournament-results)"
    getMainMenu()


def exitTournamentSimulator():
    clearScreen()
    print "You want to exit. Ok, Bye."
    exit()


def getLogo():
    print "\n" + 75*"_"
    print "  _                                                    _   "
    print " | |                                                  | |  "
    print " | |_ ___  _   _ _ __ _ __   __ _ _ __ ___   ___ _ __ | |_ "
    print " | __/ _ \| | | | '__| '_ \ / _` | '_ ` _ \ / _ \ '_ \| __|"
    print " | || (_) | |_| | |  | | | | (_| | | | | | |  __/ | | | |_ "
    print "  \__\___/ \__,_|_|  |_| |_|\__,_|_| |_| |_|\___|_| |_|\__|"
    print "      _                 _       _                          "
    print "     (_)               | |     | |                         "
    print "  ___ _ _ __ ___  _   _| | __ _| |_ ___  _ __              "
    print " / __| | '_ ` _ \| | | | |/ _` | __/ _ \| '__|             "
    print " \__ \ | | | | | | |_| | | (_| | || (_) | |                "
    print " |___/_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|                "


def getMainMenu():
    print "\n" + 75*"_"
    print "What do you like to do?"
    print "1. Run a new tournament."
    print "2. Take a look at the statistics of tournaments."
    print "3. Take a look at the statistics of players."
    print "4. Install or reset the database."
    print "5. Show info about this project."
    print "6. Quit the simulator."
    print 75*"_"
    users_choice=raw_input("Please choose between option 1, 2, 3, 4, 5 and 6.\nYour choice: ")
    if users_choice =='1':
        getTournament()
    elif users_choice == '2':
        getTournamentStatisticsMenu()
    elif users_choice == '3':
        getPlayerStatisticsMenu()
    elif users_choice == '4':
        resetDatabase()
    elif users_choice == '5':
        showInfoAboutThisProject()
    elif users_choice == '6':
        exitTournamentSimulator()
    else:
        clearScreen()
        print "Unknown Option. Please start again and choose a number from 1 to 5."
        getMainMenu()

"""
getLogo()
getMainMenu()
"""