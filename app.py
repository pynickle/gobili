import os

from flask import Flask, render_template, request, redirect, \
    flash, send_from_directory

from src.api import barrage_main, user_main

from src import user_app, video_app

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(user_app, url_prefix="/user")
app.register_blueprint(video_app, url_prefix="/video")
app.config.from_pyfile("config.py")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/bilibili", methods=["POST"])
def bilibili():
    aid = request.form.get("aid")
    res = barrage_main(aid)
    if not res:
        flash("网址或av码错误！")
        return redirect("/")
    return redirect("/show")


@app.route("/show")
def show():
    return render_template("show.html")


@app.route("/download")
def download():
    if os.path.isfile("./static/bilibili.jpg"):
        return send_from_directory("static", "bilibili.jpg", as_attachment=True)
    else:
        flash("你尚未制作词云！")
        return redirect("/")


@app.route("/comment")
def comment():
    if os.path.isfile("./instance/comment.txt"):
        with open("./instance/comment.txt", mode="r", encoding="utf-8") as f:
            content = f.read()
        return render_template("comment.html", content=content)
    else:
        flash("你尚未制作词云！")
        return redirect("/")


if __name__ == "__main__":
    app.run(port=5800, debug=True)
