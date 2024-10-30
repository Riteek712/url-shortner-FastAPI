import os
import redis

DATABASE_URL = os.getenv("DATABASE_URL", 
    "postgresql://neondb_owner:LYw9Tqhypm4F@ep-misty-field-a5vh0w68.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

# Redis configuration
async def get_redis_connection():
    redis_url = os.getenv("REDIS_URL", "redis://redis-15290.c8.us-east-1-2.ec2.redns.redis-cloud.com:15290")
    redis_password = os.getenv("REDIS_PASSWORD", "######################") # problem with  redis connection wrt to await statements.
    
    return redis.StrictRedis.from_url(redis_url, password=redis_password)