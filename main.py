from fastapi import FastAPI
from views import router, router_user, router_ad  # імпортуємо router з views.py

app = FastAPI()

app.include_router(router, tags=["Locations"])
app.include_router(router_user, tags=["Users"])
app.include_router(router_ad, tags=["Advertisements"])
