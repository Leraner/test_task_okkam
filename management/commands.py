import asyncio
import io
from datetime import datetime

import pandas as pd

from database.db import Database
from database.schemas import CreateRespondentModelSchema


class StartUpCommands:
    database: Database = Database()

    async def init_database(self):
        if await self.database.check_table_empty():
            return

        with open("database_dump/data 1.csv", "rb") as file:
            contents = file.read()

        def chunk_csv_pandas(file: bytes, chunk_size: int):
            """Reads a CSV file in chunks using pandas."""
            reader = pd.read_csv(io.StringIO(file.decode()), chunksize=chunk_size)
            for chunk in reader:
                yield chunk

        tasks = []

        for chunk in chunk_csv_pandas(file=contents, chunk_size=100):
            object_to_create = []
            for data in chunk.to_numpy():
                data_element = data[0].split(";")
                data_element[1] = datetime.strptime(data_element[1], "%Y%m%d").date()
                object_to_create.append(
                    CreateRespondentModelSchema(
                        id=int(data_element[0]),
                        date=data_element[1],
                        respondent=data_element[2],
                        sex=data_element[3],
                        age=data_element[4],
                        weight=data_element[5],
                    )
                )

            tasks.append(self.database.insert_database_data(instances=object_to_create))

        await asyncio.gather(*tasks)
