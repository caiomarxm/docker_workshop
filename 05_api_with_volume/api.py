import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List


DATABASE_FILE = './db/db.json'


class MovieQuote(BaseModel):
    id: Optional[int] = None
    movie_title: str
    quote: str
    is_active: bool = True


with open(DATABASE_FILE, 'r') as file:
    data = json.load(file)
    db = [MovieQuote(**entry) for entry in data]


def persist_db(db: List[MovieQuote]):
    with open(DATABASE_FILE, 'w') as file:
        db_dict = [entry.model_dump() for entry in db]
        json.dump(db_dict, file)


app = FastAPI()


@app.get('/')
def read_movie_quotes(
    filter_inactive: bool = True
):
    if filter_inactive:
        return [quote for quote in db if quote.is_active]
    return db


@app.get('/{id_}')
def read_movie_quote_by_id(
    id_: int
):
    if len(db) >= id_:
        return db[id_-1]

    raise HTTPException(
        status_code=404,
        detail=f"No element with such id"
    )


@app.post('/create')
def create_movie_quote(
    movie_quote: MovieQuote
):
    id_ = len(db) + 1
    movie_quote.id = id_
    db.append(movie_quote)
    persist_db(db)
    return movie_quote


@app.put('/{id_}')
def update_movie_quote(
    id_: int,
    movie_quote: MovieQuote
):
    if not movie_quote.id:
        movie_quote.id = id_

    db[id_-1] = movie_quote
    persist_db(db)

    return movie_quote


@app.delete('/{id_}')
def delete_movie_quote(
    id_: int
):
    if len(db) >= id_:
        db[id_-1].is_active = False
        persist_db(db)
        return 'Deleted'
    raise HTTPException(
        status_code=404,
        detail=f"Element doesn't exist in database"
    )
