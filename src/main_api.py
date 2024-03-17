from fastapi import FastAPI
from src.infrastructure import controllers
from src.logger_config import setup_global_logger


setup_global_logger()
app = FastAPI()
app.include_router(controllers.router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World"}
