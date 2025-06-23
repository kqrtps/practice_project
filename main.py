from fastapi import FastAPI
from views import router , router_user # імпортуємо router з views.py

app = FastAPI()

app.include_router(router)
app.include_router(router_user)