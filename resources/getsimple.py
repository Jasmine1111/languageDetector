# _*_ coding:utf8 _*_

import pymysql

conn = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root',passwd='shanbaymysql',db='bbc',charset='UTF8')
cur = conn.cursor()
cur.execute("select title,content from message where language='vietnamese'")
articles = cur.fetchall()
with open("vietnamese_sample.txt",'w') as out:
    for article in articles:
        title=article[0].encode('utf8')
        out.write(title)
        content = article[1].encode('utf8')
        out.write(content)
