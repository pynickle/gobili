from flask import Blueprint, flash, render_template, redirect, request
import requests
import re

from .api import user_main, video_main

video_app = Blueprint(__name__, "video_app")


@video_app.route("/")
def index():
    return redirect("/video/ask-id")


@video_app.route("/ask-id")
def ask_id():
    return render_template("video/ask_id.html")


@video_app.route("/info", methods=["POST"])
def info():
    aid = request.form.get("av")
    if not aid or not aid.isnumeric():
        flash("av输入错误！")
        return redirect("/video/ask-id")
    res = video_main(aid)
    if not res:
        flash("av输入错误！")
        return redirect("/")
    return render_template("video/video.html", data=res, zip=zip)
