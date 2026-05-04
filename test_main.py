from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_read_reservations():
    """Vérifie que la route GET fonctionne"""
    response = client.get("/reservations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_health_check():
    """Un test simple pour vérifier que l'app répond"""
    response = client.get("/reservations")
    assert response.status_code == 200