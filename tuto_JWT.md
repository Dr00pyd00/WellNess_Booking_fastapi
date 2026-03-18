
# Tuto JWT 

Le token doit contenir de la data:

- `sub` : (str par convention) = user id
- `exp` : (datetime) = temps avant expiration 
- `iat` : (datetime) = "**issued_at**", timestamp du moment de creation du token

---


### le datetime:

Objet python assez precis pour le temps:

```python
from datetime import datetime, timezone

datetime.now(timezone.utc)  
# → 2026-03-18 14:32:05.123456+00:00
```

> +00:00  : le fuseau horaire.