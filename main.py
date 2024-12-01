from fastapi import FastAPI
import uvicorn
import settings
from api import PercentRouter
from management import StartUpCommands

routers = [PercentRouter]

app = FastAPI(root_path="/api")

for router in routers:
    app.include_router(router().create_router())


@app.on_event("startup")
async def startup():
    commands = StartUpCommands()
    await commands.init_database()


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True
    )
