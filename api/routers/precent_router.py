import asyncio
import sqlalchemy
from .base.base_router import RegisterRoutes
from database.db import Database
from database.schemas import CreateRespondentModelSchema
from database.exceptions import DatabaseException
from fastapi import UploadFile, HTTPException
from datetime import datetime
import pandas as pd
import io

class PrecentRouter(RegisterRoutes):
    prefix = "/precents"
    tags = ["precents"]

    database: Database

    @classmethod
    async def get_GetPrecent(cls, audience1: str | None = None, audience2: str | None = None):
        try:
            result = await cls.database.get_precent(audience1=audience1, audience2=audience2)
        except sqlalchemy.exc.DBAPIError:
            return {"error": "В первой группе нет респондентов либо указан неверный фильтр в audience"}
        except DatabaseException as e:
            return {"error": e.message}
        return result

    @classmethod
    async def post_init_database(cls, file: UploadFile):
        contents: bytes = await file.read()

        def chunk_csv_pandas(file: bytes, chunk_size: int):
            """Reads a CSV file in chunks using pandas."""
            reader = pd.read_csv(io.StringIO(contents.decode()), chunksize=chunk_size)
            for chunk in reader:
                yield chunk

        tasks = []

        for chunk in chunk_csv_pandas(file=contents, chunk_size=100):
            object_to_create = []
            for data in chunk.to_numpy():
                data_element = data[0].split(';')
                data_element[1] = datetime.strptime(data_element[1], "%Y%m%d").date()
                object_to_create.append(
                    CreateRespondentModelSchema(
                        id=int(data_element[0]),
                        date=data_element[1], 
                        respondent=data_element[2], 
                        sex=data_element[3], 
                        age=data_element[4], 
                        weight=data_element[5]
                    )
                )
            
            tasks.append(cls.database.insert_database_data(instances=object_to_create))
        
        await asyncio.gather(*tasks)

    @classmethod
    async def get_ping(cls):
        return {"success": True}