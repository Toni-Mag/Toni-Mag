from flask import Flask, render_template, abort
import calendar
from datetime import datetime
from flask_caching import Cache

# Flask App Configuration
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

# Holiday Data
holidays = [
    {"date": "2025-01-01", "name": "New Year's Day"},
    {"date": "2025-03-17", "name": "St. Patrick's Day"},
    {"date": "2025-05-12", "name": "Mother's Day"},
    {"date": "2025-06-16", "name": "Father's Day"},
    {"date": "2025-12-25", "name": "Christmas Day"}
]

# Forum Data
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

# Utility Functions
@cache.cached(timeout=60)
def generate_calendar(year, month):
    """Generate a calendar with highlighted holidays."""
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    holiday_dates = {
        datetime.strptime(h["date"], "%Y-%m-%d").day: h["name"]
        for h in holidays if datetime.strptime(h["date"], "%Y-%m-%d").month == month
    }
    return month_days, holiday_dates

@cache.cached(timeout=60)
def get_sidebar_content():
    """Generate sidebar content including ads, videos, and calendar."""
    today = datetime.today()
    year, month = today.year, today.month
    month_days, holiday_dates = generate_calendar(year, month)
    month_name = calendar.month_name[month]
    today_date = today.strftime("%A, %B %d, %Y")  # Премахваме "Today:"


    return {
        "ads": [
            {"title": "Health Gadgets", "url": "#", "image": "/static/images/ad1.jpg"},
            {"title": "Posture Correctors", "url": "#", "image": "/static/images/ad2.jpg"}
        ],
        "videos": [
            {"title": "Daily Exercises", "url": "https://www.youtube.com/embed/example1"},
            {"title": "Stress Relief Tips", "url": "https://www.youtube.com/embed/example2"}
        ],
        "calendar": {
            "month_days": month_days,
            "holiday_dates": holiday_dates,
            "month_name": month_name,
            "year": year,
            "today": today_date
        }
    }

def find_topic_by_id(topic_id):
    """Find a forum topic by ID."""
    return next((topic for topic in forum_topics if topic["id"] == topic_id), None)

# Routes
@app.route("/")
def home():
    sidebar_content = get_sidebar_content()
    return render_template("home.html", sidebar=sidebar_content)

@app.route("/back-pain")
def back_pain():
    sidebar_content = get_sidebar_content()
    return render_template("back_pain.html", sidebar=sidebar_content)

@app.route("/exercise-tools")
def exercise_tools():
    sidebar_content = get_sidebar_content()
    return render_template("exercise_tools.html", sidebar=sidebar_content)

@app.route("/cosmetic-products")
def cosmetic_products():
    sidebar_content = get_sidebar_content()
    return render_template("cosmetic_products.html", sidebar=sidebar_content)

@app.route("/products")
def products():
    sidebar_content = get_sidebar_content()
    return render_template("products.html", sidebar=sidebar_content)

@app.route("/maria_story")
def maria_story():
    sidebar_content = get_sidebar_content()
    return render_template("maria_story.html", sidebar=sidebar_content)

@app.route("/forum")
def forum():
    sidebar_content = get_sidebar_content()
    return render_template("forum.html", topics=forum_topics, sidebar=sidebar_content)

@app.route("/forum/topic/<int:topic_id>")
def topic(topic_id):
    topic = find_topic_by_id(topic_id)
    if not topic:
        abort(404, description="Topic not found")
    sidebar_content = get_sidebar_content()
    return render_template("topic.html", topic=topic, sidebar=sidebar_content)

@app.errorhandler(404)
def page_not_found(e):
    sidebar_content = get_sidebar_content()
    return render_template("404.html", error=e, sidebar=sidebar_content), 404

@app.errorhandler(400)
def bad_request(e):
    sidebar_content = get_sidebar_content()
    return render_template("400.html", error=e, sidebar=sidebar_content), 400

# Main Starter
if __name__ == "__main__":
    app.run(debug=True)
