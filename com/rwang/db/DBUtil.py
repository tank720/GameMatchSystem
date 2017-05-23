# -*- coding: utf-8 -*-
import sys
import MySQLdb


def getConnection():
    conn = MySQLdb.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='',
        db='gamematchsystem',
        charset='utf8'
    )
    return conn
