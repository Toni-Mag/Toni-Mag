from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Списък за съхранение на темите във форума
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

def find_topic_by_id(topic_id):
    """Намира тема по ID."""
    for topic in forum_topics:
        if topic["id"] == topic_id:
            return topic
    return None

def find_post_by_id(topic, post_id):
    """Намира пост по ID в дадена тема."""
    for post in topic["posts"]:
        if post["id"] == post_id:
            return post
    return None

def generate_new_id(collection):
    """Генерира ново уникално ID за дадена колекция."""
    return max([item["id"] for item in collection], default=0) + 1

@app.route("/forum")
def forum():
    """Показва страницата на форума със списък от теми."""
    return render_template("forum.html", topics=forum_topics)

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    """Показва постовете в дадена тема."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        return "Topic not found", 404
    return render_template("topic.html", topic=topic)

@app.route("/add-topic", methods=["POST"])
def add_topic():
    """Добавя нова тема към форума."""
    title = request.form.get("title")
    if not title:
        return "Title is required", 400

    new_topic = {
        "id": generate_new_id(forum_topics),
        "title": title,
        "posts": []
    }
    forum_topics.append(new_topic)
    return redirect("/forum")

@app.route("/add-post/<int:topic_id>", methods=["POST"])
def add_post(topic_id):
    """Добавя нов пост в дадена тема."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        return "Topic not found", 404

    name = request.form.get("name")
    message = request.form.get("message")
    if not (name and message):
        return "Name and message are required", 400

    new_post = {
        "id": generate_new_id(topic["posts"]),
        "name": name,
        "message": message,
        "replies": []
    }
    topic["posts"].append(new_post)
    return redirect(f"/topic/{topic_id}")

@app.route("/reply/<int:topic_id>/<int:post_id>", methods=["POST"])
def reply(topic_id, post_id):
    """Добавя отговор към конкретен пост."""
    topic = find_topic_by_id(topic_id)
    if not topic:
        return "Topic not found", 404

    post = find_post_by_id(topic, post_id)
    if not post:
        return "Post not found", 404

    reply_name = request.form.get("name")
    reply_message = request.form.get("message")
    if not (reply_name and reply_message):
        return "Name and message are required", 400

    post["replies"].append({"name": reply_name, "message": reply_message})
    return redirect(f"/topic/{topic_id}")

@app.route("/")
def home():
    """Начална страница."""
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
