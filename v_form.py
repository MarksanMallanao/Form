from flask import Flask, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

# ================= SAVE ANSWERS =================
def save_answers(data):
    with open("valentine_answers.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "="*50 + "\n")
        f.write(f"Submitted: {datetime.now()}\n")
        for k, v in data.items():
            f.write(f"{k}: {v}\n")

# ================= STYLE =================
STYLE = """
<style>
body {
 font-family: Arial;
 background: linear-gradient(#ffe6ea, #fff0f5);
 text-align: center;
}
button {
 background:#ff4d6d;
 color:white;
 padding:12px 25px;
 border:none;
 border-radius:25px;
 font-size:16px;
 cursor:pointer;
 margin:8px;
}
button:hover { background:#ff1f4d; }
input {
 padding:10px;
 border-radius:15px;
 border:1px solid #ccc;
}
.heart {
 position:fixed;
 bottom:-40px;
 font-size:26px;
 animation:float 6s infinite;
}
@keyframes float {
 0% { transform:translateY(0); opacity:1; }
 100% { transform:translateY(-900px); opacity:0; }
}
</style>
"""

HEARTS = """
<div class="heart" style="left:10%">❤️</div>
<div class="heart" style="left:30%">💖</div>
<div class="heart" style="left:50%">💕</div>
<div class="heart" style="left:70%">💘</div>
<div class="heart" style="left:90%">💗</div>
"""

# ================= PAGE 1 =================
PAGE1 = """
<!DOCTYPE html>
<html>
<head><title>Hello</title>""" + STYLE + """</head>
<body>""" + HEARTS + """
<h1>Hello pretty lady 💕</h1>
<p>This is a survey. Please answer honestly 💖</p>

<form method="post" action="/survey">
<input name="name" placeholder="Your name" required><br><br>
<input name="age" type="number" placeholder="Your age" required><br><br>
<button>Start ➡️</button>
</form>
</body>
</html>
"""

# ================= PAGE 2 =================
PAGE2 = """
<!DOCTYPE html>
<html>
<head><title>Survey</title>""" + STYLE + """</head>
<body>""" + HEARTS + """
<h2>Answer by clicking 💖</h2>

<form method="post" action="/valentine">
<input type="hidden" name="name" value="{{name}}">
<input type="hidden" name="age" value="{{age}}">

{% for q,a,b in questions %}
<p><b>{{q}}</b></p>
<button type="submit" name="{{q}}" value="{{a}}">{{a}}</button>
<button type="submit" name="{{q}}" value="{{b}}">{{b}}</button>
<br><br>
{% endfor %}

</form>
</body>
</html>
"""

# ================= PAGE 3 =================
PAGE3 = """
<!DOCTYPE html>
<html>
<head><title>Valentine</title>""" + STYLE + """</head>
<body>""" + HEARTS + """
<h1>Will you be my Valentine this Feb 14? ❤️</h1>

<form method="post" action="/result">
{% for k,v in data.items() %}
<input type="hidden" name="{{k}}" value="{{v}}">
{% endfor %}

<button name="valentine" value="YES ❤️">YES ❤️</button>
<button name="valentine" value="NO 😅">NO 😅</button>
</form>
</body>
</html>
"""

# ================= RESULT =================
RESULT = """
<!DOCTYPE html>
<html>
<head><title>Done</title>""" + STYLE + """</head>
<body>""" + HEARTS + """
<h1>Thank you 💕</h1>
<p>Your answer has been saved.</p>
</body>
</html>
"""

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template_string(PAGE1)

@app.route("/survey", methods=["POST"])
def survey():
    questions = [
        ("Coffee or Tea?", "Coffee", "Tea"),
        ("Sunrise or Sunset?", "Sunrise", "Sunset"),
        ("Sweet or Savory?", "Sweet", "Savory"),
        ("Pizza or Burger?", "Pizza", "Burger"),
        ("Gamer or Sporty?", "Gamer", "Sporty"),
        ("Rose or Sunflower?", "Rose", "Sunflower"),
        ("McDo or Jollibee?", "McDo", "Jollibee"),
        ("Cookies & Cream or Vanilla?", "Cookies & Cream", "Vanilla"),
    ]
    return render_template_string(
        PAGE2,
        name=request.form["name"],
        age=request.form["age"],
        questions=questions
    )

@app.route("/valentine", methods=["POST"])
def valentine():
    return render_template_string(PAGE3, data=request.form)

@app.route("/result", methods=["POST"])
def result():
    save_answers(dict(request.form))
    return render_template_string(RESULT)

# ================= SECRET ADMIN PAGE =================
@app.route("/admin-jaja-0214")
def admin():
    try:
        with open("valentine_answers.txt", "r", encoding="utf-8") as f:
            content = f.read().replace("\n", "<br>")
    except:
        content = "No responses yet 💔"

    return f"""
    <html>
    <head>
        <title>Secret Admin 💖</title>
        <style>
            body {{
                font-family: Arial;
                background: #fff0f5;
                padding: 30px;
            }}
            .box {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                max-width: 700px;
                margin: auto;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>💌 Valentine Responses</h2>
            {content}
        </div>
    </body>
    </html>
    """

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
