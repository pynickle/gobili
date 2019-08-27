import requests
import json
import urllib.request
import http.cookiejar

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36"
}

def get_data_info(key):
    global data
    if data["data"][key] is None:
        return "未设置"
    else:
        return data["data"][key]

def user_main(mid):
    global data
    url = "http://api.bilibili.com/x/relation/stat?vmid=" + mid
    r = requests.get(url, headers=headers)
    data = json.loads(r.content.decode())
    if data["code"] != 0:
        return False
    following = get_data_info("following")
    follower = get_data_info("follower")

    url = "http://api.bilibili.com/x/space/upstat?mid=" + mid
    r = requests.get(url, headers = headers)
    data = json.loads(r.content.decode())
    if data["code"] != 0:
        return False
    view = data["data"]["archive"]["view"]

    url = "https://api.bilibili.com/x/space/acc/info?mid=" + mid
    r = requests.get(url, headers = headers)
    data = json.loads(r.content.decode())
    if data["code"] != 0:
        return False
    name = get_data_info("name")
    sign = get_data_info("sign")
    sex = get_data_info("sex")
    rank = get_data_info("rank")
    level = get_data_info("level")
    birthday = get_data_info("birthday")

    mid = get_data_info("mid")

    url = f"https://api.bilibili.com/x/web-interface/elec/show?aid={aid}&mid={mid}"
    r = requests.get(url, headers=headers)
    data = json.loads(r.content.decode())
    if data["code"] != 0:
        return False
    elec_name = []
    for i in data["data"]["av_list"]:
        elec_name.append(i["uname"])

    info = [name, sign, sex, rank, level, birthday, following, follower, view, elec_name]
    return info 

if __name__ == "__main__":
    user_main()
