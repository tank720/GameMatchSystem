#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb as mdb
import random
from com.rwang.db import DBUtil
from com.rwang.dao import PlayerDao


class Solution(object):
    def groupPlayer(self, A):
        Solution.minDiff = sys.maxint
        Solution.res = []
        m = sum(A) / 2
        # print m
        # print "res = " + str(Solution.res)
        self.dfs(A, m, 0, 0, [])
        # print "res = " + str(Solution.res)
        # print Solution.minDiff
        return Solution.res

    def dfs(self, A, m, start, curSum, curList):
        if start > len(A):
            return
        if len(curList) == len(A) / 2:
            if 0 <= m - curSum < Solution.minDiff:
                Solution.res[:] = []
                for e in curList:
                    Solution.res.append(e)
                Solution.minDiff = m - curSum
        for i in range(start, len(A)):
            self.dfs(A, m, i + 1, curSum + A[i], curList + [i])

    def group1v1(self, playerInfo):
        res = sorted(playerInfo, key=lambda player: player[1])  # sort the playerInfo according to scores
        return res
        pass

