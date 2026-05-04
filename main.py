from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configuration CORS pour que ton Next.js puisse parler au Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # L'URL de ton front Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Notre "base de données" en mémoire (une simple liste)
# Attention : si tu redémarres le serveur, cette liste se vide.
db_reservations = []

class Reservation(BaseModel):
    event_id: str

@app.get("/reservations")
def get_all_reservations():
    """Récupère tous les IDs réservés"""
    return db_reservations

@app.post("/reservations")
def add_reservation(res: Reservation):
    """Ajoute un ID à la liste s'il n'y est pas déjà"""
    if res.event_id not in db_reservations:
        db_reservations.append(res.event_id)
        return {"status": "success", "added": res.event_id}
    return {"status": "already_exists"}

@app.delete("/reservations/{event_id}")
def remove_reservation(event_id: str):
    """Supprime un ID de la liste"""
    if event_id in db_reservations:
        db_reservations.remove(event_id)
        return {"status": "removed"}
    return {"status": "not_found"}