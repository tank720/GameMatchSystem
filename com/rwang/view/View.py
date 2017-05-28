#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import MySQLdb as mdb
from com.rwang.db import DBUtil
from com.rwang.model import Player
from com.rwang.action import PlayerAction
from com.rwang.action import GameAction
from com.rwang.dao import PlayerDao


CONTEXT = "Welcome to Game Matching System !!! \n" \
        + "The following is the main menu of the system: \n" \
        + "[MAIN/M]: Main Menu \n" \
        + "[QUERY/Q]: Query the information of all players \n" \
        + "[COMPLETE/C]: Query the complete information of all players \n" \
        + "[GET/G]: Get the information of one specific player \n" \
        + "[ADD/A]: Add player \n" \
        + "[RANDOMADD/R]: Randomly Add player \n" \
        + "[UPDATE/U]: Update player \n" \
        + "[DELETE/D]: Delete player \n" \
        + "[SEARCH/S]: Search the information of players according to his name or email \n" \
        + "[PLAY/P]: Start Playing Game" \
        + "[P1]: Start Playing 1v1 Game" \
        + "[P2]: Start Playing 2v2 Game" \
        + "[P3]: Start Playing 3v3 Game" \
        + "[P4]: Start Playing 4v4 Game" \
        + "[EXIT/E]: Exit the system \n"


OPERATION_MAIN = "MAIN"
OPERATION_QUERY = "QUERY"
OPERATION_EXIT = "EXIT"
OPERATION_ADD = "ADD"
OPERATION_RANDOMADD = "RANDOMADD"
OPERATION_DELETE = "DELETE"
OPERATION_UPDATE = "UPDATE"
OPERATION_GET = "GET"
# OPERATION_BREAK = "BREAK"
OPERATION_SEARCH = "SEARCH"
OPERATION_COMPLETE = "COMPLETE"
OPERATION_PlAY = "PLAY"
OPERATION_ONE = "P1"
OPERATION_TWO = "P2"
OPERATION_THREE = "P3"
OPERATION_FOUR = "P4"

print CONTEXT
step = 0
# previous = ""

player = Player.Player()

while 1:
    # print "previous: " + previous
    # print "step: " + str(step)

    command = raw_input("Please input command: ")

    # print "command: " + command

    if OPERATION_EXIT == command.upper() or OPERATION_EXIT[0] == command.upper():
        print "The system is exited !!!"
        break
    elif OPERATION_QUERY == command.upper() or OPERATION_QUERY[0] == command.upper():
        print "You are querying the information of all players !!!"
        # previous = OPERATION_QUERY
        res = PlayerAction.query()
        for i in range(len(res)):
            row = res[i]
            print " player_id: " + str(row[0]) + \
                  " player_name: " + row[1] + \
                  " player_email: " + row[2] + "\n"
    elif OPERATION_ADD == command.upper() or OPERATION_ADD[0] == command.upper():
        print "You are adding a new player !!!"
        # previous = OPERATION_ADD
        step += 1
        while 1 <= step <= 3:
            # print "step: " + str(step)
            if 1 == step:
                player_name = raw_input(" Please input the name of the player: ")
                step += 1
            elif 2 == step:
                setattr(player, '__player_name', player_name)
                player_email = raw_input(" Please input the email of the player: ")
                step += 1
            elif 3 == step:
                setattr(player, '__player_email', player_email)
                setattr(player, '__is_online', 1)
                PlayerAction.add(player)
                step = 0

    elif OPERATION_DELETE == command.upper() or OPERATION_DELETE[0] == command.upper():
        print "You are deleting a player according to his id !!!"
        # previous = OPERATION_DELETE
        player_id = raw_input(" Please input the id of the player: ")
        answer = raw_input(" Are you sure you want to permanently delete this player [Y/N] ? ")
        if answer == "Y":
            PlayerAction.delete(player_id)

    elif OPERATION_UPDATE == command.upper() or OPERATION_UPDATE[0] == command.upper():
        print "You are editing a player according to his id !!!"
        # previous = OPERATION_ADD
        step += 1
        while 1 <= step <= 4:
            # print "step: " + str(step)
            if 1 == step:
                player_id = raw_input(" Please input the id of the player: ")
                step += 1
            elif 2 == step:
                player_name = raw_input(" Please input the name of the player: ")
                step += 1
            elif 3 == step:
                setattr(player, '__player_name', player_name)
                player_email = raw_input(" Please input the email of the player: ")
                step += 1
            elif 4 == step:
                setattr(player, '__player_email', player_email)
                setattr(player, '__is_online', 1)
                PlayerAction.edit(player, player_id)
                print "Edit player successfully !!!"
                step = 0

    elif OPERATION_GET == command.upper() or OPERATION_GET[0] == command.upper():
        print "You are query the information of one player according to his id !!!"
        player_id = raw_input(" Please input the id of the player: ")
        row = PlayerAction.get(player_id)
        if len(row) == 0:
            print "There is no player with player_id = " + player_id + " !!! "
            continue
        print " player_id: " + str(row[0]) + \
              " player_name: " + row[1] + \
              " player_email: " + row[2] + "\n"

    elif OPERATION_SEARCH == command.upper() or OPERATION_SEARCH[0] == command.upper():
        print "You are search the information of players according to his name and email !!!"
        step += 1
        while 1 <= step <= 2:
            if 1 == step:
                player_name = raw_input(" Please input the name of the player: ")
                step += 1
            elif 2 == step:
                player_email = raw_input(" Please input the name of the player: ")
                res = PlayerAction.search(player_name, player_email)
                for i in range(len(res)):
                    row = res[i]
                    print " player_id: " + str(row[0]) + \
                          " player_name: " + row[1] + \
                          " player_email: " + row[2] + "\n"
                step = 0
    elif OPERATION_COMPLETE == command.upper() or OPERATION_COMPLETE[0] == command.upper():
        print "You are querying the complete information of all players !!!"
        # previous = OPERATION_QUERY
        res = PlayerAction.queryComplete()
        for i in range(len(res)):
            row = res[i]
            print " player_id: " + str(row[0]) + \
                  " player_name: " + row[1] + \
                  " player_email: " + row[2] + \
                  " num_win: " + str(row[3]) + \
                  " num_lose: " + str(row[4]) + \
                  " score: " + str(row[5]) + \
                  " league: " + row[6] + "\n"
    elif OPERATION_PlAY == command.upper() or OPERATION_PlAY[0] == command.upper():
        print "You are selecting players to play the game !!!"
        numberOfPlayer = raw_input(" Please input the number of the players (must be an even number): ")
        upBound = len(PlayerDao.queryOnline())
        if int(numberOfPlayer) > upBound:
            print " The number of players playing game exceeds the total number of online players !!!"
            continue
        # print numberOfPlayer
        GameAction.startGame(int(numberOfPlayer))
    elif OPERATION_ONE == command.upper():
        print "You are selecting players to play the 1v1 game !!!"
        numberOfPlayer = raw_input(" Please input the number of the players (must be an even number): ")
        upBound = len(PlayerDao.queryOnline())
        if int(numberOfPlayer) % 2 != 0:
            print "The input number is not a multiple of 2 !!!"
            continue
        if int(numberOfPlayer) > upBound:
            print " The number of players playing game exceeds the total number of online players !!!"
            continue
        # print numberOfPlayer
        GameAction.start1v1Game(int(numberOfPlayer))
    elif OPERATION_TWO == command.upper():
        print "You are selecting players to play the 2v2 game !!!"
        numberOfPlayer = raw_input(" Please input the number of the players (must be a multiple of 4): ")
        upBound = len(PlayerDao.queryOnline())
        if int(numberOfPlayer) % 4 != 0:
            print "The input number is not a multiple of 4 !!!"
            continue
        if int(numberOfPlayer) > upBound:
            print " The number of players playing game exceeds the total number of online players !!!"
            continue
        # print numberOfPlayer
        GameAction.start2v2Game(int(numberOfPlayer))
    elif OPERATION_THREE == command.upper():
        pass
    elif OPERATION_FOUR == command.upper():
        pass
    elif OPERATION_RANDOMADD == command.upper() or OPERATION_RANDOMADD[0] == command.upper():
        print "You are randomly add players to the databases !!!"
        num_players = raw_input(" Please enter the number of players you want to add: ")
        PlayerAction.randomAddPlayer(int(num_players))
        print " Randomly Add Players Successfully !!!"
    else:
        print "Your input command " + str(command) + " is not valid , please input again !!! "
        print CONTEXT






