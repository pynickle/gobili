import json

from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from .get_api import user_main, video_main

user_parser = RequestParser()
user_parser.add_argument("mid", type=int, location="args", required=True, help="mid must be provided and is type int")

video_parser = RequestParser()
video_parser.add_argument("aid", type=int, location="args", required=True, help="aid must be provided and is type int")

def dump_to_json(info, name):
    data = {}
    for key, value in zip(name, info):
        data[key] = value
    return data

class UserApi(Resource):
    def __init__(self):
        self.error404 = jsonify({"code": 404, "msg": "mid wrong!"})

    def get(self):
        req = user_parser.parse_args()
        mid = req.get("mid")
        data = self._get_info(mid)
        return data

    def _get_info(self, mid):
        info = user_main(str(mid))
        name = ["name", "sign", "sex", "rank", "level", "birthday", "following", "follower", "view"]
        if not info:
            return self.error404
        data = dump_to_json(info, name)
        data["code"] = 0
        return jsonify(data)
        
class VideoApi(Resource):
    def __init__(self):
        self.error404 = jsonify({"code": 404, "msg": "aid wrong!"})

    def get(self):
        req = video_parser.parse_args()
        aid = req.get("aid")
        data = self._get_info(aid)
        return data

    def _get_info(self, aid):
        info = video_main(str(aid))
        name = ["title", "tname", "desc", "duration", "owner", "view", "danmaku", "reply", "favorite", \
    "coin", "share", "like", "dislike", "tag_name", "use", "elec_name"]
        if not info:
            return self.error404
        data = dump_to_json(info, name)
        data["code"] = 0
        return jsonify(data)
