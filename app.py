from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import calendar
from datetime import datetime

app = Flask(__name__)

# Данни за празници
holidays = [
    {"date": "2025-01-01", "name": "New Year's Day"},
    {"date": "2025-03-17", "name": "St. Patrick's Day"},
    {"date": "2025-05-12", "name": "Mother's Day"},
    {"date": "2025-06-16", "name": "Father's Day"},
    {"date": "2025-12-25", "name": "Christmas Day"}
]

# Генериране на календар
def generate_calendar(year, month, holidays):
    """Генерира календар с отбелязани празници."""
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    holiday_dates = {
        datetime.strptime(h["date"], "%Y-%m-%d").day: h["name"]
        for h in holidays if datetime.strptime(h["date"], "%Y-%m-%d").month == month
    }
    return month_days, holiday_dates

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
    """Начална страница с календар."""
    today = datetime.today()
    year, month = today.year, today.month
    month_days, holiday_dates = generate_calendar(year, month, holidays)
    month_name = calendar.month_name[month]
    return render_template(
        "home.html",
        month_days=month_days,
        holiday_dates=holiday_dates,
        month_name=month_name,
        year=year
    )

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
    title = request.json.get("title")
    if not title:
        return jsonify({"success": False, "error": "Title is required"}), 400
    new_topic = {
        "id": generate_new_id(forum_topics),
        "title": title,
        "posts": []
    }
    forum_topics.append(new_topic)
    return jsonify({"success": True, "topic": new_topic})

@app.route("/add-post/<int:topic_id>", methods=["POST"])
def add_post(topic_id):
    """Добавяне на пост в тема."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        return jsonify({"success": False, "error": "Topic not found"}), 404
    name = request.json.get("name")
    message = request.json.get("message")
    if not (name and message):
        return jsonify({"success": False, "error": "Name and message are required"}), 400
    new_post = {
        "id": generate_new_id(topic["posts"]),
        "name": name,
        "message": message,
        "replies": []
    }
    topic["posts"].append(new_post)
    return jsonify({"success": True, "post": new_post})

@app.route("/reply/<int:topic_id>/<int:post_id>", methods=["POST"])
def reply(topic_id, post_id):
    """Добавяне на отговор в пост."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        return jsonify({"success": False, "error": "Topic not found"}), 404
    post = find_post_by_id(topic, post_id)
    if not post:
        return jsonify({"success": False, "error": "Post not found"}), 404
    reply_name = request.json.get("name")
    reply_message = request.json.get("message")
    if not (reply_name and reply_message):
        return jsonify({"success": False, "error": "Name and message are required"}), 400
    reply = {"name": reply_name, "message": reply_message}
    post["replies"].append(reply)
    return jsonify({"success": True, "reply": reply})

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
