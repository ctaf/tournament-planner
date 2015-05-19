# Tournament Planner

The Tournament Planner is a Python module which keeps track of players participating
in Swiss system tournament and is a project of Udacity's full stack developer
nanodegree. It is based on a PostgreSQL database to store and retrieve the player
stats and the results of their matches.

## Quick Start

1. Clone this repo.
2. Get the Vagrantfile from the [fullstack-nanodegree-vm repository] (https://github.com/udacity/fullstack-nanodegree-vm).
3. Install and run a Vagrant VM with the Vagrantfile.
4. Configure the home directory of your VM to be able to run the Tournament Planner code.
5. Using psql create a database called `tournament`.
6. Create the tables and views by running `tournament.sql`.
7. Now everything is set up to import and use the code from `tournament.py`.

## Documentation

There is also some testing code included in `tournament_test.py` (also for the
extra features) which can be run to validate the installation and configuration
of the Tournament Planner.

A typical usage of the Tournament Planner might be as follows:
* Start a new tournament by re-initializing the database with `deleteMatches()`
  and `deletePlayers()`.
* Register new players with `registerPlayer()`.
* Retrieve the current player stats with `playerStandings()`.
* Record the results of every round with `reportMatch()`.
* Get the player pairings for the next round with `swissPairings()`.

## Creator

**Philip Taferner**

- [Google+] (https://plus.google.com/u/0/+PhilipTaferner/posts)
