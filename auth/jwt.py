from database import SessionLocal


def get_db(): #crea la conexion
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()