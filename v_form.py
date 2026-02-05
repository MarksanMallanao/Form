from flask import Flask, request, render_template_string
from datetime import datetime
import os, json, math

app = Flask(__name__)

# ================= SAVE =================
def save_answers(data):
    with open("valentine_answers.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 45 + "\n")
        f.write(f"Submitted: {datetime.now()}\n")
        for k, v in data.items():
            f.write(f"{k}: {v}\n")

# ================= STYLE =================
STYLE = """
<style>
body{
 font-family:Arial;
 background:linear-gradient(#ffe6ea,#fff0f5);
 display:flex;
 justify-content:center;
 align-items:center;
 flex-direction:column;
 min-height:100vh;
 margin:0;
 text-align:center;
 overflow:hidden;
}
button{
 background:#ff4d6d;
 color:white;
 padding:14px 28px;
 border:none;
 border-radius:30px;
 font-size:18px;
 cursor:pointer;
 margin:10px;
}
.question{display:none;}
.question.active{display:block;}
#secret{
 display:none;
 background:#fff0f5;
 padding:18px;
 border-radius:18px;
 color:#ff1f4d;
 max-width:500px;
 margin:20px auto;
}
#bow{
 position:fixed;
 bottom:40px;
 left:50%;
 transform-origin:center bottom;
 font-size:60px;
}
.arrow{position:absolute;font-size:26px;}
.heart{
 position:absolute;
 font-size:24px;
 animation:float 8s linear infinite;
 opacity:0.6;
}
@keyframes float{
 from{bottom:-40px;}
 to{bottom:110%;}
}
</style>
"""

# ================= MUSIC =================
MUSIC = """
<audio id="bgm" loop>
 <source src="/static/music/love.mp3" type="audio/mpeg">
</audio>
<script>
function startMusic(){
 localStorage.setItem("music","on");
 var a=document.getElementById("bgm");
 a.volume=0.6;
 a.play();
}
window.addEventListener("load",function(){
 var a=document.getElementById("bgm");
 if(localStorage.getItem("music")==="on"){
  a.volume=0.6;
  a.play();
 }
});
</script>
"""

# ================= FLOATING HEARTS =================
FLOATING = """
<script>
setInterval(function(){
 var h=document.createElement("div");
 h.className="heart";
 h.innerHTML="💖";
 h.style.left=Math.random()*100+"%";
 h.style.animationDuration=(5+Math.random()*5)+"s";
 document.body.appendChild(h);
 setTimeout(function(){h.remove();},9000);
},800);
</script>
"""

# ================= DATA =================
QUESTIONS = [
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
("Cookies & Cream or Vanilla?","Cookies & Cream","Vanilla")
]

SECRETS = [
"You have a really gentle heart 💕",
"Your choices feel warm and comforting 🌷",
"You seem like someone easy to talk to ☕",
"You give calm, safe, and happy energy 💖",
"I like the way your mind works 😊",
"You’re effortlessly charming ✨",
"You feel genuine, and that’s rare 🌸",
"Every answer makes you more special 💘",
"You have a beautiful way of thinking 💭",
"You feel like someone worth choosing 💗",
"There’s something very sincere about you 🌹",
"You’re exactly the kind of person I admire ❤️"
]

# ================= START =================
PAGE0 = """
<!DOCTYPE html><html><head><title>Start</title>""" + STYLE + """</head>
<body>
<h1>🎯 Ready for a little game?</h1>
<form method="post" action="/game">
<button>Start the Game 💘</button>
</form>
""" + FLOATING + """
</body></html>
"""

# ================= GAME =================
PAGE1 = """
<!DOCTYPE html><html><head><title>Game</title>""" + STYLE + """
<script>
var angle=0, hit=0;

function aim(x,y){
 var bow=document.getElementById("bow");
 var dx=x-window.innerWidth/2;
 var dy=window.innerHeight-y-40;
 angle=Math.atan2(dx,dy);
 bow.style.transform="translateX(-50%) rotate("+ (angle*180/Math.PI) +"deg)";
}

function shoot(){
 var arrow=document.createElement("div");
 arrow.className="arrow";
 arrow.innerHTML="➵";
 var x=window.innerWidth/2, y=90;
 document.body.appendChild(arrow);

 var vx=Math.sin(angle)*12;
 var vy=Math.cos(angle)*12;

 var fly=setInterval(function(){
  x+=vx; y+=vy;
  arrow.style.left=x+"px";
  arrow.style.bottom=y+"px";

  document.querySelectorAll(".heart").forEach(function(h){
   var r=h.getBoundingClientRect();
   if(Math.abs(r.left+r.width/2-x)<20){
    h.remove(); arrow.remove(); clearInterval(fly);
    hit++; if(hit>=3){document.getElementById("go").submit();}
   }
  });
 },20);
}

function spawn(){
 var h=document.createElement("div");
 h.className="heart";
 h.innerHTML="💖";
 h.style.left=Math.random()*90+"%";
 h.style.bottom="-40px";
 document.body.appendChild(h);
}

window.onload=function(){
 for(var i=0;i<5;i++){spawn();}
 setInterval(spawn,1200);
 document.addEventListener("mousemove",function(e){aim(e.clientX,e.clientY);});
 document.addEventListener("mouseup",shoot);
};
</script>
</head>
<body>
<h1>Aim & release 💘</h1>
<p>Hit 3 hearts to continue</p>
<div id="bow">🏹</div>
<form id="go" method="post" action="/intro"></form>
""" + FLOATING + """
</body></html>
"""

# ================= INTRO =================
PAGE2 = """
<!DOCTYPE html><html><head><title>Intro</title>""" + STYLE + """</head>
<body>
<h1>This is a survey 💌</h1>
<p>Answer it honestly 💖</p>
<form method="post" action="/survey">
<button>Proceed ➡️</button>
</form>
""" + FLOATING + """
</body></html>
"""

# ================= SURVEY =================
PAGE3 = """
<!DOCTYPE html><html><head><title>Survey</title>""" + STYLE + """
<script>
var q=0;
var questions=[];
var SECRETS=""" + json.dumps(SECRETS) + """;

window.onload=function(){
 questions=document.querySelectorAll(".question");
 questions[0].classList.add("active");
 startMusic();
};

function next(name,value){
 document.getElementsByName(name)[0].value=value;
 if((q+1)%2===0){
  var s=document.getElementById("secret");
  s.innerHTML="💌 Secret Message 💌<br><br>"+SECRETS[Math.floor(q/2)];
  s.style.display="block";
 }
 questions[q].classList.remove("active");
 q++;
 if(q<questions.length){questions[q].classList.add("active");}
 else{document.getElementById("surveyForm").submit();}
}
</script>
</head>
<body>
""" + MUSIC + """
<h1>Hello Pretty lady, Jaja 💕</h1>
<div id="secret"></div>
<form id="surveyForm" method="post" action="/valentine">
""" + "".join([f'<input type="hidden" name="q{i}">' for i in range(1,25)]) + """
""" + "".join(
f"""
<div class="question">
<h3>{q}</h3>
<button type="button" onclick="next('q{i}','{a}')">{a}</button>
<button type="button" onclick="next('q{i}','{b}')">{b}</button>
</div>
""" for i,(q,a,b) in enumerate(QUESTIONS,1)
) + """
</form>
""" + FLOATING + """
</body></html>
"""

# ================= VALENTINE =================
PAGE4 = """
<!DOCTYPE html><html><head><title>Valentine</title>""" + STYLE + """</head>
<body>
""" + MUSIC + """
<h1>Will you be my Valentine and my online date this February 14? ❤️</h1>
<form method="post" action="/result">
{% for k,v in data.items() %}
<input type="hidden" name="{{k}}" value="{{v}}">
{% endfor %}
<button name="valentine" value="YES ❤️">YES ❤️</button>
<button type="button" onmouseover="this.style.left=Math.random()*80+'%'">NO 😳</button>
</form>
""" + FLOATING + """
</body></html>
"""

# ================= RESULT =================
RESULT = """
<!DOCTYPE html><html><head><title>For You</title>""" + STYLE + """</head>
<body>
<h1>Thank you, Jaja 💕</h1>
<p style="max-width:600px;font-size:18px;">
I didn’t make this just for fun.<br><br>
I made this because I want to be with you forever —<br>
Your personality, your vibe — and honestly, everything about you.<br><br>
No pressure, no rush.<br>
I just wanted you to know 💖
</p>
</body></html>
"""

# ================= ROUTES =================
@app.route("/")
def start(): return render_template_string(PAGE0)

@app.route("/game",methods=["POST"])
def game(): return render_template_string(PAGE1)

@app.route("/intro",methods=["POST"])
def intro(): return render_template_string(PAGE2)

@app.route("/survey",methods=["POST"])
def survey(): return render_template_string(PAGE3)

@app.route("/valentine",methods=["POST"])
def valentine(): return render_template_string(PAGE4,data=request.form)

@app.route("/result",methods=["POST"])
def result():
 save_answers(dict(request.form))
 return render_template_string(RESULT)

@app.route("/admin-jaja-0214")
def admin():
 try:
  with open("valentine_answers.txt","r",encoding="utf-8") as f:
   return "<pre>"+f.read()+"</pre>"
 except:
  return "No responses yet."

# ================= RUN =================
if __name__=="__main__":
 port=int(os.environ.get("PORT",10000))
 app.run(host="0.0.0.0",port=port)
