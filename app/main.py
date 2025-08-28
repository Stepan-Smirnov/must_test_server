import uvicorn
from fastapi import FastAPI


app = FastAPI(summary="Тестовое", description="123123")


if __name__ == "__main__":
    uvicorn.run(app=app)