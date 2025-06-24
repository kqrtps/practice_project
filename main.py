from fastapi import FastAPI
from views import router, router_user, router_ad , router_login  # імпортуємо router з views.py

app = FastAPI()

app.include_router(router, tags=["Locations"])
app.include_router(router_user, tags=["Users"])
app.include_router(router_ad, tags=["Advertisements"])
app.include_router(router_login, tags=["Users"])