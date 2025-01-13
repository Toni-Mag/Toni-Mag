from flask import Flask, render_template, request, jsonify, abort
import calendar
from datetime import datetime

app = Flask(__name__)

# Фиктивна база данни за форумни теми
forum_topics = [
    {
        "id": 1,
        "title": "Back Pain Solutions",
        "description": "Share your tips and experiences about dealing with back pain.",
        "posts": [
            {
                "id": 1,
                "name": "Maria",
                "message": "How to relieve sciatica pain?",
                "replies": [
                    {"name": "John", "message": "Using a lumbar support cushion helped me a lot!"}
                ]
            }
        ],
        "comments": [
            {"id": 1, "author": "Sarah", "text": "This is such a helpful discussion. Thanks!"}
        ]
    }
]

# Функция за генериране на календар
def generate_calendar():
    today = datetime.today()
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(today.year, today.month)
    holiday_dates = {15: "Holiday Example"}  # Примерен празник
    return {
        "month_name": calendar.month_name[today.month],
        "year": today.year,
        "today": today.strftime("%A, %B %d, %Y"),
        "month_days": month_days,
        "holiday_dates": holiday_dates,
    }

# Странично съдържание (sidebar)
def get_sidebar_content():
    return {
        "ads": [
            {"title": "Health Gadgets", "url": "#", "image": "/static/images/ad1.jpg"},
            {"title": "Posture Correctors", "url": "#", "image": "/static/images/ad2.jpg"},
        ],
        "videos": [
            {"title": "Stretching Exercises", "url": "https://www.youtube.com/embed/example1"},
            {"title": "Back Pain Relief", "url": "https://www.youtube.com/embed/example2"},
        ],
        "calendar": generate_calendar(),
    }

# API за добавяне на нова тема
@app.route("/api/add-topic", methods=["POST"])
def add_topic():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author", "Anonymous")

    if not title:
        return jsonify({"success": False, "error": "Topic title is required"}), 400

    new_id = max([t["id"] for t in forum_topics], default=0) + 1
    new_topic = {
        "id": new_id,
        "title": title,
        "description": f"Topic created by {author}.",
        "posts": [],
        "comments": []
    }
    forum_topics.append(new_topic)
    return jsonify({"success": True, "topic": new_topic})

# API за добавяне на нова публикация
@app.route("/api/add-post/<int:topic_id>", methods=["POST"])
def add_post(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return jsonify({"success": False, "error": "Topic not found"}), 404

    data = request.get_json()
    name = data.get("name", "Anonymous")
    message = data.get("message")

    if not message:
        return jsonify({"success": False, "error": "Message is required"}), 400

    new_post_id = max([p["id"] for p in topic["posts"]], default=0) + 1
    new_post = {"id": new_post_id, "name": name, "message": message, "replies": []}
    topic["posts"].append(new_post)
    return jsonify({"success": True, "post": new_post})

# API за добавяне на коментари
@app.route("/api/add-comment/<int:topic_id>", methods=["POST"])
def add_comment(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return jsonify({"success": False, "error": "Topic not found"}), 404

    data = request.get_json()
    author = data.get("name", "Anonymous")
    comment = data.get("comment")

    if not comment:
        return jsonify({"success": False, "error": "Comment is required"}), 400

    new_comment_id = max([c["id"] for c in topic["comments"]], default=0) + 1
    new_comment = {"id": new_comment_id, "author": author, "text": comment}
    topic["comments"].append(new_comment)
    return jsonify({"success": True, "comment": new_comment})

# Главна страница
@app.route("/")
def home():
    return render_template("home.html", topics=forum_topics, sidebar=get_sidebar_content())

# Страница за форума
@app.route("/forum")
def forum():
    return render_template("forum.html", topics=forum_topics, sidebar=get_sidebar_content())

# Страница за конкретна тема
@app.route("/forum/topic/<int:topic_id>")
def topic(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        abort(404, description="Topic not found")
    return render_template("topic.html", topic=topic, sidebar=get_sidebar_content())

# Страници за различни секции
@app.route("/cosmetic-products")
def cosmetic_products():
    return render_template("cosmetic_products.html", sidebar=get_sidebar_content())

@app.route("/exercise-tools")
def exercise_tools():
    return render_template("exercise_tools.html", sidebar=get_sidebar_content())

@app.route("/products")
def products():
    return render_template("products.html", sidebar=get_sidebar_content())

@app.route("/back-pain")
def back_pain():
    return render_template("back_pain.html", sidebar=get_sidebar_content())

@app.route("/maria_story")
def maria_story():
    return render_template("maria_story.html", sidebar=get_sidebar_content())

# Грешка 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", error=e, sidebar=get_sidebar_content()), 404

if __name__ == "__main__":
    app.run(debug=True)
