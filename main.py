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
        return {"ID": rows[0][0], "Quote": rows[0][1], "Author": rows[0][2]}
    else:
        return {"request": request, "ID": rows[0][0], "Quote": rows[0][1], "Author": rows[0][2]}


def get_quote_by_id(quote_id: int):
    rows = cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchall()
    if rows:
        return {"ID": rows[0][0], "Quote": rows[0][1], "Author": rows[0][2]}
    else:
        return {"error": "No quote found with the given ID"}


# @app.get("/quote")
# async def root():
#     return get_random_quote()


@app.get("/quote")
async def get_quote(id: int = None):
    if id is None:
        return get_random_quote()
    else:
        return get_quote_by_id(id)


@app.get("/")
async def name(request: Request):
    return templates.TemplateResponse("base.html", get_random_quote(request))


print("done")
