import threading
import json
import queue

import requests
import pymysql


def connect_to_mysql():
    conn = pymysql.connect(
        host = "localhost",
        user = "root", 
        port = 3306,
        db = "bilibili"
    )
    cur = conn.cursor()
    command = "CREATE TABLE IF NOT EXISTS `bilibili_user`( \
`mid` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
`birthday` VARCHAR(30) NOT NULL, \
`follower` INT NOT NULL, \
`following` INT NOT NULL, \
`level` INT NOT NULL, \
`rank` INT NOT NULL, \
`sex` VARCHAR(30) NOT NULL, \
`view` INT NOT NULL \
) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    # print(command)
    cur.execute(command)
    cur.execute("truncate table bilibili_user;")
    return cur, conn

class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        while True:
            crawler(self.name, self.q)
        print("Exiting", self.name)

# connect_to_mysql()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
conn = pymysql.connect(
        host = "localhost",
        user = "root", 
        port = 3306,
        db = "bilibili"
    )
cur = conn.cursor()
def crawler(threadName, q):
    conn = pymysql.connect(
        host = "localhost",
        user = "root", 
        port = 3306,
        db = "bilibili"
    )
    cur = conn.cursor()
    url = q.get(timeout = 2)
    mid = url.rsplit("=", 1)[1]
    print(f"{threadName} execute {url}")
    r = requests.get(url, headers = headers)
    data = r.content
    data = json.loads(data)
    if data["code"] != 0:
        return False
    birthday = data["birthday"]
    follower = data["follower"]
    following = data["following"]
    level = data["level"]
    rank = data["rank"]
    sex = data["sex"]
    view = data["view"]
    command = f"INSERT INTO bilibili_user VALUES ({mid}, '{birthday}', {follower}, {following}, {level}, {rank}, '{sex}', {view});"
    print(command)
    cur.execute(command)
    conn.commit()
    return True

threadList = []
for i in range(1, 4):
    threadList.append("Thread-" + str(i))

workQueue = queue.Queue(30000)
threads = []

for tName in threadList:
    thread = myThread(tName, workQueue)
    thread.start()
    threads.append(thread)

for i in range(30001, 50000):
    url = "http://gobili.herokuapp.com/api/user?mid=" + str(i)
    workQueue.put(url)

for t in threads:
    t.join()

cur.close()
conn.commit()
conn.close()