
```python 
import asyncio

async def tache(nom: str, delay: int):
    print(f"{nom} commence")
    await asyncio.sleep(delay)
    print(f"{nom} termine après {delay}s")

async def main():
    await asyncio.gather(
        tache("A", 3),
        tache("B", 1),
        tache("C", 2),
    )

asyncio.run(main())

```