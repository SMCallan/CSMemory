from flask import Flask, render_template, jsonify, request

import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset_game", methods=["POST"])
def reset_game():
    # You would set up and reset your game here
    # This example just sends back random board values
    grid_size = request.json.get("grid_size", 4)
    max_num = (grid_size * grid_size) // 2
    numbers = [i for i in range(1, max_num + 1)] * 2
    random.shuffle(numbers)
    board = [[numbers.pop() for _ in range(grid_size)] for _ in range(grid_size)]
    return jsonify({"board": board, "score": 0})

if __name__ == "__main__":
    app.run(debug=True)
