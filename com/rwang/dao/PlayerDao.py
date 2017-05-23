#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import os
import random
import sys
import MySQLdb as mdb
from com.rwang.db import DBUtil
from com.rwang.model import Player


conn = DBUtil.getConnection()
with conn:
    """
    add player to database
    """
    def addPlayer(player):
        cursor = conn.cursor()
        sql = "INSERT INTO player" \
              + "(player_name, player_email, is_online)" \
              + "VALUES(%s, %s, %s)"
        try:
            cursor.execute(sql, (getattr(player, "__player_name"),
                                 getattr(player, "__player_email"),
                                 getattr(player, "__is_online")))
            conn.commit()
            flag = 1
        except Exception as e:
            print e
            flag = 0
            conn.rollback()
        cursor.close()
        return flag
        # conn.close()
    """
    update player in database
    """
    def updatePlayer(new_player, player_id):
        cursor = conn.cursor()
        sql = " UPDATE player " \
              + " SET player_name = %s, player_email = %s, is_online = %s " \
              + " WHERE id = %s"
        try:
            cursor.execute(sql, (getattr(new_player, "__player_name"),
                                 getattr(new_player, "__player_email"),
                                 getattr(new_player, "__is_online"), player_id))
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
        cursor.close()

    """
    delete player from database
    """
    def delPlayer(player_id):
        cursor = conn.cursor()
        sql = " DELETE FROM player " \
              + " WHERE id = %s "
        try:
            cursor.execute(sql, (player_id,))
            conn.commit()
            flag = 1
        except Exception as e:
            print e
            conn.rollback()
            flag = 0
        cursor.close()
        return flag
    """
    query all the information of the players in the database
    """
    def queryAll():
        cursor = conn.cursor()
        sql = "SELECT * FROM player"
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

    """
    get an information of a specific player according to his id
    """
    def get(player_id):
        cursor = conn.cursor()
        sql = " SELECT * FROM player " \
            + " WHERE id = %s"
        cursor.execute(sql, (player_id,))
        res = []
        row = cursor.fetchone()
        if row is None:
            return res
        cursor.close()
        # conn.close()
        for i in range(len(row)):
            res.append(row[i])
        return res
    """
    search the information of players according to his player_name and email
    """
    def query(player_name, player_email):
        cursor = conn.cursor()
        sql = " SELECT * FROM player " \
              + " WHERE player_name LIKE %s and player_email LIKE %s "
        cursor.execute(sql, ("%" + player_name + "%", "%" + player_email + "%"))
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
    query all the information of the on-line players in the database
    """

    def queryOnline():
        cursor = conn.cursor()
        sql = " SELECT * FROM player " \
              + " WHERE is_online = 1"
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

    """
    query the player_id according to player's email
    """
    def queryIdByEmail(player_email):
        cursor = conn.cursor()
        sql = " SELECT id FROM player " \
              + " WHERE player_email = %s "
        cursor.execute(sql, (player_email, ))
        row = cursor.fetchone()
        cursor.close()
        return row[0]
        pass


















