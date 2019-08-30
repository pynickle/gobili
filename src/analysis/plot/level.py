import pymysql
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
conn = pymysql.connect(
        host = "localhost",
        user = "root", 
        port = 3306,
        db = "bilibili"
    )
cur = conn.cursor()

level = []
label = []
for i in range(7):
    cur.execute("select * from bilibili_user where level=" + str(i))
    level.append(len(cur.fetchall()))
    label.append("等级" + str(i))

plt.bar(range(7), level)
plt.xticks(range(7), label)
plt.title("哔哩哔哩用户级别分析")
plt.show()
