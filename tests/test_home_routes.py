from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.home import home_routes

appT = FastAPI()


client = TestClient(appT)

appT.include_router(home_routes.router)


def test_health_check():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0.0"}
    