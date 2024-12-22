from flask import Flask, render_template

app = Flask(__name__)

@app.route("/maria_story")
def maria_story():
    return render_template("maria_story.html")


# Функция за обновяване на броя на посетителите
def update_database():
    try:
        # Четене и обновяване на броя
        with open("visitor_count.txt", "r+") as file:
            count = int(file.read())
            count += 1
            file.seek(0)
            file.write(str(count))
            file.truncate()
        return count
    except FileNotFoundError:
        # Ако файлът липсва, създаваме нов
        with open("visitor_count.txt", "w") as file:
            file.write("1")
        return 1

# Начална страница
@app.route("/")
def home():
    visitor_count = update_database()
    return render_template("home.html", count=visitor_count)

# Продукти
@app.route("/products")
def products():
    return render_template("products.html")

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
