from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Форум данни
forum_topics = [
    {
        "id": 1,
        "title": "Back Pain Solutions",
        "posts": [
            {
                "id": 1,
                "name": "Maria",
                "message": "How to relieve sciatica pain?",
                "replies": [
                    {"name": "John", "message": "Using a lumbar support cushion helped me a lot!"}
                ]
            }
        ]
    }
]

# Функции за търсене
def find_topic_by_id(topic_id):
    """Намира тема по ID."""
    return next((topic for topic in forum_topics if topic["id"] == topic_id), None)

def find_post_by_id(topic, post_id):
    """Намира пост по ID в тема."""
    return next((post for post in topic["posts"] if post["id"] == post_id), None)

def generate_new_id(collection):
    """Генерира ново ID за дадена колекция."""
    return max((item["id"] for item in collection), default=0) + 1

# Роутове
@app.route("/")
def home():
    """Начална страница."""
    return render_template("home.html")

@app.route("/products")
def products():
    """Продуктова страница."""
    return render_template("products.html")

@app.route("/back-pain")
def back_pain():
    """Страница за проблеми с гърба."""
    products = [
        {
            "name": "Ergonomic Office Chair",
            "description": "Designed to keep your spine aligned and reduce strain during long hours of sitting.",
            "link": "https://amzn.to/41M2Qzb"
        },
        {
            "name": "Lumbar Support Cushion",
            "description": "Perfect for office chairs, car seats, or sofas, this cushion ensures optimal lumbar support.",
            "link": "https://amzn.to/41M2Qzb"
        }
    ]
    return render_template("back_pain.html", products=products)

@app.route("/exercise-tools")
def exercise_tools():
    """Страница за фитнес уреди."""
    return render_template("exercise_tools.html")

@app.route("/cosmetic-products")
def cosmetic_products():
    """Страница за козметични продукти."""
    return render_template("cosmetic_products.html")

@app.route("/maria_story")
def maria_story():
    """Историята на Мария."""
    return render_template("maria_story.html")

@app.route("/forum")
def forum():
    """Страница на форума."""
    return render_template("forum.html", topics=forum_topics)

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    """Детайли за тема."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        abort(404, description="Topic not found")
    return render_template("topic.html", topic=topic)

@app.route("/add-topic", methods=["POST"])
def add_topic():
    """Добавяне на нова тема."""
    title = request.form.get("title")
    if not title:
        abort(400, description="Title is required")
    new_topic = {
        "id": generate_new_id(forum_topics),
        "title": title,
        "posts": []
    }
    forum_topics.append(new_topic)
    return redirect(url_for("forum"))

@app.route("/add-post/<int:topic_id>", methods=["POST"])
def add_post(topic_id):
    """Добавяне на пост в тема."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        abort(404, description="Topic not found")
    name = request.form.get("name")
    message = request.form.get("message")
    if not (name and message):
        abort(400, description="Name and message are required")
    new_post = {
        "id": generate_new_id(topic["posts"]),
        "name": name,
        "message": message,
        "replies": []
    }
    topic["posts"].append(new_post)
    return redirect(url_for("topic", topic_id=topic_id))

@app.route("/reply/<int:topic_id>/<int:post_id>", methods=["POST"])
def reply(topic_id, post_id):
    """Добавяне на отговор в пост."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        abort(404, description="Topic not found")
    post = find_post_by_id(topic, post_id)
    if not post:
        abort(404, description="Post not found")
    reply_name = request.form.get("name")
    reply_message = request.form.get("message")
    if not (reply_name and reply_message):
        abort(400, description="Name and message are required")
    post["replies"].append({"name": reply_name, "message": reply_message})
    return redirect(url_for("topic", topic_id=topic_id))

# Грешки
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", error=e), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html", error=e), 400

# Основен стартер
if __name__ == "__main__":
    app.run(debug=True)
