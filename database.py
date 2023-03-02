"""数据读取"""


import MySQLdb
import MySQLdb.cursors

HOSTNAME = "175.178.4.151"
PORT = 3306
DATABASE = "earthquake"
USERNAME = "root"
PASSWORD = "2001G1225"

'''
Insert items into database
@author: hakuri
'''


def GetData(TableName):
    try:
        conn = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DATABASE, port=PORT, cursorclass=MySQLdb.cursors.DictCursor)  # 链接数据库
        cur = conn.cursor()

        # 推断表是否存在，存在运行try
        try:
            cur.execute("SELECT DISTINCT * FROM  %s" % TableName)
            data = cur.fetchall()
            return data

        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
