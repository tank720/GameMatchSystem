#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import string
import random
import sys
import MySQLdb as mdb
from com.rwang.db import DBUtil
from com.rwang.model import Player
from com.rwang.dao import PlayerDao
from com.rwang.dao import GameDao

"""
add player
"""


def add(player):
    flag = PlayerDao.addPlayer(player)
    if flag == 1:
        player_id = PlayerDao.queryIdByEmail(getattr(player, '__player_email'))
        GameDao.addPerformance(player_id)
        print "Add player successfully !!!"
    else:
        print "Add player failure !!!"
    pass

"""
randomly insert players to the database
"""


def randomAddPlayer(num_player):
    player = Player.Player()
    for i in range(num_player):
        player_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        player_email = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + "@" \
                       + ''.join(random.sample(string.ascii_letters + string.digits, 3)) + ".com"
        setattr(player, '__player_name', player_name)
        setattr(player, '__player_email', player_email)
        setattr(player, '__is_online', 1)
        add(player)
    pass


"""
delete player
"""


def delete(player_id):
    flag = PlayerDao.delPlayer(player_id)
    if flag == 1:
        GameDao.delPerformance(player_id)
        print "Delete player successfully !!!"
    else:
        print "Delete player failure !!!"
    pass


"""
get player using player_id
"""


def get(player_id):
    res = PlayerDao.get(player_id)
    return res
    pass


"""
edit player
"""


def edit(new_player, player_id):
    PlayerDao.updatePlayer(new_player, player_id)
    pass


"""
query player information
"""


def query():
    res = PlayerDao.queryAll()
    return res
    pass

"""
query the complete information of all players
"""


def queryComplete():
    res = GameDao.queryCompleteInfo()
    return res
    pass

"""
search player information
"""


def search(player_name, player_email):
    res = PlayerDao.query(player_name, player_email)
    return res







