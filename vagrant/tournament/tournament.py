#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import itertools


def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error: Not able to connect to database.")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    # Query deletes from matches table
    query = "DELETE FROM matches"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    # Query deletes from players table
    query = "DELETE FROM players"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    # Query selects player id's from players table
    query = "SELECT id FROM players"
    cursor.execute(query)
    result = cursor.rowcount
    db.commit()
    db.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    # Serial is automaticallya assigned and query inserts name into table
    query = "INSERT INTO players (name) VALUES (%s)"
    cursor.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    # Query fetches all rows as a list of tuples
    query = "SELECT * FROM player_standings"
    cursor.execute(query)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    # reportMatch function assigns winner and loser
    query = "INSERT INTO matches(winner, loser) VALUES (%s, %s)"
    cursor.execute(query, (winner, loser))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, cursor = connect()
    # Fetches rows with id and name from player_standings view
    query = "SELECT id, name FROM player_standings"
    cursor.execute(query)
    result = cursor.fetchall()
    db.commit()
    # Combine every two tuples using iter tools library
    result = [
                aa + bb
                for (aa, bb)
                in itertools.izip(result[::2], result[1::2])
            ]
    # Inserts players into swiss_pairings table.
    # Players are automatically paired by win records due to player_standings
    for i in range(len(result)):
        player_1_id = result[i][0]
        player_1_name = result[i][1]
        player_2_id = result[i][2]
        player_2_name = result[i][3]
        query = """
                INSERT INTO swiss_pairings
                (player_1_id, player_1_name, player_2_id, player_2_name)
                VALUES (%s, %s, %s, %s)
                """
        cursor.execute(
                        query,
                        (
                            player_1_id,
                            player_1_name,
                            player_2_id,
                            player_2_name
                        )
                        )
        db.commit()
    db.close()
    return result
