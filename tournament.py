#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def doQuery(sql, *xargs):
    """Perform a sql query against the database and handle the connection.

    Args:
        sql: a sql statement.
        xargs: further arguments to select statements provided as tuple.
    Returns:
        A list of tuples containing the query results if any, else None.
    """

    conn = connect()
    cur = conn.cursor()

    if xargs:
        cur.execute(sql, xargs)
    else:
        cur.execute(sql)

    if sql.startswith("SELECT"):
        res = cur.fetchall()
    else:
        res = None

    conn.commit()
    conn.close()

    return res


def deleteMatches():
    """Remove all the match records from the database."""

    doQuery("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""

    doQuery("DELETE FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""

    count = doQuery("SELECT COUNT(name) FROM players;")[0][0]
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    doQuery("INSERT INTO players VALUES (%s)", name)


def applyOMW(standings):
    """Use OMW to rank players with equal scores.

    Args:
        standings: the player standings returned by playerStandings.
    Returns:
        The newly ordered standings.
    """

    standings_omw = []
    flip_done = False

    # Look for players with equal scores.
    # If there are any, rank them by OMW.
    for ind, (i, n, w, m) in enumerate(standings):

        # The last player is just added to the new list,
        # no more flipping necessary.
        if ind + 1 == len(standings):
            standings_omw.append(standings[ind])

        else:
            this_player = standings[ind]
            next_player = standings[ind+1]
            former_player = standings[ind-1]
            next_w, next_m = next_player[2:]

            # If next player has the same scores, check the OMWs.
            if flip_done:
                standings_omw.append(former_player)
                flip_done = False
            else:
                next_omw = next_w if not next_m else float(next_w)/next_m
                this_omw = w if not m else float(w)/m

                # If next player has a higher OMW, flip the positions,
                # but don't flip again in the next iteration.
                if next_omw > this_omw:
                    standings_omw.append(next_player)
                    flip_done = True
                else:
                    standings_omw.append(this_player)

    return standings_omw


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Players with equal scores are further ranked by OMW.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    before_omw = doQuery("SELECT * FROM standings;")
    after_omw = applyOMW(before_omw)

    # A single reorder cycle might not be enough, so
    # iteratively apply OMW until the ranking is stable.

    while before_omw != after_omw:
        before_omw = after_omw
        after_omw = applyOMW(after_omw)

    return after_omw


def reportMatch(winner, loser, tie=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tie: if True, record a tie in the database
    """

    # Check if there has been a match between the two players before.
    # If so, no record will be generated.

    former_matches = doQuery("SELECT * FROM matches WHERE p1 = %(w)s AND \
                            p2 = %(l)s OR p2 = %(w)s AND p1 = %(l)s;" %
                            {'w': winner, 'l': loser})
    if former_matches:
        return

    # In case of a tie, write NULL to the database.
    # The proper type casting from Python to SQL is handled by psycopg2.

    if tie:
        doQuery("INSERT INTO matches VALUES (%s, %s, %s);", winner, loser, None)
    else:
        doQuery("INSERT INTO matches VALUES (%s, %s, %s);", winner, loser, winner)


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

    standings = playerStandings()
    playerlist = []

    while standings:
        stats1, stats2 = standings.pop(), standings.pop()
        playerlist.append((stats1[0], stats1[1], stats2[0], stats2[1]))

    return playerlist

