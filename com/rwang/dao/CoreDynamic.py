#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy
import MySQLdb as mdb
import random
import collections
from com.rwang.db import DBUtil
from com.rwang.dao import PlayerDao
from com.rwang.dao import GameDao

conn = DBUtil.getConnection()
with conn:

    class Solution(object):

        def __init__(self):
            # initialize the deque for each league
            self.Bronze1v1Deque = collections.deque()
            self.Silver1v1Deque = collections.deque()
            self.Gold1v1Deque = collections.deque()
            self.Platinum1v1Deque = collections.deque()
            self.Diamond1v1Deque = collections.deque()
            self.Master1v1Deque = collections.deque()
            self.GrandMaster1v1Deque = collections.deque()
            # assign number to each league
            self.BronzeLeague = 1
            self.SilverLeague = 2
            self.GoldLeague = 3
            self.PlatinumLeague = 4
            self.DiamondLeague = 5
            self.MasterLeague = 6
            self.GrandMasterLeague = 7
            # set the max size of each deque
            self.Bronze1v1DequeSize = 10
            self.Silver1v1DequeSize = 10
            self.Gold1v1DequeSize = 10
            self.Platinum1v1DequeSize = 10
            self.Diamond1v1DequeSize = 10
            self.Master1v1DequeSize = 10
            self.GrandMaster1v1DequeSize = 10
            # set the max waiting time of each deque
            self.Bronze1v1WaitTime = 10
            self.Silver1v1WaitTime = 10
            self.Gold1v1WaitTime = 10
            self.Platinum1v1WaitTime = 10
            self.Diamond1v1WaitTime = 10
            self.Master1v1WaitTime = 10
            self.GrandMaster1v1WaitTime = 10
            # initialize the dictionary to indicate each player whether he is in or not in the deque
            self.isIn1v1Bronzedeque = {}
            self.isIn1v1Silverdeque = {}
            self.isIn1v1Golddeque = {}
            self.isIn1v1Platinumdeque = {}
            self.isIn1v1Diamonddeque = {}
            self.isIn1v1Masterdeque = {}
            self.isIn1v1GrandMasterdeque = {}
            # gaming pool
            self.gamingPool1v1 = {}
            # Mode : 2v2
            # initialize the deque for each league
            self.Bronze2v2Deque = collections.deque()
            self.Silver2v2Deque = collections.deque()
            self.Gold2v2Deque = collections.deque()
            self.Platinum2v2Deque = collections.deque()
            self.Diamond2v2Deque = collections.deque()
            self.Master2v2Deque = collections.deque()
            self.GrandMaster2v2Deque = collections.deque()
            # set the max size of each deque
            self.Bronze2v2DequeSize = 16
            self.Silver2v2DequeSize = 16
            self.Gold2v2DequeSize = 16
            self.Platinum2v2DequeSize = 16
            self.Diamond2v2DequeSize = 16
            self.Master2v2DequeSize = 16
            self.GrandMaster2v2DequeSize = 16
            # set the max waiting time of each deque
            self.Bronze2v2WaitTime = 10
            self.Silver2v2WaitTime = 10
            self.Gold2v2WaitTime = 10
            self.Platinum2v2WaitTime = 10
            self.Diamond2v2WaitTime = 10
            self.Master2v2WaitTime = 10
            self.GrandMaster2v2WaitTime = 10
            # initialize the dictionary to indicate each player whether he is in or not in the deque
            self.isIn2v2Bronzedeque = {}
            self.isIn2v2Silverdeque = {}
            self.isIn2v2Golddeque = {}
            self.isIn2v2Platinumdeque = {}
            self.isIn2v2Diamonddeque = {}
            self.isIn2v2Masterdeque = {}
            self.isIn2v2GrandMasterdeque = {}
            # gaming pool
            self.gamingPool2v2 = {}

        def genPlayerId(self):
            cursor = conn.cursor()
            sql = "SELECT count(*) FROM player"
            cursor.execute(sql)
            rows = cursor.fetchone()
            cursor.close()
            totalNumPlayer = rows[0]
            randomnumplayer = numpy.random.poisson(totalNumPlayer / 10, 1)
            chooseplayer = random.sample(range(totalNumPlayer), int(randomnumplayer))
            # print "chooseplayer: " + str(chooseplayer)
            isIn1v1deque = dict(self.isIn1v1Bronzedeque.items() +
                                self.isIn1v1Silverdeque.items() +
                                self.isIn1v1Golddeque.items() +
                                self.isIn1v1Platinumdeque.items() +
                                self.isIn1v1Diamonddeque.items() +
                                self.isIn1v1Masterdeque.items() +
                                self.isIn1v1GrandMasterdeque.items())
            isIn1v1Game = self.playerListInGame(self.gamingPool1v1)
            cursor = conn.cursor()
            sql = " SELECT id FROM player ORDER BY id "
            cursor.execute(sql)
            ind = 0
            resList = []
            # print "randomnumplayer: " + str(randomnumplayer)
            i = 0
            while i in range(randomnumplayer):
                rows = cursor.fetchone()
                # print "rows" + str(rows)
                if rows[0] == 50:
                    break
                if (rows[0] in isIn1v1deque) or (rows[0] in isIn1v1Game):
                    continue
                else:
                    if ind in chooseplayer:
                        resList.append(rows[0])
                        i = i + 1
                        ind = ind + 1
                    else:
                        ind = ind + 1
            cursor.close()
            # conn.close()
            print "resList: " + str(resList)
            # print "isIn1v1deque: " + str(isIn1v1deque)
            return resList

        """
        group 1v1 players using their id
        """
        def dynamicGroup1v1(self, playerIdList, curTime):
            print "isInGame:" + str(self.gamingPool1v1) + " at curTime = " + str(curTime)
            # query the league using player_id, the output = [[player_id, score, league],..]
            res = GameDao.queryScoreAndLeague(playerIdList)
            print res
            # put the current [player_id, score] into the corresponding deque according to his league
            bronze1v1PlayerInfo = []
            silver1v1PlayerInfo = []
            gold1v1PlayerInfo = []
            platinum1v1PlayerInfo = []
            diamond1v1PlayerInfo = []
            master1v1PlayerInfo = []
            grandmaster1v1PlayerInfo = []
            # at the beginning of each round, we need to copy the players id from high league deque to
            # the low league deque according to their waiting time.
            # GrandMaster => Master
            self.copyPlayerId(self.GrandMaster1v1WaitTime, self.isIn1v1GrandMasterdeque,
                              self.GrandMaster1v1Deque, self.isIn1v1Masterdeque, self.Master1v1Deque,
                              self.MasterLeague, curTime, 1)
            # Master => Diamond
            self.copyPlayerId(self.Master1v1WaitTime, self.isIn1v1Masterdeque,
                              self.Master1v1Deque, self.isIn1v1Diamonddeque, self.Diamond1v1Deque,
                              self.DiamondLeague, curTime, 1)
            # Diamond => Platinum
            self.copyPlayerId(self.Diamond1v1WaitTime, self.isIn1v1Diamonddeque,
                              self.Diamond1v1Deque, self.isIn1v1Platinumdeque, self.Platinum1v1Deque,
                              self.PlatinumLeague, curTime, 1)
            # Platinum => Gold
            self.copyPlayerId(self.Platinum1v1WaitTime, self.isIn1v1Platinumdeque,
                              self.Platinum1v1Deque, self.isIn1v1Golddeque, self.Gold1v1Deque,
                              self.GoldLeague, curTime, 1)
            # Gold => Silver
            self.copyPlayerId(self.Gold1v1WaitTime, self.isIn1v1Golddeque,
                              self.Gold1v1Deque, self.isIn1v1Silverdeque, self.Silver1v1Deque,
                              self.SilverLeague, curTime, 1)
            # Silver => Bronze
            self.copyPlayerId(self.Silver1v1WaitTime, self.isIn1v1Silverdeque,
                              self.Silver1v1Deque, self.isIn1v1Bronzedeque, self.Bronze1v1Deque,
                              self.BronzeLeague, curTime, 1)
            # add all the current players in their corresponding deque
            for i in range(len(res)):
                player = res[i]
                player_id = player[0]
                player_league = player[2]
                # GrandMaster
                if player_league == self.GrandMasterLeague:
                    self.isIn1v1GrandMasterdeque[player_id] = curTime
                    self.GrandMaster1v1Deque.append(player)
                # Master
                elif player_league == self.MasterLeague:
                    self.isIn1v1Masterdeque[player_id] = curTime
                    self.Master1v1Deque.append(player)
                # Diamond
                elif player_league == self.DiamondLeague:
                    self.isIn1v1Diamonddeque[player_id] = curTime
                    self.Diamond1v1Deque.append(player)
                # Platinum
                elif player_league == self.PlatinumLeague:
                    self.isIn1v1Platinumdeque[player_id] = curTime
                    self.Platinum1v1Deque.append(player)
                # Gold
                elif player_league == self.GoldLeague:
                    self.isIn1v1Golddeque[player_id] = curTime
                    self.Gold1v1Deque.append(player)
                # Silver
                elif player_league == self.SilverLeague:
                    self.isIn1v1Silverdeque[player_id] = curTime
                    self.Silver1v1Deque.append(player)
                # Bronze
                elif player_league == self.BronzeLeague:
                    self.isIn1v1Bronzedeque[player_id] = curTime
                    self.Bronze1v1Deque.append(player)
            # group the current players for each league deque
            # GrandMaster
            curGrandMasterLength = len(self.GrandMaster1v1Deque)
            while curGrandMasterLength >= self.GrandMaster1v1DequeSize:
                curPath = []
                for i in range(self.GrandMaster1v1DequeSize):
                    # current league: GrandMaster
                    top = self.GrandMaster1v1Deque.popleft()
                    top_id = top[0]
                    self.isIn1v1GrandMasterdeque.pop(top_id, None)
                    # lower league
                    if top_id in self.isIn1v1Masterdeque:
                        self.Master1v1Deque.remove(top)
                        self.isIn1v1Masterdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                grandmaster1v1PlayerInfo.append(curPath)
                curGrandMasterLength -= self.GrandMaster1v1DequeSize
            # Master
            curMasterLength = len(self.Master1v1Deque)
            while curMasterLength >= self.Master1v1DequeSize:
                curPath = []
                for i in range(self.Master1v1DequeSize):
                    # current league: Master
                    top = self.Master1v1Deque.popleft()
                    top_id = top[0]
                    self.isIn1v1Masterdeque.pop(top_id, None)
                    # lower league: Diamond
                    if top_id in self.isIn1v1Diamonddeque:
                        self.Diamond1v1Deque.remove(top)
                        self.isIn1v1Diamonddeque.pop(top_id, None)
                    # upper league: GrandMaster
                    if top_id in self.isIn1v1GrandMasterdeque:
                        self.GrandMaster1v1Deque.remove(top)
                        self.isIn1v1GrandMasterdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                master1v1PlayerInfo.append(curPath)
                curMasterLength -= self.Master1v1DequeSize
            # Diamond
            curDiamondLength = len(self.Diamond1v1Deque)
            while curDiamondLength >= self.Diamond1v1DequeSize:
                curPath = []
                for i in range(self.Diamond1v1DequeSize):
                    # current league: Diamond
                    top = self.Diamond1v1Deque.popleft()
                    top_id = top[0]
                    self.isIn1v1Diamonddeque.pop(top_id, None)
                    # lower level: Platinum
                    if top_id in self.isIn1v1Platinumdeque:
                        self.Platinum1v1Deque.remove(top)
                        self.isIn1v1Platinumdeque.pop(top_id, None)
                    # upper level: Master
                    if top_id in self.isIn1v1Masterdeque:
                        self.Master1v1Deque.remove(top)
                        self.isIn1v1Masterdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                diamond1v1PlayerInfo.append(curPath)
                curDiamondLength -= self.Diamond1v1DequeSize
            # Platinum
            curPlatinumLength = len(self.Platinum1v1Deque)
            while curPlatinumLength >= self.Platinum1v1DequeSize:
                curPath = []
                for i in range(self.Platinum1v1DequeSize):
                    # current league: Platinum
                    top = self.Platinum1v1Deque.popleft()
                    top_id = top[0]
                    self.isIn1v1Platinumdeque.pop(top_id, None)
                    # lower league: Gold
                    if top_id in self.isIn1v1Golddeque:
                        self.Gold1v1Deque.remove(top)
                        self.isIn1v1Golddeque.pop(top_id, None)
                    # upper league: Diamond
                    if top_id in self.isIn1v1Diamonddeque:
                        self.Diamond1v1Deque.remove(top)
                        self.isIn1v1Diamonddeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                platinum1v1PlayerInfo.append(curPath)
                curPlatinumLength -= self.Platinum1v1DequeSize
            # Gold
            curGoldLength = len(self.Gold1v1Deque)
            while curGoldLength >= self.Gold1v1DequeSize:
                curPath = []
                for i in range(self.Gold1v1DequeSize):
                    # current league: Gold
                    top = self.Gold1v1Deque.popleft()
                    top_id = top[0]
                    self.isIn1v1Golddeque.pop(top_id, None)
                    # lower league: Silver
                    if top_id in self.isIn1v1Silverdeque:
                        self.Silver1v1Deque.remove(top)
                        self.isIn1v1Silverdeque.pop(top_id, None)
                    # upper league: Platinum
                    if top_id in self.isIn1v1Platinumdeque:
                        self.Platinum1v1Deque.remove(top)
                        self.isIn1v1Platinumdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                gold1v1PlayerInfo.append(curPath)
                curGoldLength -= self.Gold1v1DequeSize
            # Silver
            curSilverLength = len(self.Silver1v1Deque)
            while curSilverLength >= self.Silver1v1DequeSize:
                curPath = []
                for i in range(self.Silver1v1DequeSize):
                    # current league: Silver
                    top = self.Silver1v1Deque.popleft()
                    top_id = top[0]
                    self.isIn1v1Silverdeque.pop(top_id, None)
                    # lower league: Bronze
                    if top_id in self.isIn1v1Bronzedeque:
                        self.Bronze1v1Deque.remove(top)
                        self.isIn1v1Bronzedeque.pop(top_id, None)
                    # upper league: Gold
                    if top_id in self.isIn1v1Golddeque:
                        self.Gold1v1Deque.remove(top)
                        self.isIn1v1Golddeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                silver1v1PlayerInfo.append(curPath)
                curSilverLength -= self.Silver1v1DequeSize
            # Bronze
            curBronzeLength = len(self.Bronze1v1Deque)
            while curBronzeLength >= self.Bronze1v1DequeSize:
                curPath = []
                for i in range(self.Bronze1v1DequeSize):
                    # current league: Bronze
                    top = self.Bronze1v1Deque.popleft()
                    top_id = top[0]
                    self.isIn1v1Bronzedeque.pop(top_id, None)
                    # upper league: Silver
                    if top_id in self.isIn1v1Silverdeque:
                        self.Silver1v1Deque.remove(top)
                        self.isIn1v1Silverdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                bronze1v1PlayerInfo.append(curPath)
                curBronzeLength -= self.Bronze1v1DequeSize

            # print the results of each deque
            # print "bronzeDeque: " + str(self.Bronze1v1Deque)
            # print "silverDeque: " + str(self.Silver1v1Deque)
            # print "goldDeque: " + str(self.Gold1v1Deque)
            # print "platinumDeque: " + str(self.Platinum1v1Deque)
            # print "diamondDeque: " + str(self.Diamond1v1Deque)
            # print "masterDeque: " + str(self.Master1v1Deque)
            # print "grandmasterDeque: " + str(self.GrandMaster1v1Deque)

            # return the results
            return bronze1v1PlayerInfo, silver1v1PlayerInfo, gold1v1PlayerInfo, \
                platinum1v1PlayerInfo, diamond1v1PlayerInfo, \
                master1v1PlayerInfo, grandmaster1v1PlayerInfo

        """
        group 2v2 players using their id
        """
        def dynamicGroup2v2(self, playerIdList, curTime):
            print "isInGame:" + str(self.gamingPool2v2) + " at curTime = " + str(curTime)
            # query the league using player_id, the output = [[player_id, score, league],..]
            res = GameDao.queryScoreAndLeague(playerIdList)
            print res
            # put the current [player_id, score] into the corresponding deque according to his league
            bronze2v2PlayerInfo = []
            silver2v2PlayerInfo = []
            gold2v2PlayerInfo = []
            platinum2v2PlayerInfo = []
            diamond2v2PlayerInfo = []
            master2v2PlayerInfo = []
            grandmaster2v2PlayerInfo = []
            # at the beginning of each round, we need to copy the players id from high league deque to
            # the low league deque according to their waiting time.
            # GrandMaster => Master
            self.copyPlayerId(self.GrandMaster2v2WaitTime, self.isIn2v2GrandMasterdeque,
                              self.GrandMaster2v2Deque, self.isIn2v2Masterdeque, self.Master2v2Deque,
                              self.MasterLeague, curTime, 1)
            # Master => Diamond
            self.copyPlayerId(self.Master2v2WaitTime, self.isIn2v2Masterdeque,
                              self.Master2v2Deque, self.isIn2v2Diamonddeque, self.Diamond2v2Deque,
                              self.DiamondLeague, curTime, 1)
            # Diamond => Platinum
            self.copyPlayerId(self.Diamond2v2WaitTime, self.isIn2v2Diamonddeque,
                              self.Diamond2v2Deque, self.isIn2v2Platinumdeque, self.Platinum2v2Deque,
                              self.PlatinumLeague, curTime, 1)
            # Platinum => Gold
            self.copyPlayerId(self.Platinum2v2WaitTime, self.isIn2v2Platinumdeque,
                              self.Platinum2v2Deque, self.isIn2v2Golddeque, self.Gold2v2Deque,
                              self.GoldLeague, curTime, 1)
            # Gold => Silver
            self.copyPlayerId(self.Gold2v2WaitTime, self.isIn2v2Golddeque,
                              self.Gold2v2Deque, self.isIn2v2Silverdeque, self.Silver2v2Deque,
                              self.SilverLeague, curTime, 1)
            # Silver => Bronze
            self.copyPlayerId(self.Silver2v2WaitTime, self.isIn2v2Silverdeque,
                              self.Silver2v2Deque, self.isIn2v2Bronzedeque, self.Bronze2v2Deque,
                              self.BronzeLeague, curTime, 1)
            # add all the current players in their corresponding deque
            for i in range(len(res)):
                player = res[i]
                player_id = player[0]
                player_league = player[2]
                # GrandMaster
                if player_league == self.GrandMasterLeague:
                    self.isIn2v2GrandMasterdeque[player_id] = curTime
                    self.GrandMaster2v2Deque.append(player)
                # Master
                elif player_league == self.MasterLeague:
                    self.isIn2v2Masterdeque[player_id] = curTime
                    self.Master2v2Deque.append(player)
                # Diamond
                elif player_league == self.DiamondLeague:
                    self.isIn2v2Diamonddeque[player_id] = curTime
                    self.Diamond2v2Deque.append(player)
                # Platinum
                elif player_league == self.PlatinumLeague:
                    self.isIn2v2Platinumdeque[player_id] = curTime
                    self.Platinum2v2Deque.append(player)
                # Gold
                elif player_league == self.GoldLeague:
                    self.isIn2v2Golddeque[player_id] = curTime
                    self.Gold2v2Deque.append(player)
                # Silver
                elif player_league == self.SilverLeague:
                    self.isIn2v2Silverdeque[player_id] = curTime
                    self.Silver2v2Deque.append(player)
                # Bronze
                elif player_league == self.BronzeLeague:
                    self.isIn2v2Bronzedeque[player_id] = curTime
                    self.Bronze2v2Deque.append(player)
            # group the current players for each league deque
            # GrandMaster
            curGrandMasterLength = len(self.GrandMaster2v2Deque)
            while curGrandMasterLength >= self.GrandMaster2v2DequeSize:
                curPath = []
                for i in range(self.GrandMaster2v2DequeSize):
                    # current league: GrandMaster
                    top = self.GrandMaster2v2Deque.popleft()
                    top_id = top[0]
                    self.isIn2v2GrandMasterdeque.pop(top_id, None)
                    # lower league
                    if top_id in self.isIn2v2Masterdeque:
                        self.Master2v2Deque.remove(top)
                        self.isIn2v2Masterdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                grandmaster2v2PlayerInfo.append(curPath)
                curGrandMasterLength -= self.GrandMaster2v2DequeSize
            # Master
            curMasterLength = len(self.Master2v2Deque)
            while curMasterLength >= self.Master2v2DequeSize:
                curPath = []
                for i in range(self.Master2v2DequeSize):
                    # current league: Master
                    top = self.Master2v2Deque.popleft()
                    top_id = top[0]
                    self.isIn2v2Masterdeque.pop(top_id, None)
                    # lower league: Diamond
                    if top_id in self.isIn2v2Diamonddeque:
                        self.Diamond2v2Deque.remove(top)
                        self.isIn2v2Diamonddeque.pop(top_id, None)
                    # upper league: GrandMaster
                    if top_id in self.isIn2v2GrandMasterdeque:
                        self.GrandMaster2v2Deque.remove(top)
                        self.isIn2v2GrandMasterdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                master2v2PlayerInfo.append(curPath)
                curMasterLength -= self.Master2v2DequeSize
            # Diamond
            curDiamondLength = len(self.Diamond2v2Deque)
            while curDiamondLength >= self.Diamond2v2DequeSize:
                curPath = []
                for i in range(self.Diamond2v2DequeSize):
                    # current league: Diamond
                    top = self.Diamond2v2Deque.popleft()
                    top_id = top[0]
                    self.isIn2v2Diamonddeque.pop(top_id, None)
                    # lower level: Platinum
                    if top_id in self.isIn2v2Platinumdeque:
                        self.Platinum2v2Deque.remove(top)
                        self.isIn2v2Platinumdeque.pop(top_id, None)
                    # upper level: Master
                    if top_id in self.isIn2v2Masterdeque:
                        self.Master2v2Deque.remove(top)
                        self.isIn2v2Masterdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                diamond2v2PlayerInfo.append(curPath)
                curDiamondLength -= self.Diamond2v2DequeSize
            # Platinum
            curPlatinumLength = len(self.Platinum2v2Deque)
            while curPlatinumLength >= self.Platinum2v2DequeSize:
                curPath = []
                for i in range(self.Platinum2v2DequeSize):
                    # current league: Platinum
                    top = self.Platinum2v2Deque.popleft()
                    top_id = top[0]
                    self.isIn2v2Platinumdeque.pop(top_id, None)
                    # lower league: Gold
                    if top_id in self.isIn2v2Golddeque:
                        self.Gold2v2Deque.remove(top)
                        self.isIn2v2Golddeque.pop(top_id, None)
                    # upper league: Diamond
                    if top_id in self.isIn2v2Diamonddeque:
                        self.Diamond2v2Deque.remove(top)
                        self.isIn2v2Diamonddeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                platinum2v2PlayerInfo.append(curPath)
                curPlatinumLength -= self.Platinum2v2DequeSize
            # Gold
            curGoldLength = len(self.Gold2v2Deque)
            while curGoldLength >= self.Gold2v2DequeSize:
                curPath = []
                for i in range(self.Gold2v2DequeSize):
                    # current league: Gold
                    top = self.Gold2v2Deque.popleft()
                    top_id = top[0]
                    self.isIn2v2Golddeque.pop(top_id, None)
                    # lower league: Silver
                    if top_id in self.isIn2v2Silverdeque:
                        self.Silver2v2Deque.remove(top)
                        self.isIn2v2Silverdeque.pop(top_id, None)
                    # upper league: Platinum
                    if top_id in self.isIn2v2Platinumdeque:
                        self.Platinum2v2Deque.remove(top)
                        self.isIn2v2Platinumdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                gold2v2PlayerInfo.append(curPath)
                curGoldLength -= self.Gold2v2DequeSize
            # Silver
            curSilverLength = len(self.Silver2v2Deque)
            while curSilverLength >= self.Silver2v2DequeSize:
                curPath = []
                for i in range(self.Silver2v2DequeSize):
                    # current league: Silver
                    top = self.Silver2v2Deque.popleft()
                    top_id = top[0]
                    self.isIn2v2Silverdeque.pop(top_id, None)
                    # lower league: Bronze
                    if top_id in self.isIn2v2Bronzedeque:
                        self.Bronze2v2Deque.remove(top)
                        self.isIn2v2Bronzedeque.pop(top_id, None)
                    # upper league: Gold
                    if top_id in self.isIn2v2Golddeque:
                        self.Gold2v2Deque.remove(top)
                        self.isIn2v2Golddeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                silver2v2PlayerInfo.append(curPath)
                curSilverLength -= self.Silver2v2DequeSize
            # Bronze
            curBronzeLength = len(self.Bronze2v2Deque)
            while curBronzeLength >= self.Bronze2v2DequeSize:
                curPath = []
                for i in range(self.Bronze2v2DequeSize):
                    # current league: Bronze
                    top = self.Bronze2v2Deque.popleft()
                    top_id = top[0]
                    self.isIn2v2Bronzedeque.pop(top_id, None)
                    # upper league: Silver
                    if top_id in self.isIn2v2Silverdeque:
                        self.Silver2v2Deque.remove(top)
                        self.isIn2v2Silverdeque.pop(top_id, None)
                    curPath.append([top[0], top[1]])
                bronze2v2PlayerInfo.append(curPath)
                curBronzeLength -= self.Bronze2v2DequeSize

            # print the results of each deque
            # print "bronzeDeque: " + str(self.Bronze1v1Deque)
            # print "silverDeque: " + str(self.Silver1v1Deque)
            # print "goldDeque: " + str(self.Gold1v1Deque)
            # print "platinumDeque: " + str(self.Platinum1v1Deque)
            # print "diamondDeque: " + str(self.Diamond1v1Deque)
            # print "masterDeque: " + str(self.Master1v1Deque)
            # print "grandmasterDeque: " + str(self.GrandMaster1v1Deque)

            # return the results
            return bronze2v2PlayerInfo, silver2v2PlayerInfo, gold2v2PlayerInfo, \
                platinum2v2PlayerInfo, diamond2v2PlayerInfo, \
                master2v2PlayerInfo, grandmaster2v2PlayerInfo

        """
        copy the player_id from the high league to low league
        """
        def copyPlayerId(self, fromDequeWaitTime, fromisInDeque, fromDeque,
                         toisInDeque, toDeque, toLeague, curTime, maxLeagueDiff = 1):
            # fromDeque is empty
            if len(fromDeque) == 0:
                return
            for i in range(len(fromDeque)):
                playerInfo = fromDeque[i]
                player_id = playerInfo[0]
                player_league = playerInfo[2]
                startTime = fromisInDeque[player_id]
                duration = curTime - startTime
                # if the duration exceed the waiting time limit
                if duration >= fromDequeWaitTime:
                    # if the player_id not copy before
                    if player_id not in toisInDeque:
                        # if the league diff not exceed the limit
                        if player_league - toLeague <= maxLeagueDiff:
                            if len(toisInDeque) == 0:
                                toisInDeque[player_id] = curTime
                                toDeque.appendleft(playerInfo)
                            else:
                                top = toDeque[0]
                                top_id = top[0]
                                toisInDeque[player_id] = toisInDeque[top_id]
                                toDeque.appendleft(playerInfo)
                else:
                    break

        """
        start 1v1 game for matched group
        """
        def startGame(self, playerGroup, curTime):
            gameDuration = random.sample(range(1, 3), 1)[0]
            endTime = curTime + gameDuration
            for i in range(0, len(playerGroup), 2):
                player1 = playerGroup[i]
                player2 = playerGroup[i + 1]
                player1_id = player1[0]
                player2_id = player2[0]
                # randNum = 1 : player1 win, randNum = 0 : player2 win
                randNum = random.randint(0, 1)
                if endTime not in self.gamingPool1v1:
                    self.gamingPool1v1[endTime] = []
                group = [player1_id, player2_id, randNum]
                self.gamingPool1v1[endTime].append(group)
            print "================================================================"
            print " The 1v1 game are starting... "
            print " The 1v1 game for the above players are starting at time = " + str(curTime)
            print " The 1v1 game for the above players are ending at time = " + str(endTime)
            print "================================================================"

        """
        start 2v2 game for matched group
        """
        def start2v2Game(self, playerGroup, curTime):
            pass

        """
        end game for matched group
        """
        def endGame(self, curTime):
            gameResults = []
            if curTime in self.gamingPool1v1:
                print "================================================================"
                print " The 1v1 game are ending..."
                print " The 1v1 game for the following players are ending at time = " + str(curTime)
                print "================================================================"
                playerList = self.gamingPool1v1[curTime]
                for i in range(len(playerList)):
                    player1_id = playerList[i][0]
                    player2_id = playerList[i][1]
                    play_res = playerList[i][2]
                    gameResults.append([player1_id, play_res])
                    gameResults.append([player2_id, 1 - play_res])
                self.gamingPool1v1.pop(curTime, None)
            return gameResults
        """
        play 1v1 game
        """
        def play1v1Game(self, bronze1v1PlayerInfo, silver1v1PlayerInfo, gold1v1PlayerInfo,
                        platinum1v1PlayerInfo, diamond1v1PlayerInfo,
                        master1v1PlayerInfo, grandmaster1v1PlayerInfo, curTime):
            # bronze
            if len(bronze1v1PlayerInfo) != 0:
                for i in range(len(bronze1v1PlayerInfo)):
                    tempBronzePlayerInfo = bronze1v1PlayerInfo[i]
                    GameDao.showInfoAfterGame(tempBronzePlayerInfo)
                    playerGroup = GameDao.gameMatch1v1(tempBronzePlayerInfo)
                    GameDao.showGroup1v1(playerGroup)
                    self.printPlayerInfoByLeague(tempBronzePlayerInfo, self.BronzeLeague, curTime)
                    self.startGame(playerGroup, curTime)
            # silver
            if len(silver1v1PlayerInfo) != 0:
                for i in range(len(silver1v1PlayerInfo)):
                    tempSilverPlayerInfo = silver1v1PlayerInfo[i]
                    GameDao.showInfoAfterGame(tempSilverPlayerInfo)
                    playerGroup = GameDao.gameMatch1v1(tempSilverPlayerInfo)
                    GameDao.showGroup1v1(playerGroup)
                    self.printPlayerInfoByLeague(tempSilverPlayerInfo, self.SilverLeague, curTime)
                    self.startGame(playerGroup, curTime)
            # gold
            if len(gold1v1PlayerInfo) != 0:
                for i in range(len(gold1v1PlayerInfo)):
                    tempGoldPlayerInfo = gold1v1PlayerInfo[i]
                    GameDao.showInfoAfterGame(tempGoldPlayerInfo)
                    playerGroup = GameDao.gameMatch1v1(tempGoldPlayerInfo)
                    GameDao.showGroup1v1(playerGroup)
                    self.printPlayerInfoByLeague(tempGoldPlayerInfo, self.GoldLeague, curTime)
                    self.startGame(playerGroup, curTime)
            # platinum
            if len(platinum1v1PlayerInfo) != 0:
                for i in range(len(platinum1v1PlayerInfo)):
                    tempPlatinumPlayerInfo = platinum1v1PlayerInfo[i]
                    GameDao.showInfoAfterGame(tempPlatinumPlayerInfo)
                    playerGroup = GameDao.gameMatch1v1(tempPlatinumPlayerInfo)
                    GameDao.showGroup1v1(playerGroup)
                    self.printPlayerInfoByLeague(tempPlatinumPlayerInfo, self.PlatinumLeague, curTime)
                    self.startGame(playerGroup, curTime)
            # diamond
            if len(diamond1v1PlayerInfo) != 0:
                for i in range(len(diamond1v1PlayerInfo)):
                    tempDiamondPlayerInfo = diamond1v1PlayerInfo[i]
                    GameDao.showInfoAfterGame(tempDiamondPlayerInfo)
                    playerGroup = GameDao.gameMatch1v1(tempDiamondPlayerInfo)
                    GameDao.showGroup1v1(playerGroup)
                    self.printPlayerInfoByLeague(tempDiamondPlayerInfo, self.DiamondLeague, curTime)
                    self.startGame(playerGroup, curTime)
            # master
            if len(master1v1PlayerInfo) != 0:
                for i in range(len(master1v1PlayerInfo)):
                    tempMasterPlayerInfo = master1v1PlayerInfo[i]
                    GameDao.showInfoAfterGame(tempMasterPlayerInfo)
                    playerGroup = GameDao.gameMatch1v1(tempMasterPlayerInfo)
                    GameDao.showGroup1v1(playerGroup)
                    self.printPlayerInfoByLeague(tempMasterPlayerInfo, self.MasterLeague, curTime)
                    self.startGame(playerGroup, curTime)
            # grandmaster
            if len(grandmaster1v1PlayerInfo) != 0:
                for i in range(len(grandmaster1v1PlayerInfo)):
                    tempGrandMasterPlayerInfo = grandmaster1v1PlayerInfo[i]
                    GameDao.showInfoAfterGame(tempGrandMasterPlayerInfo)
                    playerGroup = GameDao.gameMatch1v1(tempGrandMasterPlayerInfo)
                    GameDao.showGroup1v1(playerGroup)
                    self.printPlayerInfoByLeague(tempGrandMasterPlayerInfo, self.GrandMasterLeague, curTime)
                    self.startGame(playerGroup, curTime)
            # end the game for each round
            gameResults = self.endGame(curTime)
            if len(gameResults) > 0:
                GameDao.show1v1GameRes(gameResults)
                GameDao.upDatePerformance(gameResults)

        """
        return the player_id list in the game according to the gaming pool
        """
        def playerListInGame(self, gamingPool):
            playerList = []
            values = gamingPool.values()
            if len(values) > 0:
                for i in range(len(values)):
                    biggroup = values[i]
                    for j in range(len(biggroup)):
                        player1_id = biggroup[j][0]
                        player2_id = biggroup[j][1]
                        playerList.append(player1_id)
                        playerList.append(player2_id)
            return playerList

        """
        print the current matched player_id list for specific league
        """
        @staticmethod
        def printPlayerInfoByLeague(curPlayerInfo, league, curTime):
            print "================================================================"
            print "1v1 Game Matched Players' ID are " + str(curPlayerInfo) + " at Time = " + str(curTime) \
                  + " for League = " + str(league)
            print "================================================================"

