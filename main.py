from fastapi import FastAPI, Request
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql.expression import func
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
engine = create_engine('sqlite:///quotes.db', echo=True)
conn = engine.connect()
meta = MetaData()

quotes = Table(
    'quotes', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('quote', String),
    Column('author', String),
)


class Quote(BaseModel):
    id: int
    quote: str
    author: str


def get_random_quote(request: Request = None):
    q = quotes.select().order_by(func.random())
    result = conn.execute(q)
    rows = result.fetchone()
    if request is None:
        return {"ID": rows[0], "Quote": rows[1], "Author": rows[2]}
    else:
        return {"request": request, "ID": rows[0], "Quote": rows[1], "Author": rows[2]}


def get_quote_by_id(quote_id: int):
    q = quotes.select().where(quotes.c.id == quote_id)
    result = conn.execute(q)
    rows = result.fetchone()
    if rows:
        return {"ID": rows[0], "Quote": rows[1], "Author": rows[2]}
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
