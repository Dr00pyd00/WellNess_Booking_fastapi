from app.core.database import LocalSession


# si sync: 
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
# si async:
    # comme pour ouvrir un fichier text par exemple avec with: le with va fermer correctement:
async def async_get_db():
    async with LocalSession() as db:
        yield db 


