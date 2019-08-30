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
cur.execute("SELECT sex FROM bilibili_user;")

sex = cur.fetchall()
data = []
for i in sex:
    data.append(i[0])

percentage = []
label = ["男", "女", "保密"]

for i in label:
    percentage.append(data.count(i))

plt.pie(percentage, labels = label)
plt.title("哔哩哔哩用户性别分析")
plt.show()
