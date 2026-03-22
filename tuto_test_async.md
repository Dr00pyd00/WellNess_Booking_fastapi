# Test Async

Il faut creer une database special test dans le container.

On se connecte :

```bash
psql -h localhost -p 5433 -U wellNessUser -d wellNessDb
```
- `-h` — *host* : l'adresse du serveur
- `-p` — *port* : le port
- `-U` — *user* : l'utilisateur PostgreSQL
- `-d` — *database* : la base à laquelle se connecter

---

### Creation de la table:
```sql
CREATE DATABASE "wellNessDb_test" OWNER "wellNessUser";
```

### gestion .env  et app_settings:

On ajoute dans .env et dans le pydantic des settings:

```python
TEST_POSTGRES_DB="wellNessDb_test"
```


