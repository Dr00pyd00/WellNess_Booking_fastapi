
# Postgres CLI tuto 


## Connection:

```bash
psql -h localhost -p 5433 -U wellNessUser -d wellNessDb
```
- `-h` — *host* : l'adresse du serveur
- `-p` — *port* : le port
- `-U` — *user* : l'utilisateur PostgreSQL
- `-d` — *database* : la base à laquelle se connecter

Une fois connect:
```bash 
wellNessDb=#
```

--- 

Ce que ca dit a Postgres:

- `Host` => regarde sur tel Machine (c'est son ip)
- `Port` => ecoute sur tel port de cette machine.
- `User` => connecte toi en tant que ...
- `database` => ouvre cette database 


## Commandes :

- `\dt` : lis toutes les tables de la base (*describe tables*)
- `\d nom_table` : decrire table
-`\l` : liste des bases de donnes 
-`\c nom_db` : changer de base de donnes
-`\du` : liste des utilisateurs postgresql

---
-`\x` : mode etendu pour mieux voir les colonnes

**Quitter** = `\q`

--- 
#### requetes : avce du SQL pure !

---

