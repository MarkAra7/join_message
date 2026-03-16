import aiomysql
from contextlib import asynccontextmanager
import datetime
from datetime import timedelta
import json, os

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

DB_HOST = config.get('DB_HOST')
DB_PORT = config.get('DB_PORT')
DB_USER = config.get('DB_USER')
DB_PASSWORD = config.get('DB_PASSWORD')
DB_NAME = config.get('DB_NAME')


MYSQL_CONFIG = {
    'host': DB_HOST, 
    'port': DB_PORT,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'db': DB_NAME,
    'charset': 'utf8mb4',
    'autocommit': True
}
@asynccontextmanager
async def get_db():
    pool = await aiomysql.create_pool(**MYSQL_CONFIG, minsize=1, maxsize=10)
    try:
        yield pool
    finally:
        pool.close()
        await pool.wait_closed()



#region Player DB Functions
async def player_exists(player_discord_id: str):
    """Returns True if player exists in DB"""
    async with get_db() as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1 FROM Player WHERE player_id = %s LIMIT 1", (player_discord_id,))
                return await cur.fetchone() is not None

async def create_player(player_discord_id: str):
    """Creates a new player in the DB"""
    async with get_db() as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO Player (player_id) VALUES (%s)", (player_discord_id,))