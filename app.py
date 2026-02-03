import json
import os
from flask import Flask, render_template

app = Flask(__name__)

DATA_FILE = "posts.json"


def load_posts():
    """Load blog posts from the JSON file. Returns a list."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
