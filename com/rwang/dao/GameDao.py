#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb as mdb
import random
from com.rwang.db import DBUtil
from com.rwang.dao import PlayerDao
from com.rwang.dao.Core import Solution


conn = DBUtil.getConnection()
with conn:

    """
    select players to play the game 
    output: playerInfo = [[player1, 1200], [player2, 2000], [player3, 3400]]
    """

    def selectPlayers(num_players):
        res = PlayerDao.queryOnline()  # get the list of online players
        num_online = len(res)  # num of online players
        # print num_online
        index_player = random.sample(range(num_online), num_players)
        # print index_player
        # print "The following players are going to play the game: "
        id_list = []
        for i in index_player:
            id_list.append(res[i][0])
        scores = getScore(id_list)
        playerInfo = []
        for i in range(len(id_list)):
            p = [id_list[i], scores[i]]
            playerInfo.append(p)
        return playerInfo
        pass

    """
    game matching according to playerInfo
    input: playerInfo = [[player1, 1200], [player2, 2000], [player3, 3400]]
    output: playerGroup = [[player1, group1], [player2, group1], [player3, group2]]
    """
    def gameMatching(playerInfo):
        scores = []
        for i in range(len(playerInfo)):
            scores.append(playerInfo[i][1])
        # print "scores: " + str(scores)

        playerGroup = playerInfo
        for i in range(len(playerInfo)):
            playerGroup[i][1] = "group2"
        # index = 0
        # print "index:" + str(index)
        # print groupPlayer(scores)
        sol = Solution()
        index = sol.groupPlayer(scores)

        # print "index:" + str(index)

        for i in range(len(index)):
            playerGroup[index[i]][1] = "group1"
        return playerGroup
        pass


    """
    generate gameResults according to the matched playerGroup
    input: [[player1, group1], [player2, group1], [player3, group2], [player4, group2]]
    output: gameResults = [[player1, 1], [player2, 1], [player3, 0], [player4, 0]]
    """

    """
    change the performance of players according to the game results
    input: gameResults = [[player1, 1], [player2, 0], [player3, 1]]
    where "1" represents win and "0" represents lose
    """
    def upDatePerformance(gameResults, winScore=200, loseScore=200,
                          baseScore=100, leagueBound=(2000, 5000, 10000, 20000, 50000, 100000)):
        cursor = conn.cursor()
        for i in range(len(gameResults)):
            player_id = gameResults[i][0]
            game_res = gameResults[i][1]
            curLeague = queryLeague(player_id)
            if game_res == 1:
                sql = " UPDATE performance " \
                      " SET num_win = num_win + 1, " \
                      " league = IF((score + %s > %s) && (league < 7), league + 1, league), " \
                      " score = score + %s " \
                      " WHERE id = %s"
                try:
                    cursor.execute(sql, (winScore, leagueBound[curLeague - 1], winScore, player_id))
                    conn.commit()
                except Exception as e:
                    print e
                    conn.rollback()
            else:
                sql = " UPDATE performance " \
                      " SET num_lose = num_lose + 1, " \
                      " league = IF((score - %s > %s) && (score - %s <= %s) && (league > 1), league - 1, league), " \
                      " score = If(score - %s > %s, score - %s, score) " \
                      " WHERE id = %s"
                try:
                    cursor.execute(sql, (loseScore, baseScore, loseScore, leagueBound[curLeague - 2],
                                         loseScore, baseScore, loseScore, player_id))
                    conn.commit()
                except Exception as e:
                    print e
                    conn.rollback()
        cursor.close()


    """
    query all the information of the players' performance in the database
    """

    """
    query the league according to player_id
    """
    def queryLeague(player_id):
        cursor = conn.cursor()
        sql = " SELECT league FROM performance " \
              + " WHERE id = %s"
        cursor.execute(sql, (player_id,))
        league = cursor.fetchone()
        return league[0]
        pass


    """
    query the full information of one player
    """
    def queryCompleteInfo():
        cursor = conn.cursor()
        sql = "SELECT u.id, u.player_name, u.player_email, " \
              " p.num_win, p.num_lose, p.score, l.name " \
              " FROM((player AS u INNER JOIN performance AS p ON u.id = p.id) " \
              " INNER JOIN league AS l ON p.league = l.id) "
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        # conn.close()
        res = []
        for row in rows:
            resList = []
            for i in range(len(row)):
                resList.append(row[i])
            res.append(resList)
        return res
        pass

    """
    insert the performance of the player by player_id
    """
    def addPerformance(player_id):
        cursor = conn.cursor()
        sql = " INSERT INTO performance (id) VALUES (%s) "
        try:
            cursor.execute(sql, (player_id, ))
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
        cursor.close()
        pass

    """
    delete the performance of the player by player_id
    """

    """
    query the score of the selected player_id
    """

    """
    backpack test
    """
    def backPack(m, A):
        n = len(A)
        dp = [[0 for i in range(m + 1)] for i in range(n + 1)]
        subsets = [[[] for i in range(m + 1)] for i in range(n + 1)]
        # print subsets
        dp[0][0] = 1
        for i in range(n):
            for j in range(m + 1):
                dp[i + 1][j] = dp[i][j]
                if dp[i][j]:
                    subsets[i + 1][j] = subsets[i][j]
                if j >= A[i] and dp[i][j - A[i]]:
                    dp[i + 1][j] = 1
                    if len(subsets[i + 1][j]):
                        continue
                    for e in subsets[i][j - A[i]]:
                        subsets[i + 1][j].append(e)
                    subsets[i + 1][j].append(i)

        for i in range(m, -1, -1):
            if dp[n][i] == 1:
                return i, subsets[n][i]
        return 0, []
        pass

    """
    show the information of the people who are playing the game:
    """
    def showPlayerInfo(playerInfo):
        cursor = conn.cursor()
        resList = []
        for i in range(len(playerInfo)):
            player_id = playerInfo[i][0]
            player_score = playerInfo[i][1]

            sql = " SELECT player_name FROM player " \
                  + " WHERE id = %s "
            cursor.execute(sql, (player_id, ))
            row = cursor.fetchone()

            curList = [player_id, row[0], player_score]
            resList.append(curList)
        cursor.close()
        # for e in resList:
        #     print " player_id: " + str(e[0]) + ", player_name: " + e[1] + ", player_score: " + str(e[2])
        return resList


    """
    show the information of the people who are playing the game after grouped:
    """
    def showGroupedPlayerInfo(playerGroup, resList):
        print "================================================================"
        print " After group :"
        group1 = []
        group2 = []
        for i in range(len(playerGroup)):
            if playerGroup[i][1] == "group1":
                group1.append(resList[i])
            else:
                group2.append(resList[i])

        print " Group 1 : "
        for p1 in group1:
            print " player_id: " + str(p1[0]) + ", player_name: " + p1[1] + ", player_score: " + str(p1[2])
        print " Group 2 :"
        for p2 in group2:
            print " player_id: " + str(p2[0]) + ", player_name: " + p2[1] + ", player_score: " + str(p2[2])

        pass

    """
    show the general game results of each group
    """
    def showGroupRes(groupRes):
        print "================================================================"
        print " The game is over !!! The result of this game : "
        if groupRes[0] == 1:
            print " Group 1 Win !!! "
        else:
            print " Group 2 Win !!! "
        pass

    """
    show the info of the players 
    """
    def showInfoAfterGame(playerInfo):
        print "================================================================"
        print " The info of the players are: "
        cursor = conn.cursor()
        rows = []
        for p in playerInfo:
            player_id = p[0]
            sql = "SELECT u.id, u.player_name, u.player_email, " \
                  " p.num_win, p.num_lose, p.score, l.name " \
                  " FROM((player AS u INNER JOIN performance AS p ON u.id = p.id) " \
                  " INNER JOIN league AS l ON p.league = l.id) " \
                  " WHERE u.id = %s "
            cursor.execute(sql, (player_id, ))
            row = cursor.fetchone()
            rows.append(row)
        cursor.close()
        # conn.close()
        res = []
        for row in rows:
            resList = []
            for i in range(len(row)):
                resList.append(row[i])
            res.append(resList)

        for e in res:
            print " player_id: " + str(e[0]) \
                  + ", player_name: " + e[1] \
                  + ", player_email: " + e[2] \
                  + ", num_win: " + str(e[3]) \
                  + ", num_lose: " + str(e[4]) \
                  + ", score: " + str(e[5]) \
                  + ", league: " + e[6]
        return res
        pass


    """
    group all 1v1 players according to their scores
    """

    """
    show group results of 1v1 matching
    """

    """
    generate gameResults according to the matched playerGroup
    input: [[player1, group1], [player2, group1], [player3, group2], [player4, group2]]
    output: gameResults = [[player1, 1], [player2, 0], [player3, 0], [player4, 1]]
    """

    def genGame1v1Results(playerGroup):
        gameResults = playerGroup
        for i in range(0, len(gameResults), 2):
            randNum = random.randint(0, 1)
            gameResults[i][1] = randNum
            gameResults[i + 1][1] = 1 - randNum
        return gameResults
        pass

    """
    show the 1v1 game results of each group
    """
    def show1v1GameRes(gameResults):
        print "================================================================"
        print " The game is over !!! The result of this game : "
        for i in range(0, len(gameResults), 2):
            if gameResults[i][1] == 1:
                print " player " + str(gameResults[i][0]) + " win " + " and " \
                      + " player " + str(gameResults[i + 1][0]) + " lose !!!"
            else:
                print " player " + str(gameResults[i][0]) + " lose " + " and " \
                      + " player " + str(gameResults[i + 1][0]) + " win !!!"
        pass


    """
    group all 2v2 players according to their scores
    """
    def gameMatch2v2(playerInfo):
        sol = Solution()
        res = sol.group1v1(playerInfo)
        playerInfo = res
        playerGroup = []
        for i in range(0, len(playerInfo), 4):
            pI = playerInfo[i: i + 4]
            pG = gameMatching(pI)
            playerGroup.append(pG)
            pass
        return playerGroup
        pass


    """
    show group results of 2v2 matching
    """
    def showGroup2v2(playerGroup):
        print "================================================================"
        print " After group :"
        for i in range(0, len(playerGroup), 1):
            print " Group " + str(i + 1) + ": "
            group = playerGroup[i]
            groupLeft = []
            groupRight = []
            for i in range(len(group)):
                if group[i][1] == "group1":
                    groupLeft.append(group[i][0])
                else:
                    groupRight.append(group[i][0])
            print " player " + str(groupLeft[0]) + " + " \
                  " player " + str(groupLeft[1]) + \
                  " vs " +\
                  " player " + str(groupRight[0]) + " + " \
                  " player " + str(groupRight[1])
        pass


    """
    generate gameResults according to the matched playerGroup
    input: [[[1, 'group1'], [3, 'group2'], [5, 'group2'], [4, 'group1']], 
    [[2, 'group1'], [6, 'group2'], [7, 'group2'], [8, 'group1']]]
    output: gameResults = [[player1, 1], [player2, 0], [player3, 0], [player4, 1]]
    """
    def genGame2v2Results(playerGroup):
        gameResults = []
        groupRes = []
        for i in range(len(playerGroup)):
            randNum = random.randint(0, 1)
            group = playerGroup[i]
            for j in range(len(group)):
                if group[j][1] == "group1":
                    gameResults.append([group[j][0], randNum])
                    groupRes.append(randNum)
                else:
                    gameResults.append([group[j][0], 1 - randNum])
                    groupRes.append(1 - randNum)
        return gameResults, groupRes
        pass


    """
    show the 2v2 game results of each group
    input: gameResults = [[player1, 1], [player2, 0], [player3, 0], [player4, 1]]
    """
    def show2v2GameRes(groupRes, playerGroup):
        print "================================================================"
        print " The game is over !!! The result of this game : "
        for i in range(0, len(playerGroup), 1):
            print " Group " + str(i + 1) + ": "
            group = playerGroup[i]
            groupLeft = []
            groupRight = []
            for j in range(len(group)):
                if group[j][1] == "group1":
                    groupLeft.append(group[j][0])
                else:
                    groupRight.append(group[j][0])
            if groupRes[i] == 1:
                print " player " + str(groupLeft[0]) + " + " \
                      " player " + str(groupLeft[1]) + \
                      " win !!!"
                print " player " + str(groupRight[0]) + " + " \
                      " player " + str(groupRight[1]) + \
                      " lose !!!"
            else:
                print " player " + str(groupLeft[0]) + " + " \
                      " player " + str(groupLeft[1]) + \
                      " lose !!!"
                print " player " + str(groupRight[0]) + " + " \
                      " player " + str(groupRight[1]) + \
                      " win !!!"
        pass

    """
    group all 3v3 players according to their scores
    """
    def gameMatch3v3(playerInfo):
        sol = Solution()
        res = sol.group1v1(playerInfo)
        playerInfo = res
        playerGroup = []
        for i in range(0, len(playerInfo), 6):
            pI = playerInfo[i: i + 6]
            pG = gameMatching(pI)
            playerGroup.append(pG)
            pass
        return playerGroup
        pass


    """
    show group results of 3v3 matching
    """
    def showGroup3v3(playerGroup):
        print "================================================================"
        print " After group :"
        for i in range(0, len(playerGroup), 1):
            print " Group " + str(i + 1) + ": "
            group = playerGroup[i]
            groupLeft = []
            groupRight = []
            for j in range(len(group)):
                if group[j][1] == "group1":
                    groupLeft.append(group[j][0])
                else:
                    groupRight.append(group[j][0])
            print " player " + str(groupLeft[0]) + " + " \
                  " player " + str(groupLeft[1]) + " + " \
                  " player " + str(groupLeft[2]) + \
                  " vs " + \
                  " player " + str(groupRight[0]) + " + " \
                  " player " + str(groupRight[1]) + " + " \
                  " player " + str(groupRight[2])
        pass


    """
    show the 3v3 game results of each group
    input: gameResults = [[player1, 1], [player2, 0], [player3, 0], [player4, 1]]
    """
    def show3v3GameRes(groupRes, playerGroup):
        print "================================================================"
        print " The game is over !!! The result of this game : "
        for i in range(0, len(playerGroup), 1):
            print " Group " + str(i + 1) + ": "
            group = playerGroup[i]
            groupLeft = []
            groupRight = []
            for j in range(len(group)):
                if group[j][1] == "group1":
                    groupLeft.append(group[j][0])
                else:
                    groupRight.append(group[j][0])
            if groupRes[i] == 1:
                print " player " + str(groupLeft[0]) + " + " \
                      " player " + str(groupLeft[1]) + " + " \
                      " player " + str(groupLeft[2]) + \
                      " win !!!"
                print " player " + str(groupRight[0]) + " + " \
                      " player " + str(groupRight[1]) + " + " \
                      " player " + str(groupRight[2]) + \
                      " lose !!!"
            else:
                print " player " + str(groupLeft[0]) + " + " \
                      " player " + str(groupLeft[1]) + " + " \
                      " player " + str(groupLeft[2]) + \
                      " lose !!!"
                print " player " + str(groupRight[0]) + " + " \
                      " player " + str(groupRight[1]) + " + " \
                      " player " + str(groupRight[2]) + \
                      " win !!!"
        pass

    """
    group all 4v4 players according to their scores
    """

    """
    show group results of 4v4 matching
    """

    """
    show the 4v4 game results of each group
    input: gameResults = [[player1, 1], [player2, 0], [player3, 0], [player4, 1]]
    """











