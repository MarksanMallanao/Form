from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

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
.question { display:none; }
.question.active { display:block; }
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
#countdown { font-size:20px; color:#ff1f4d; }
#secret {
 display:none;
 background:#fff0f5;
 padding:18px;
 border-radius:18px;
 color:#ff1f4d;
 max-width:500px;
 margin:20px auto;
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

MUSIC = """
<audio id="bgm" autoplay loop>
 <source src="/static/music/love.mp3" type="audio/mpeg">
</audio>
<script>
document.addEventListener("DOMContentLoaded",()=>{
 let a=document.getElementById("bgm");
 a.volume=0;
 let v=0;
 let fade=setInterval(()=>{
  if(v<0.6){ v+=0.02; a.volume=v; }
  else clearInterval(fade);
 },200);
});
</script>
"""

# ================= SAVE =================
def save_answers(data):
 with open("valentine_answers.txt","a",encoding="utf-8") as f:
  f.write("\n"+"="*45+"\n")
  f.write(f"Submitted: {datetime.now()}\n")
  for k,v in data.items():
   f.write(f"{k}: {v}\n")

# ================= PAGE 1 =================
PAGE1 = """
<!DOCTYPE html><html><head><title>Welcome</title>""" + STYLE + """</head>
<body>""" + MUSIC + HEARTS + """
<h1>Hello Pretty lady, Jaja 💕</h1>
<p>This is a survey. Please answer honestly 💖</p>
<img src="/static/images/heart.png" width="180"><br><br>

<form method="post" action="/page2">
<input name="name" placeholder="Your full name" required><br><br>
<input name="age" type="number" placeholder="Ideal age for marriage" required><br><br>
<button>Start ➡️</button>
</form>
</body></html>
"""

# ================= PAGE 2 =================
PAGE2 = """
<!DOCTYPE html><html><head><title>Survey</title>""" + STYLE + """
<script>
let q=0;
function next(name,val){
 document.getElementsByName(name)[0].value=val;

 let msg="";
 if(document.getElementsByName('q1')[0].value=='Coffee' &&
    document.getElementsByName('q2')[0].value=='Sunset'){
  msg="You’re a quiet romantic soul 🌅☕";
 }
 if(document.getElementsByName('q21')[0].value=='Gamer'){
  msg="Late-night talks and games? I like that 🎮";
 }
 if(document.getElementsByName('q23')[0].value=='Jollibee'){
  msg="Certified Filipino sweetheart 🇵🇭💖";
 }
 if(msg!=""){
  let s=document.getElementById('secret');
  s.innerHTML="💌 Secret Message 💌<br><br>"+msg;
  s.style.display='block';
 }

 document.querySelectorAll('.question')[q].classList.remove('active');
 q++;
 document.querySelectorAll('.question')[q].classList.add('active');
}

function countdown(){
 let t=new Date("February 14, 2026").getTime();
 setInterval(()=>{
  let d=t-new Date().getTime();
  document.getElementById("countdown").innerHTML=
   Math.floor(d/86400000)+" days "+
   Math.floor((d/3600000)%24)+"h "+
   Math.floor((d/60000)%60)+"m "+
   Math.floor((d/1000)%60)+"s 💘";
 },1000);
}
</script>
</head>

<body onload="countdown()">""" + MUSIC + HEARTS + """
<h1>Hello pretty lady, {{ name }} 💖</h1>
<p id="countdown"></p>

<div id="secret"></div>

<form method="post" action="/page3">
<input type="hidden" name="name" value="{{ name }}">
<input type="hidden" name="age" value="{{ age }}">
""" + "".join([f'<input type="hidden" name="q{i}">' for i in range(1,25)]) + """

""" + "".join([
f"""
<div class="question{' active' if i==1 else ''}">
<h3>{q}</h3>
<button type="button" onclick="next('q{i}','{a}')">{a}</button>
<button type="button" onclick="next('q{i}','{b}')">{b}</button>
</div>
""" for i,(q,a,b) in enumerate([
("Coffee or Tea?","Coffee","Tea"),
("Sunrise or Sunset?","Sunrise","Sunset"),
("Sweet or Savory?","Sweet","Savory"),
("Beach or Mountain?","Beach","Mountain"),
("Early bird or Night owl?","Early bird","Night owl"),
("Books or Movies?","Books","Movies"),
("Cats or Dogs?","Cats","Dogs"),
("Dressing up or Cozy?","Dressing up","Cozy"),
("Texting or Calling?","Texting","Calling"),
("Spontaneous or Planned?","Spontaneous","Planned"),
("Summer or Winter?","Summer","Winter"),
("Pizza or Burger?","Pizza","Burger"),
("City life or Small town?","City","Small town"),
("Singing or Dancing?","Singing","Dancing"),
("Netflix binge or One movie?","Binge","One movie"),
("Morning or Night showers?","Morning","Night"),
("Heels or Sneakers?","Heels","Sneakers"),
("Instagram or TikTok?","Instagram","TikTok"),
("Adventure or Relaxing getaway?","Adventure","Relaxing"),
("Homemade meals or Eating out?","Homemade","Eating out"),
("Gamer or Sporty?","Gamer","Sporty"),
("Rose or Sunflower?","Rose","Sunflower"),
("McDo or Jollibee?","McDo","Jollibee"),
("Cookies & Cream or Vanilla?","Cookies & Cream","Vanilla"),
], start=1)
]) + """

<div class="question"><button>Next ➡️</button></div>
</form></body></html>
"""

# ================= PAGE 3 =================
PAGE3 = """
<!DOCTYPE html><html><head><title>Valentine</title>""" + STYLE + """
<script>
function run(btn){
 btn.style.position='absolute';
 btn.style.left=Math.random()*80+'%';
 btn.style.top=Math.random()*80+'%';
}
</script></head>
<body>""" + MUSIC + HEARTS + """
<h1>Will you be my Valentine this Feb 14? ❤️</h1>
<form method="post" action="/result">
""" + "".join([f'<input type="hidden" name="q{i}" value="{{{{ q{i} }}}}">' for i in range(1,25)]) + """
<input type="hidden" name="name" value="{{ name }}">
<button name="valentine" value="YES ❤️">YES ❤️</button>
<button type="button" onmouseover="run(this)">NO 😳</button>
</form></body></html>
"""

# ================= RESULT =================
RESULT = """
<!DOCTYPE html><html><head><title>For You</title>""" + STYLE + """</head>
<body>""" + HEARTS + """
<h1>Thank you, Jaja 💕</h1>
<p style="max-width:600px;margin:auto;font-size:18px;">
I didn’t make this just for fun.<br><br>
I made this because I really want to spend my life with you —<br>
Your humor, your vibe, the whole Jezreen Anzea Belo thing.<br><br>
No pressure, no rush.<br>
I just wanted you to know 💖
</p>
<h2 style="color:#ff4d6d;margin-top:30px;">
Your answer: {{ valentine }}
</h2>
</body></html>
"""

# ================= ROUTES =================
@app.route("/")
def home(): return render_template_string(PAGE1)

@app.route("/page2",methods=["POST"])
def page2():
 return render_template_string(PAGE2,name=request.form["name"],age=request.form["age"])

@app.route("/page3",methods=["POST"])
def page3():
 return render_template_string(PAGE3,**request.form)

@app.route("/result",methods=["POST"])
def result():
 save_answers(dict(request.form))
 return render_template_string(RESULT,name=request.form["name"],valentine=request.form.get("valentine"))

@app.route("/admin")
def admin():
 try:
  with open("valentine_answers.txt","r",encoding="utf-8") as f:
   return "<pre>"+f.read()+"</pre>"
 except:
  return "No answers yet."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

