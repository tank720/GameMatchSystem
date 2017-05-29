#!/usr/bin/python
# -*- coding: utf-8 -*-

from com.rwang.dao import GameDao

"""
start playing game
"""


def startGame(num_player):
    playerInfo = GameDao.selectPlayers(num_player)
    # print playerInfo
    # playerInfo = [[4, 200], [8, 1200], [10, 400], [16, 1400]]
    print "================================================================"
    print " The following players are going to play the game: "
    GameDao.showInfoAfterGame(playerInfo)
    resList = GameDao.showPlayerInfo(playerInfo)
    playerGroup = GameDao.gameMatching(playerInfo)
    GameDao.showGroupedPlayerInfo(playerGroup, resList)
    gameResults, groupRes = GameDao.genGameResults(playerGroup)
    GameDao.showGroupRes(groupRes)
    GameDao.upDatePerformance(gameResults)
    print "================================================================"
    print " The Info of the players after the game: "
    GameDao.showInfoAfterGame(playerInfo)


"""
start 1v1 game
"""


def start1v1Game(num_player):
    playerInfo = GameDao.selectPlayers(num_player)
    print "================================================================"
    print " The following players are going to play the 1v1 game: "
    GameDao.showInfoAfterGame(playerInfo)
    playerGroup = GameDao.gameMatch1v1(playerInfo)
    GameDao.showGroup1v1(playerGroup)
    gameResults = GameDao.genGame1v1Results(playerGroup)
    GameDao.show1v1GameRes(gameResults)
    GameDao.upDatePerformance(gameResults)
    print "================================================================"
    print " The Info of the players after the game: "
    GameDao.showInfoAfterGame(playerInfo)
    pass

"""
start 2v2 game
"""


def start2v2Game(num_player):
    playerInfo = GameDao.selectPlayers(num_player)
    print "================================================================"
    print " The following players are going to play the 2v2 game: "
    GameDao.showInfoAfterGame(playerInfo)
    playerGroup = GameDao.gameMatch2v2(playerInfo)
    GameDao.showGroup2v2(playerGroup)
    gameResults, groupRes = GameDao.genGame2v2Results(playerGroup)
    GameDao.show2v2GameRes(groupRes, playerGroup)
    GameDao.upDatePerformance(gameResults)
    print "================================================================"
    print " The Info of the players after the game: "
    GameDao.showInfoAfterGame(playerInfo)
    pass


"""
start 3v3 game
"""


def start3v3Game(num_player):
    playerInfo = GameDao.selectPlayers(num_player)
    print "================================================================"
    print " The following players are going to play the 3v3 game: "
    GameDao.showInfoAfterGame(playerInfo)
    playerGroup = GameDao.gameMatch3v3(playerInfo)
    GameDao.showGroup3v3(playerGroup)
    gameResults, groupRes = GameDao.genGame2v2Results(playerGroup)
    GameDao.show3v3GameRes(groupRes, playerGroup)
    GameDao.upDatePerformance(gameResults)
    print "================================================================"
    print " The Info of the players after the game: "
    GameDao.showInfoAfterGame(playerInfo)
    pass

"""
start 4v4 game
"""


def start4v4Game(num_player):
    playerInfo = GameDao.selectPlayers(num_player)
    print "================================================================"
    print " The following players are going to play the 4v4 game: "
    GameDao.showInfoAfterGame(playerInfo)
    playerGroup = GameDao.gameMatch4v4(playerInfo)
    GameDao.showGroup4v4(playerGroup)
    gameResults, groupRes = GameDao.genGame2v2Results(playerGroup)
    GameDao.show4v4GameRes(groupRes, playerGroup)
    GameDao.upDatePerformance(gameResults)
    print "================================================================"
    print " The Info of the players after the game: "
    GameDao.showInfoAfterGame(playerInfo)
    pass


