# Chargement des relations en SQLAlchemy async — Fiche de référence

## Le problème de base

En SQLAlchemy **async**, les relations ne se chargent pas automatiquement.

```python
# ❌ INTERDIT en async — déclenche MissingGreenlet error
practitioner = await db.get(Practitioner, 1)
print(practitioner.user_profile)  # lazy load impossible en async
```

En async, toute requête SQL doit être explicite avec `await`.

---

## Deux situations, deux solutions

### Situation 1 — Tu viens de créer / modifier un objet

Tu as un seul objet, tu veux recharger ses données + une relation après un `commit`.

```python
new_profile = Practitioner(**data, user_id=user_id)
db.add(new_profile)
await db.commit()

# recharger l'objet + sa relation
await db.refresh(new_profile, ["user_profile"])

return new_profile  # user_profile est disponible ✅
```

`db.refresh(obj, ["relation"])` dit à SQLAlchemy :
> "Recharge cet objet depuis la DB, et charge aussi cette relation."

✅ Valide pour **un seul objet** après création ou modification.

---

### Situation 2 — Tu fais une query (SELECT)

Tu récupères un ou plusieurs objets avec `select()`.

```python
# ❌ Sans selectinload — user_profile non chargé
result = await db.execute(select(Practitioner))
practitioners = result.scalars().all()
practitioners[0].user_profile  # 💥 MissingGreenlet error
```

```python
# ✅ Avec selectinload — user_profile chargé
from sqlalchemy.orm import selectinload

result = await db.execute(
    select(Practitioner)
    .options(selectinload(Practitioner.user_profile))
)
practitioners = result.scalars().all()
practitioners[0].user_profile  # ✅ disponible
```

`selectinload` fait **2 requêtes SQL** :
1. La requête principale sur `practitioners`
2. Une deuxième requête pour charger `user_profile`

---

## Charger plusieurs relations en même temps

```python
result = await db.execute(
    select(Booking)
    .where(Booking.id == booking_id)
    .options(
        selectinload(Booking.user_profile),   # charge le patient
        selectinload(Booking.availability),    # charge le créneau
    )
)
```

---

## Pourquoi c'est lié à Pydantic ?

Pydantic avec `from_attributes=True` accède aux attributs de l'objet SQLAlchemy pour sérialiser.

Si ton schema a `user_profile: UserDataFromDbSchema`, Pydantic fait :
```python
obj.user_profile  # accès à la relation → MissingGreenlet si pas chargée
```

**Règle simple : si ton schema Pydantic contient une relation → tu dois la charger.**

```python
# Ce schema contient une relation → chargement obligatoire
class PractitionerDataFromDbSchema(BaseModel):
    id: int
    speciality: str
    user_profile: UserDataFromDbSchema  # ← relation

# Ce schema ne contient pas de relation → pas besoin
class PractitionerDataFromDbSchema(BaseModel):
    id: int
    speciality: str
    user_id: int  # ← juste un int
```

---

## Récapitulatif

| Situation | Solution |
|---|---|
| Création / modification d'un objet | `await db.refresh(obj, ["relation"])` |
| Query SELECT | `.options(selectinload(Model.relation))` |
| Schema Pydantic sans relation | `await db.refresh(obj)` suffit |
| Accès à `obj.relation` dans le service | `selectinload` dans le `select` |

---

## À ne pas confondre

- `db.refresh(obj)` → rafraîchit les **colonnes scalaires** uniquement
- `db.refresh(obj, ["relation"])` → rafraîchit + charge la **relation** pour un objet unique
- `selectinload` → charge les **relations** dans une **query**