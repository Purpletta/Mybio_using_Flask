import sys

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import desc

from config import SQLITE_DATABASE_NAME, POST_MAX_NAME_LENGTH, POST_MAX_TEXT_LENGTH
from model import db, db_init, Post

app = Flask(__name__, template_folder="templates", static_folder="assets")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + SQLITE_DATABASE_NAME
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["SECRET_KEY"] = "verysecretkey"

db.app = app
db.init_app(app)


def save_post(name, text):
    if len(name) >= POST_MAX_NAME_LENGTH or len(text) >= POST_MAX_TEXT_LENGTH:
        flash("Too long name or text!", "error")
        return

    try:
        post = Post(name=name, text=text)
        db.session.add(post)
        db.session.commit()
    except:
        flash("Unexpected server error", "error")
        return

    flash("Successfully posted your comment!", "info")


@app.route('/', methods=["GET", "POST"])
def main_page():
    comments = Post.query.order_by(Post.created_on.desc()).all()

    if request.method == "POST":
        name = request.form.get("name", type=str, default="")
        text = request.form.get("message", type=str, default="")

        save_post(name, text)

        return redirect(url_for("main_page"))

    return render_template("index.html", comments=comments)


def start():
    if len(sys.argv) > 1:
        if sys.argv[1] == "initdb":
            with app.app_context():
                db_init()
                return

    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    start()