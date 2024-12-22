from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Страници на сайта
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/back-pain")
def back_pain():
    return render_template("back_pain.html")

@app.route("/exercise-tools")
def exercise_tools():
    return render_template("exercise_tools.html")

@app.route("/cosmetic-products")
def cosmetic_products():
    return render_template("cosmetic_products.html")

@app.route("/maria_story")
def maria_story():
    return render_template("maria_story.html")

# Форум
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

@app.route("/forum")
def forum():
    return render_template("forum.html", topics=forum_topics)

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return "Topic not found", 404
    return render_template("topic.html", topic=topic)

@app.route("/add-topic", methods=["POST"])
def add_topic():
    title = request.form.get("title")
    if not title:
        return "Title is required", 400
    new_topic = {"id": len(forum_topics) + 1, "title": title, "posts": []}
    forum_topics.append(new_topic)
    return redirect("/forum")

@app.route("/add-post/<int:topic_id>", methods=["POST"])
def add_post(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return "Topic not found", 404
    name = request.form.get("name")
    message = request.form.get("message")
    if not (name and message):
        return "Name and message are required", 400
    new_post = {"id": len(topic["posts"]) + 1, "name": name, "message": message, "replies": []}
    topic["posts"].append(new_post)
    return redirect(f"/topic/{topic_id}")

@app.route("/reply/<int:topic_id>/<int:post_id>", methods=["POST"])
def reply(topic_id, post_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return "Topic not found", 404
    post = next((p for p in topic["posts"] if p["id"] == post_id), None)
    if not post:
        return "Post not found", 404
    reply_name = request.form.get("name")
    reply_message = request.form.get("message")
    if not (reply_name and reply_message):
        return "Name and message are required", 400
    post["replies"].append({"name": reply_name, "message": reply_message})
    return redirect(f"/topic/{topic_id}")

if __name__ == "__main__":
    app.run(debug=True)
