from flask import Flask, render_template, request, jsonify, abort, redirect
import calendar
from datetime import datetime
from flask_caching import Cache

# Инициализация на приложението
app = Flask(__name__)

# Инициализация на кеша
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Главна страница с кеширане
@app.route("/")
@cache.cached(timeout=300)
def home():
    return render_template("home.html", topics=forum_topics, sidebar=get_sidebar_content())

# Пример за друга страница с кеширане
@app.route("/forum")
@cache.cached(timeout=300)
def forum():
    return render_template("forum.html", topics=forum_topics, sidebar=get_sidebar_content())

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

# Празници
holidays = [
    {"date": "2025-01-01", "name": "New Year's Day", "type": "Bank Holiday"},
    {"date": "2025-01-02", "name": "Last day of Hanukkah", "type": "Jewish Holiday"},
    {"date": "2025-01-02", "name": "2nd January", "type": "Local Bank Holiday (Scotland)"},
    {"date": "2025-01-05", "name": "Twelfth Night", "type": "Observance, Christian"},
    {"date": "2025-01-06", "name": "Epiphany", "type": "Observance, Christian"},
    {"date": "2025-01-07", "name": "Orthodox Christmas Day", "type": "Observance, Orthodox"},
    {"date": "2025-01-14", "name": "Orthodox New Year", "type": "Observance, Orthodox"},
    {"date": "2025-01-25", "name": "Burns Night", "type": "Local Observance, Scotland"},
    {"date": "2025-01-27", "name": "Isra and Mi'raj", "type": "Muslim"},
    {"date": "2025-01-29", "name": "Lunar New Year", "type": "Observance"},
    {"date": "2025-02-13", "name": "Tu B'Shevat (Arbor Day)", "type": "Jewish Holiday"},
    {"date": "2025-02-14", "name": "Valentine's Day", "type": "Observance"},
    {"date": "2025-02-26", "name": "Maha Shivaratri", "type": "Hindu Holiday"},
    {"date": "2025-03-01", "name": "Ramadan Start (Tentative Date)", "type": "Muslim"},
    {"date": "2025-03-01", "name": "St. David's Day", "type": "Local Observance, Wales"},
    {"date": "2025-03-04", "name": "Carnival / Shrove Tuesday / Pancake Day", "type": "Observance, Christian"},
    {"date": "2025-03-05", "name": "Carnival / Ash Wednesday", "type": "Observance, Christian"},
    {"date": "2025-03-14", "name": "Purim", "type": "Jewish Holiday"},
    {"date": "2025-03-17", "name": "St Patrick's Day", "type": "Local Bank Holiday, NIR"},
    {"date": "2025-03-20", "name": "March Equinox", "type": "Season"},
    {"date": "2025-03-26", "name": "Laylatul Qadr (Night of Power)", "type": "Muslim"},
    {"date": "2025-03-30", "name": "Mother's Day", "type": "Observance"},
    {"date": "2025-03-30", "name": "Daylight Saving Time starts", "type": "Clock Change/Daylight Saving Time"},
    {"date": "2025-03-31", "name": "Eid ul Fitr (Tentative Date)", "type": "Muslim"},
    {"date": "2025-04-13", "name": "Palm Sunday", "type": "Observance, Christian"},
    {"date": "2025-04-13", "name": "First day of Passover", "type": "Jewish Holiday"},
    {"date": "2025-04-17", "name": "Maundy Thursday", "type": "Observance, Christian"},
    {"date": "2025-04-18", "name": "Good Friday", "type": "Bank Holiday"},
    {"date": "2025-04-18", "name": "Orthodox Good Friday", "type": "Observance, Orthodox"},
    {"date": "2025-04-19", "name": "Holy Saturday", "type": "Observance, Christian"},
    {"date": "2025-04-19", "name": "Orthodox Holy Saturday", "type": "Observance, Orthodox"},
    {"date": "2025-04-20", "name": "Last day of Passover", "type": "Jewish Holiday"},
    {"date": "2025-04-20", "name": "Orthodox Easter", "type": "Observance, Orthodox"},
    {"date": "2025-04-20", "name": "Easter Sunday", "type": "Observance, Christian"},
    {"date": "2025-04-21", "name": "Orthodox Easter Monday", "type": "Observance, Orthodox"},
    {"date": "2025-04-21", "name": "Easter Monday", "type": "Common Local Holiday, ENG, NIR, WAL"},
    {"date": "2025-04-21", "name": "Easter Monday", "type": "Local Observance, Scotland"},
    {"date": "2025-05-05", "name": "Early May Bank Holiday", "type": "Bank Holiday"},
    {"date": "2025-05-16", "name": "Lag B'Omer", "type": "Jewish Holiday"},
    {"date": "2025-05-26", "name": "Spring Bank Holiday", "type": "Bank Holiday"},
    {"date": "2025-05-29", "name": "Ascension Day", "type": "Observance, Christian"},
    {"date": "2025-06-02", "name": "Shavuot", "type": "Jewish Holiday"},
    {"date": "2025-06-07", "name": "Eid al-Adha (Tentative Date)", "type": "Muslim"},
    {"date": "2025-06-08", "name": "Pentecost", "type": "Observance, Christian"},
    {"date": "2025-06-09", "name": "Whit Monday", "type": "Observance, Christian"},
    {"date": "2025-06-15", "name": "Trinity Sunday", "type": "Observance, Christian"},
    {"date": "2025-06-15", "name": "Father's Day", "type": "Observance"},
    {"date": "2025-06-19", "name": "Corpus Christi", "type": "Observance, Christian"},
    {"date": "2025-06-21", "name": "King's Birthday", "type": "Observance"},
    {"date": "2025-06-21", "name": "June Solstice", "type": "Season"},
    {"date": "2025-06-22", "name": "Windrush Day", "type": "Observance"},
    {"date": "2025-06-27", "name": "Muharram/Islamic New Year (Tentative Date)", "type": "Muslim"},
    {"date": "2025-07-06", "name": "Ashura (Tentative Date)", "type": "Muslim"},
    {"date": "2025-07-12", "name": "Battle of the Boyne", "type": "Local Bank Holiday, NIR"},
    {"date": "2025-08-04", "name": "Summer Bank Holiday", "type": "Local Bank Holiday, Scotland"},
    {"date": "2025-08-25", "name": "Summer Bank Holiday", "type": "Common Local Holiday, ENG, NIR, WAL"},
    {"date": "2025-12-25", "name": "Christmas Day", "type": "Bank Holiday"},
    {"date": "2025-12-26", "name": "Boxing Day", "type": "Bank Holiday"},
    {"date": "2025-12-31", "name": "New Year's Eve", "type": "Observance"},

]

# Функция за генериране на календар
def generate_calendar():
    today = datetime.today()
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(today.year, today.month)

    # Създайте речник с празници за текущия месец
    month_holidays = {
        datetime.strptime(holiday["date"], "%Y-%m-%d").day: holiday["name"]
        for holiday in holidays
        if datetime.strptime(holiday["date"], "%Y-%m-%d").month == today.month
    }

    return {
        "month_name": calendar.month_name[today.month],
        "year": today.year,
        "today": today.strftime("%A, %B %d, %Y"),
        "month_days": month_days,
        "holiday_dates": month_holidays,
    }

# Странично съдържание (sidebar)
def get_sidebar_content():
    calendar_data = generate_calendar()
    return {
        "ads": [
            {"title": "Health Gadgets", "url": "#", "image": "/static/images/ad1.jpg"},
            {"title": "Posture Correctors", "url": "#", "image": "/static/images/ad2.jpg"},
        ],
        "videos": [
            {"title": "Stretching Exercises", "url": "https://www.youtube.com/embed/example1"},
            {"title": "Back Pain Relief", "url": "https://www.youtube.com/embed/example2"},
        ],
        "calendar": calendar_data
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
    # Намираме темата по ID
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        abort(404, description="Topic not found")

    # Извличаме данните от формата
    data = request.get_json()
    name = data.get("name", "Anonymous")
    message = data.get("message")

    # Проверяваме дали има съобщение
    if not message:
        return jsonify({"success": False, "error": "Message is required"}), 400

    # Генерираме ID за новата публикация
    new_post_id = max([p["id"] for p in topic["posts"]], default=0) + 1
    new_post = {"id": new_post_id, "name": name, "message": message, "replies": []}

    # Добавяме новата публикация към темата
    topic["posts"].append(new_post)

    # Пренасочваме към страницата на темата
    return redirect(f"/forum/topic/{topic_id}")

# API за добавяне на коментари
@app.route("/api/add-comment/<int:topic_id>", methods=["POST"])
def add_comment(topic_id):
    # Проверяваме дали заявката е JSON
    if not request.is_json:
        return jsonify({"success": False, "error": "Request must be JSON"}), 415

    # Извличаме данните от заявката
    data = request.get_json()
    author = data.get("name", "Anonymous")
    comment_text = data.get("comment")

    # Проверяваме дали коментарът е празен
    if not comment_text:
        return jsonify({"success": False, "error": "Comment text is required"}), 400

    # Намираме темата по ID
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return jsonify({"success": False, "error": "Topic not found"}), 404

    # Генерираме ID за новия коментар
    new_comment_id = max([c["id"] for c in topic["comments"]], default=0) + 1
    new_comment = {"id": new_comment_id, "author": author, "text": comment_text}

    # Добавяме новия коментар към темата
    topic["comments"].append(new_comment)

    # Връщаме успешен отговор
    return jsonify({"success": True, "comment": new_comment})

# API за изтриване на публикация
@app.route("/api/delete-post/<int:topic_id>/<int:post_id>", methods=["DELETE"])
def delete_post(topic_id, post_id):
    # Намираме темата по ID
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return jsonify({"success": False, "error": "Topic not found"}), 404

    # Намираме публикацията по ID
    post = next((p for p in topic["posts"] if p["id"] == post_id), None)
    if not post:
        return jsonify({"success": False, "error": "Post not found"}), 404

    # Премахваме публикацията от списъка
    topic["posts"].remove(post)

    return jsonify({"success": True})


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
