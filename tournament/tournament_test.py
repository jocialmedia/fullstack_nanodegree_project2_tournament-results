#!/usr/bin/env python
#
# Test cases for tournament.py

import sys
from tournament_for_testing import *

def testConnectToDatabase():
    conn = connect()
    if conn.cursor():
        return {'name':'Connection to database works!', 'success':1}   
    else:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        #sys.exit("Database connection failed!\n ->%s" % (exceptionValue))
        return {'name':'Connection to database does not work!', 'success':0}


def testDeleteMatches():
    deleteMatches()
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(""" SELECT COUNT(id) FROM matches """)
    result = cursor.fetchone()
    cursor.close()
    if result[0] == 0:
        return {'name':'Match records can be deleted!', 'success':1}
    elif result[0] != 0:
        return {'name':'Matches records can not be deleted', 'success':0}


def testRegister():
    deletePlayers()
    registerPlayer("United States", "m", "Steve", "Wozniak", "1950-08-11")
    c = countPlayers()
    if c == 1:
        return {'name':'After registering a player, countPlayers() returns 1!', 'success':1}
    elif c != 1:
        return {'name':'After registering a player, countPlayers() does not return 1!', 'success':0}


def testDeletePlayers():
    deletePlayers()
    registerPlayer("United States", "m", "Steve", "Wozniak", "1950-08-11")
    deletePlayers()
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(""" SELECT COUNT(id) FROM players """)
    result = cursor.fetchone()
    cursor.close()
    if result[0] == 0:
        return {'name':'Players records can be deleted!', 'success':1}
    elif result[0] != 0:
        return {'name':'Players records can not be deleted!', 'success':0}


def testCountPlayers():
    deletePlayers()
    registerPlayer("United States", "m", "Steve", "Wozniak", "1950-08-11")
    deletePlayers()
    c = countPlayers()
    if str(c) == '0':
        return {'name':'After deleting, countPlayers() returns zero.', 'success':1}
    elif str(c) != 0:
        return {'name':'After deleting, countPlayers() does not return zero.', 'success':0}
 

def testRegisterCountDelete():
    deletePlayers()
    registerPlayer("Poland", "w", "Marie", "Curie", "1867-11-07")
    registerPlayer("Great Britain", "w", "Joan", "Clarke", "1917-06-24")
    registerPlayer("United States", "m", "Steve", "Wozniak", "1950-08-11")
    registerPlayer("India", "m", "Mahatma", "Gandhi", "1869-10-02")
    c = countPlayers()
    deletePlayers()
    d = countPlayers()
    if c == 4 and d == 0:
        return {'name':'After registering four players, countPlayers returns 4!', 'success':1}
    elif c != 4 and d != 0:
        return {'name':'After registering four players, countPlayers does not return 4!', 'success':0}


def testStandingsBeforeMatches():
    """
    Test not used because of the differences in systems structure
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."
    """


def testReportMatches():
    """
    Test not used because of the differences in systems structure
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    """


def testPairings():
    """
    Test not used because of the differences in systems structure
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."
    """

def runTests():
    testresults = []
    testresults.append(testConnectToDatabase())
    testresults.append(testDeleteMatches())
    testresults.append(testDeletePlayers())
    testresults.append(testCountPlayers())
    testresults.append(testRegister())
    testresults.append(testRegisterCountDelete())
    countSuccessfullTests = 0
    print "\n" + 75*"#"
    print "Test cases for tournament.py - Project 2 of Udacity Nanodegree 2015"
    print 75*"#" + "\n"
    for testresult in testresults:
        print "- " + str(testresult['name'])
        countSuccessfullTests = countSuccessfullTests + testresult['success']
    print 75*"_"
    print "Number of tests: " + str(len(testresults))
    print "Number of successful tests: " + str(countSuccessfullTests)
    if len(testresults) == countSuccessfullTests:
        print "Success! All tests pass!"
    elif len(testresults) != countSuccessfullTests:
        print "Unfortunately not all tests passed!"
    print "\n" + 75*"#"

runTests()