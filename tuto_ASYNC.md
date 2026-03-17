
# Async method for FASTAPI

Il faut changer des choses pour que une fonction async fonctionne.

| Sync      | async      |
| --------- | ---------- |
| def       | async def  |
| Session   | AsyncSession |
| db.query(User).filter() | await db.exectute(select(User).where()) |
| db.commit() | await db.commit()

