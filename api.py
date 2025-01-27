from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

tags_metadata = [
    {"name": "items", "description": "Gestion des objets"},
    {"name": "consumers", "description": "Gestions des consomateurs"},
]

app = FastAPI(
    title="Items and consumers",
    version="1.0.0",
    openapi_tags=tags_metadata,
)


class Item(BaseModel):
    name: str
    description: str
    price: float
    id: Optional[int] = None


class Consumer(BaseModel):
    name: str
    email: str
    bucket_list: List[int] = []
    id: Optional[int] = None


items: List[Item] = [
    Item(
        name="Fruit de Lune",
        description="Un fruit juteux qui brille dans l'obscurité, avec un goût sucré et acidulé.",
        price=15.99,
        id=1,
    ),
    Item(
        name="Noix de Rêve",
        description="Des noix croquantes qui stimulent l'imagination, avec une saveur de caramel et de vanille.",
        price=9.50,
        id=2,
    ),
    Item(
        name="Lait de Nuage",
        description="Une boisson légère et mousseuse, infusée de saveurs florales, parfaite pour se détendre.",
        price=7.99,
        id=3,
    ),
    Item(
        name="Pâtisserie Étoilée",
        description="Une délicieuse pâtisserie garnie de crème aux étoiles, qui fond dans la bouche.",
        price=12.50,
        id=4,
    ),
    Item(
        name="Gelée de Tempête",
        description="Une gelée vibrante qui change de couleur, avec un goût épicé et fruité.",
        price=8.99,
        id=5,
    ),
    Item(
        name="Chocolat de l'Inspiration",
        description="Un chocolat riche et crémeux qui stimule la créativité, avec des éclats de menthe.",
        price=10.99,
        id=6,
    ),
    Item(
        name="Thé des Sages",
        description="Un mélange de plantes rares qui favorise la clarté d'esprit et la sérénité.",
        price=6.50,
        id=7,
    ),
    Item(
        name="Gâteau des Rêves",
        description="Un gâteau léger et aérien, garni de crème fouettée et de fruits enchantés.",
        price=14.99,
        id=8,
    ),
]
consumers: List[Consumer] = [
    Consumer(name="Alice Dupont", email="alice.dupont@example.com", id=1),
    Consumer(name="Jean Martin", email="jean.martin@example.com", id=2),
    Consumer(name="Sophie Leroy", email="sophie.leroy@example.com", id=3),
    Consumer(name="Pierre Durand", email="pierre.durand@example.com", id=4),
    Consumer(name="Claire Petit", email="claire.petit@example.com", id=5),
]


@app.get("/items/", tags=["items"])
async def read_items() -> list[Item]:
    return items


@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int):
    if item_id not in [i.id for i in items]:
        raise HTTPException(status_code=404, detail="Item not found")
    return [i for i in items if i.id == item_id][0]


@app.post("/items/", tags=["items"])
async def create_item(name: str, price: int, description: str = ""):
    item_id = max([i.id for i in items if i.id is not None]) + 1
    items.append(Item(name=name, description=description, price=price, id=item_id))
    return {"item_id": item_id}


@app.put("/items/{item_id}", tags=["items"])
async def update_item(
    item_id: int,
    name: Optional[str] = None,
    price: Optional[int] = None,
    description: Optional[str] = None,
) -> Item:
    if item_id not in [i.id for i in items]:
        raise HTTPException(status_code=404, detail="Item not found")

    item = [i for i in items if i.id == item_id][0]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if description is not None:
        item.description = description
    return item


@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: int):
    if item_id not in [i.id for i in items]:
        raise HTTPException(status_code=404, detail="Item not found")
    item = [i for i in items if i.id == item_id][0]
    items.remove(item)
    return {"detail": f"Item {item_id} deleted"}


@app.get("/consumers/", tags=["consumers"])
async def read_consumers():
    return consumers


@app.post("/consumers/", tags=["consumers"])
async def create_consumer(name: str, email: str):
    consumer_id = max([c.id for c in consumers if c.id is not None]) + 1
    consumer = Consumer(name=name, email=email, id=consumer_id)
    consumers.append(consumer)
    return {"consumer_id": consumer_id}


@app.get("/consumers/{consumer_id}", tags=["consumers"])
async def read_consumer(consumer_id: int):
    if consumer_id not in [i.id for i in consumers]:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return [c for c in consumers if c.id == consumer_id][0]


@app.put("/consumers/{consumer_id}", tags=["consumers"])
async def update_consumer(consumer_id: int, consumer: Consumer):
    try:
        consumer_old = [c for c in consumers if c.id == consumer_id][0]
    except KeyError:
        raise HTTPException(status_code=404, detail="Consumer not found")

    consumer.id = consumer_id
    consumers.append(consumer)
    consumers.remove(consumer_old)

    return consumer


@app.delete("/consumers/{consumer_id}", tags=["consumers"])
async def delete_consumer(consumer_id: int):
    try:
        consumer_old = [c for c in consumers if c.id == consumer_id][0]
    except KeyError:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumers.remove(consumer_old)
    return {"detail": f"Consumer {consumer_id} deleted"}


@app.post("/consumers/{consumer_id}/bucket_list/", tags=["consumers"])
async def add_to_bucket_list(consumer_id: int, item_id: int):
    try:
        consumer = [c for c in consumers if c.id == consumer_id][0]
    except KeyError:
        raise HTTPException(status_code=404, detail="Consumer not found")
    try:
        item = [i for i in items if i.id == item_id][0]
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")

    consumer.bucket_list.append(item.id)
    return {
        "detail": f"Added item {item.name} to consumer {consumer.name}'s bucket list"
    }


@app.delete("/consumers/{consumer_id}/bucket_list/{item_id}", tags=["consumers"])
async def delete_from_bucket_list(consumer_id: int, item_id: int):
    try:
        consumer = [c for c in consumers if c.id == consumer_id][0]
    except KeyError:
        raise HTTPException(status_code=404, detail="Consumer not found")
    try:
        item = [i for i in items if i.id == item_id][0]
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")
    consumer.bucket_list.remove(item_id)
    return {
        "detail": f"Removed item {item_id} from consumer {consumer.name}'s bucket list"
    }
