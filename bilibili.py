import json
import os
import re

import requests
from lxml import etree
import numpy as np
import jieba
import wordcloud
from PIL import Image


stopwords = ["!", "！", "?", "？", "。", ".", ",", "，", "\\", "/"]
alice_mask = np.array(Image.open("./static/wordcloud.jpg"))


def get_word(aid):
    av = re.match(r"https://www.bilibili.com/video/av(.*)", aid)
    if av:
        aid = av.groups()[0]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    url = "https://api.bilibili.com/x/web-interface/view?aid=" + aid
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode())
    if data["code"] != 0:
        return False
    else:
        cid = data["data"]["cid"]
        cid_url = "https://comment.bilibili.com/{}.xml".format(cid)

        result = requests.get(cid_url, headers=headers)
        comment_element = etree.HTML(result.content)
        d_list = comment_element.xpath("//d")

        with open("./instance/comment.txt", "w", encoding="utf-8") as file:
            for d in d_list:
                file.write(d.xpath("./text()")[0] + "\n")
        return True


def chinese_jieba(txt):
    wordlist_jieba = jieba.cut(txt)
    txt_jieba = " ".join(wordlist_jieba)
    return txt_jieba


def make_cloud():
    with open('./instance/comment.txt', encoding="utf-8") as f:
        txt = f.read()
        txt = chinese_jieba(txt)
        wc = wordcloud.WordCloud(
            font_path='./static/wc.ttf',
            max_words=30,
            stopwords=stopwords,
            mask=alice_mask,
            background_color="white",
        ).generate(txt)
        image = wc.to_file("./static/bilibili.jpg")

def get_ready():
    if os.path.exists("./instance/comment.txt"):
        os.remove("./instance/comment.txt")
    if os.path.exists("./static/bilibili.jpg"):
        os.remove("./static/bilibili.jpg")

def main(aid):
    get_ready()
    res = get_word(aid)
    if not res:
        return False
    make_cloud()
    return True
