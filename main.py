from fastapi import FastAPI
import uvicorn
import settings
from api.routers import PrecentRouter


routers = [PrecentRouter]

app = FastAPI(root_path="/api")

for router in routers:
    app.include_router(router().create_router())


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True
    )