import requests
import json
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36"
}

def get_data_info(key):
    global data
    if data["data"][key] is None:
        return "未设置"
    else:
        return data["data"][key]

def video_main(aid):
    global data
    
    av = re.match(r"https://www.bilibili.com/video/av(.*)", aid)
    if av:
        aid = av.groups()[0]
    if not aid.isnumeric():
        para = aid.split("?", 1)
        if len(para) == 2 and para[0].isnumeric():
            aid = para[0]
        else:
            return False

    url = "https://api.bilibili.com/x/web-interface/view?aid=" + aid
    r = requests.get(url, headers=headers)
    data = json.loads(r.content.decode())
    if data["code"] != 0:
        return False
    title = get_data_info("title")
    tname = get_data_info("tname")
    desc = get_data_info("desc")
    duration = get_data_info("duration")
    owner = data["data"]["owner"]["name"]
    view = data["data"]["stat"]["view"]
    danmaku = data["data"]["stat"]["danmaku"]
    reply = data["data"]["stat"]["reply"]
    favorite = data["data"]["stat"]["favorite"]
    coin = data["data"]["stat"]["coin"]
    share = data["data"]["stat"]["share"]
    like = data["data"]["stat"]["like"]
    dislike = data["data"]["stat"]["dislike"]

    url = "https://api.bilibili.com/x/tag/archive/tags?aid=" + aid
    r = requests.get(url, headers=headers)
    data = json.loads(r.content.decode())
    if data["code"] != 0:
        return False
    tag_name, use = [], []
    for i in data["data"]:
        tag_name.append(i["tag_name"])
        use.append(i["count"]["use"])
    
    info = [title, tname, desc, duration, owner, view, danmaku, reply, favorite, \
    coin, share, like, dislike, tag_name, use]
    return info
    