import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO users (user_id, user_name) VALUES ({user_id}, '{user_name}') ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)

    async def show_data(self):
        query = "SELECT * FROM users ORDER BY user_id"
        raw_result = await self.connector.fetch(query)
        result = ''
        for _ in raw_result:
            temp = str(_).replace('Record ', '')[1:-1]
            result += f'{temp},\n'
        return result