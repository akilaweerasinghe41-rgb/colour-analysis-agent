from flask import Flask, request, redirect
from collections import Counter
import json
import os

app = Flask(__name__)

FILE = "results.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

results = load_data()

def get_colour(n):
    if n in [1, 3, 7, 9]:
        return "Green"
    elif n in [2, 4, 6, 8]:
        return "Red"
    return "Violet"

@app.route("/", methods=["GET", "POST"])
def dashboard():
    global results

    if request.method == "POST":
        issue = request.form["issue"]
        number = int(request.form["number"])

        if 0 <= number <= 9:
            results.append({
                "issue": issue,
                "number": number
            })

            with open(FILE, "w") as f:
                json.dump(results, f)

        return redirect("/")

    numbers = [x["number"] for x in results]

    colours = Counter(get_colour(n) for n in numbers)
    sizes = Counter(
        "Big" if n >= 5 else "Small"
        for n in numbers
    )

    total = len(numbers)

    def percent(value):
        return round(value / total * 100, 1) if total else 0

    html = """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Colour Agent</title>
    <style>
    body {
        background:#101827;
        color:white;
        font-family:Arial;
        padding:20px
    }
    .box {
        background:#1e293b;
        padding:15px;
        margin:12px 0;
        border-radius:12px
    }
    input,button {
        padding:12px;
        margin:5px;
        width:90%;
        border-radius:7px
    }
    button {
        background:#16a34a;
        color:white;
        border:0
    }
    </style>
    </head>
    <body>
    <h2>AI COLOUR AGENT</h2>
