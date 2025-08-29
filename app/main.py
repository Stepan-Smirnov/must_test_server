import logging

import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

app = FastAPI()

app.include_router(router=main_router)


if __name__ == "__main__":
    uvicorn.run(app=app)