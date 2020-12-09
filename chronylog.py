#!/usr/bin/env python3
# chron task that logs chronyc serverstats to db
# created 2020/12/09
# Mark@minty.me

import subprocess
import pymysql

def dbcon():
    ''' inits pymysql connection'''
    import config
    connection = pymysql.connect(host=config.dbhost, 
            user = config.dbuser,
            password = config.dbpass,
            db = config.db,
            cursorclass = pymysql.cursors.DictCursor)
    
    return connection



def usms(item):
    ''' determines if us or ms at end of string
    and returns value in ms'''
    
    if item[-2:] == 'us':
        newItem = int(item[:-2]) /1000
    elif item[-2:] == 'ms':
        newItem = int(item[:-2])
    else:
        newItem = "no"

    return str(newItem)


def getChronyOutput():
    '''Gets output from "chronyc -n -m sourcestats" and returns
    array list of each ip'''
    cmd = ["/usr/bin/chronyc" , "-n", "sourcestats" ]

    p = subprocess.check_output(cmd)
    
    # splits up into lines, and only includes the ones we want
    np = p.decode().split("\n")[3:-1]
    
    # puts into Array 1st and last 3 items
    # IP address, skew, offset, stdev  
    tempArray = []
    for line in np:
        tempArray.append(line.split()[:1]+line.split()[-3:])

    # remove us/ms from values and convert to ms (divide by 1000)
    tempArray2 = []
    for item in tempArray:
        ip, skew, offset, stdev = item
        tempArray2.append([ip, skew, usms(offset), usms(stdev)])
    # [
    # ['202.46.179.18', '0.146', -0.083, 0.287],
    # ['203.109.195.162', '0.243', -0.756, 0.287],
    # ['202.27.76.97', '0.046', 0.35, 0.228],
    # ['131.203.16.6', '0.026', -0.361, 0.149]
    # ] 

    return tempArray2


if __name__ == "__main__":
    p = getChronyOutput()
    import pdb; pdb.set_trace()
    print(p)
    con = dbcon()
    try:
        with con.cursor() as cursor:
            sql = "INSERT INTO stats (ip, skew, offset, stddev) VALUES (inet_aton(%s), %s, %s, %s)"
            for items in p:
                cursor.execute(sql, tuple(items))

        con.commit()
    finally:
        con.close()
