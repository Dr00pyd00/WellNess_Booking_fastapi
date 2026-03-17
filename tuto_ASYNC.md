
# Async method for FASTAPI

Il faut changer des choses pour que une fonction async fonctionne.

| Sync      | async      |
| --------- | ---------- |
| def       | async def  |
| Session   | AsyncSession |
| db.query(User).filter() | await db.exectute(select(User).where()) |
| db.commit() | await db.commit()


--- 

ATTENTION :

```python 
res = await db.execute(select(func.count(User)).where(User.role == RoleEnum.ADMIN))
admin_count = res.scalar()
```

- `execute` = return un objet Result 
- `scalar` = prend la valeur de la position [0][0] du tableau.


## Comparaison avec SQL pure:


### Pour une list de user:

```sql
SELECT * FROM users;
```
En python on va utiliser:
- `scalars()`  = extrait l'objet python
- `all()` = prend tout les objets 

```python 
res = await db.exectute(select(User))
users_list = res.scalars().all()
```

### Pour un count :

```sql
SELECT COUNT(id) FROM users WHERE deleted_at IS NULL and role='ADMIN';
```

Exact similaire en python:
```python
select(func.count(User.id)).where(User.deleted_at == None, User.role == RoleEnum.ADMIN)
```

la requete SQL sort un tableau :
```sql
wellNessDb=# SELECT COUNT(id) FROM users;
 count 
-------
     0
```
=> .scalar() va chercher le resultat du count.
