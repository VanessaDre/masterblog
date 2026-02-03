import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = "posts.json"


def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=2)


def next_id(posts):
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1


def fetch_post_by_id(post_id, posts):
    for post in posts:
        if post.get("id") == post_id:
            return post
    return None


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        posts = load_posts()

        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        new_post = {
            "id": next_id(posts),
            "author": author,
            "title": title,
            "content": content,
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()
    post = fetch_post_by_id(post_id, posts)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        post["author"] = request.form.get("author", "").strip()
        post["title"] = request.form.get("title", "").strip()
        post["content"] = request.form.get("content", "").strip()

        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_posts()

    posts = [post for post in posts if post.get("id") != post_id]

    save_posts(posts)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

