from fastapi import FastAPI
from views import router  # імпортуємо router з views.py

app = FastAPI()

app.include_router(router)