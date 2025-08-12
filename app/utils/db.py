"""
app/utils/db.py

Utility functions for database interactions.
"""

import redis.asyncio as redis

from app.config import Config


def get_redis_client():
    """
    Get a Redis client instance.

    Returns:
        redis.Redis: An instance of the Redis client.
    """
    if Config.DB_USER and Config.DB_PORT:
        return redis.Redis(
            host=str(Config.DB_HOST),
            port=int(Config.DB_PORT),
            username=str(Config.DB_USER),
            password=str(Config.DB_PASS),
            decode_responses=True,
        )

    # connect without username and password
    return redis.Redis(host=Config.DB_HOST, port=Config.DB_PORT, decode_responses=True)
