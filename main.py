from fastapi import FastAPI, Request
import sqlite3
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
with sqlite3.connect("quotes.db") as connection:
    cursor = connection.cursor()


def get_random_quote(request=None):
    rows = cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;").fetchall()
    if request is None:
        return {"Quote": rows[0][0], "Author": rows[0][1]}
    else:
        return {"request": request, "Quote": rows[0][0], "Author": rows[0][1]}



@app.get("/quote")
async def root():
    return get_random_quote()


@app.get("/")
async def name(request: Request):
    return templates.TemplateResponse("base.html", get_random_quote(request))
