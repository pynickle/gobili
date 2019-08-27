from flask import Blueprint, flash, render_template, redirect, request
import requests
import re

from .api import user_main

user_app = Blueprint(__name__, "user_app")

@user_app.route("/")
def index():
    return redirect("/user/ask-id")

@user_app.route("/ask-id")
def ask_id():
    return render_template("user/ask_id.html")

@user_app.route("/info", methods=["POST"])
def info():
    mid = request.form.get("id")
    if not mid or not mid.isnumeric():
        flash("id输入错误！")
        return redirect("/user/ask-id")
    res = user_main(mid)
    if not res:
        flash("id输入错误！")
        return redirect("/")
    return render_template("user/user.html", data = res)