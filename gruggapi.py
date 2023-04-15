import typing as t

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
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
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/static/grug.css">
</head>
<body>
<center>
<img id="grug" src="static/grug.png">
<form action="/" method="GET">
<div class="flex-full-horiz">
<input type="text" name="q" placeholder="What learns do you want from GruggBot?">
<input type="submit" value="ask">
</div>
</form>
"""

ANSWER = """
<h1 class="question">%s</h1>
<p>%s</p>
"""

WHO = """
  grug brain developer not so smart, but grug brain developer program many long
  year and learn some things although mostly still confused.
</p><p>
  gruggbot is ai language model with embedding trained on
  <a href="https://grugbrain.dev">grugbrain.dev</a>.
  now young grugs everywhere can ask question, and grug might be able to help,
  although maybe get confused more.
"""


@app.get("/", response_class=HTMLResponse)
def ask_grug(q: t.Optional[str] = None) -> str:
    if q is not None:
        if q:
            return ASK_GRUG + ANSWER % (q, GRUGG.is_asked(q))
        else:
            # form submit, but no query entered
            return RedirectResponse("/who")
    return ASK_GRUG


@app.get("/who", response_class=HTMLResponse)
def who_grug() -> str:
  return ASK_GRUG + ANSWER % ("who grug?", WHO)