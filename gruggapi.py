from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from gruggbot import Grugg


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


GRUGG = Grugg.load_from_disk()
ASK_GRUG = """
<!DOCTYPE html>
<html>
<head>
<title>ask gruggbot</title>
<style>
input {
  padding: 10px;
}
input[type=text] {
  width: 80vw;
}
.answer {
  width: 75vw;
  text-align: left;
}
#grug {
  height: 40vh;
}
</style>
</head>
<body>
<center>
<img id="grug" src="static/grug.png">
<form action="/is_asked" method="GET">
<input type="text" name="q" placeholder="What learns do you want from GruggBot?">
<input type="submit" value="ask">
</form>
"""

ANSWER = """
<h1 class="question">%s</h1>
<p class="answer">%s</p>
"""


@app.get("/", response_class=HTMLResponse)
def ask_grug() -> str:
    return ASK_GRUG


@app.get("/is_asked", response_class=HTMLResponse)
def is_asked(q: str) -> str:
    return ASK_GRUG + ANSWER % (q, GRUGG.is_asked(q))