import redis
import requests

from fastapi import FastAPI, Header, HTTPException
from pymongo import MongoClient
from starlette.responses import JSONResponse

from auth import Auth
from joke import Joke
from config import Config

from rate_limiter.rate_limiter import RateLimiter

mongo_client = MongoClient(Config.MONGODB_CONN_STR)
redis_client = redis.Redis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD
)
rate_limiter = RateLimiter(mongo_client=mongo_client, redis_client=redis_client)


app = FastAPI()


@app.exception_handler(HTTPException)
async def rate_limit_exception_handler(request, exc):
    if exc.status_code == 429:  # Rate limit exceeded
        return JSONResponse(
            content={"message": "Request rate limit exceeded"},
            status_code=exc.status_code,
        )
    return exc


@app.get("/joke")
async def root(authorization: str = Header(None)):
    if rate_limiter.limit_exceeded(authorization):
        # maybe we can add which type of rate limit exceeded here
        raise HTTPException(status_code=429)  # Rate limit exceeded

    response = requests.get("https://api.chucknorris.io/jokes/random").json()
    Joke.from_dict(response)
    return Joke.from_dict(response)


app.add_middleware(Auth)
