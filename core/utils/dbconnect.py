import asyncpg.connection
import random


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_recipe(self, name, picture, description, link):
        query = f"INSERT INTO recipes (recipe_name, recipe_picture, recipe_description, recipe_link) " \
                f"VALUES ('{name}', '{picture}', '{description}', '{link}')"

        await self.connector.execute(query)

    async def get_random_recipe(self):
        # Get total amount or rows in the db, then we choose a random row.
        db_rows = await self.connector.fetchval('SELECT COUNT(recipe_id) FROM recipes')
        random_row_id = random.randint(1, db_rows)

        # Get SELECT query with a given random row
        data_query = f"SELECT recipe_name, recipe_picture, recipe_description, recipe_link " \
                     f"FROM recipes WHERE recipe_id = {random_row_id}"
        result = await self.connector.fetchrow(data_query)

        # Extracting data
        name = result.get('recipe_name')
        picture = result.get('recipe_picture')
        description = result.get('recipe_description')
        link = result.get('recipe_link')
        sep = '\r\n-----\r\n'
        caption = f'{name}{sep}{description}{sep}' \
                  f'<b>Would you like to cook this recipe or we will look for another one?</b>'

        recipe = {'recipe_name': name,
                  'recipe_picture': picture,
                  'recipe_description': description,
                  'recipe_link': link,
                  'recipe_caption': caption
                  }

        return recipe
