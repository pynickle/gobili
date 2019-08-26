from flask import Flask, render_template, request, redirect, \
    flash, send_from_directory

from bilibili import main

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bilibili", methods=["POST"])
def bilibili():
    aid = request.form.get("aid")
    res = main(aid)
    if not res:
        flash("网址或av码错误！")
        return redirect("/")
    return redirect("/show")

@app.route("/show")
def show():
    return render_template("show.html")

@app.route("/download")
def download():
    return send_from_directory("static", "bilibili.jpg", as_attachment=True)

if __name__ == "__main__":
    app.run(port=5800, debug=True)