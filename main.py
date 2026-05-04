import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Chargement des variables d'environnement (.env)
load_dotenv()

app = FastAPI()

# Configuration CORS pour autoriser ton front Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Récupération de l'URL Neon depuis le .env
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # Connexion à PostgreSQL (Neon nécessite souvent le sslmode=require)
    return psycopg2.connect(DATABASE_URL)

# Création de la table au démarrage du serveur
@app.on_event("startup")
def startup():
    if not DATABASE_URL:
        print("❌ ERREUR : DATABASE_URL non trouvée dans le fichier .env")
        return
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id SERIAL PRIMARY KEY,
            event_id TEXT UNIQUE NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Connecté à Neon : La table 'reservations' est prête.")

class Reservation(BaseModel):
    event_id: str
    event_title: str 

@app.get("/reservations", response_model=List[str])
def get_all_reservations():
    """Récupère tous les IDs réservés depuis Neon"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT event_id FROM reservations;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # On transforme la liste de tuples en liste simple d'IDs
    return [row[0] for row in rows]

@app.post("/reservations")
def add_reservation(res: Reservation):
    """Ajoute un ID dans la base Neon"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO reservations (event_id, event_title) VALUES (%s, %s)", 
            (res.event_id, res.event_title)
        )
        conn.commit()
        return {"status": "success", "added": res.event_id}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return {"status": "already_exists"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
# route DELETE
@app.delete("/reservations/{event_id}")
def remove_reservation(event_id: str):
    """Supprime un ID de la base Neon"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM reservations WHERE event_id = %s", (event_id,))
    deleted_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    
    if deleted_rows > 0:
        return {"status": "removed"}
    return {"status": "not_found"}