import os


class Config:
    MONGODB_CONN_STR = os.getenv("DB_CONN_STR", "mongodb://localhost:27017/")
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")
