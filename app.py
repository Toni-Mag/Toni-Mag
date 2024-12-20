from flask import Flask, render_template

app = Flask(__name__)

# Начална страница
@app.route("/")
def home():
    return render_template("home.html")

# Страница за проблеми с кръста
@app.route("/back-pain")
def back_pain():
    return render_template("back_pain.html")

# Страница за уреди за упражнения
@app.route("/exercise-tools")
def exercise_tools():
    return render_template("exercise_tools.html")

# Страница за козметични продукти
@app.route("/cosmetic-products")
def cosmetic_products():
    return render_template("cosmetic_products.html")

if __name__ == "__main__":
    app.run(debug=True)
