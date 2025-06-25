
from fastapi import FastAPI
from views import router_location, router_user, router_ad, router_login, router_r  # імпортуємо router з views.py

app = FastAPI()

app.include_router(router_location, tags=["Locations"])
app.include_router(router_user, tags=["Users"])
app.include_router(router_ad, tags=["Advertisements"])
app.include_router(router_login, tags=["Users"])
app.include_router(router_r, tags=["Users"])
