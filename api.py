from typing import Dict, List

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


class Consumer(BaseModel):
    name: str
    email: str
    bucket_list: List[Item] = []


items: Dict[int, Item] = {}
consumers: Dict[int, Consumer] = {}


items[1] = Item(
    name="Fruit de Lune",
    description="Un fruit juteux qui brille dans l'obscurité, avec un goût sucré et acidulé.",
    price=15.99,
)
items[2] = Item(
    name="Noix de Rêve",
    description="Des noix croquantes qui stimulent l'imagination, avec une saveur de caramel et de vanille.",
    price=9.50,
)
items[3] = Item(
    name="Lait de Nuage",
    description="Une boisson légère et mousseuse, infusée de saveurs florales, parfaite pour se détendre.",
    price=7.99,
)
items[4] = Item(
    name="Pâtisserie Étoilée",
    description="Une délicieuse pâtisserie garnie de crème aux étoiles, qui fond dans la bouche.",
    price=12.50,
)
items[5] = Item(
    name="Gelée de Tempête",
    description="Une gelée vibrante qui change de couleur, avec un goût épicé et fruité.",
    price=8.99,
)
items[6] = Item(
    name="Chocolat de l'Inspiration",
    description="Un chocolat riche et crémeux qui stimule la créativité, avec des éclats de menthe.",
    price=10.99,
)
items[7] = Item(
    name="Thé des Sages",
    description="Un mélange de plantes rares qui favorise la clarté d'esprit et la sérénité.",
    price=6.50,
)
items[8] = Item(
    name="Gâteau des Rêves",
    description="Un gâteau léger et aérien, garni de crème fouettée et de fruits enchantés.",
    price=14.99,
)

consumers[1] = Consumer(name="Alice Dupont", email="alice.dupont@example.com")
consumers[2] = Consumer(name="Jean Martin", email="jean.martin@example.com")
consumers[3] = Consumer(name="Sophie Leroy", email="sophie.leroy@example.com")
consumers[4] = Consumer(name="Pierre Durand", email="pierre.durand@example.com")
consumers[5] = Consumer(name="Claire Petit", email="claire.petit@example.com")


@app.get("/items/", tags=["items"])
async def read_items() -> list[Item]:
    return list(items.values())


@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items/", tags=["items"])
async def create_item(name: str, price: int, description: str = ""):
    item = Item(name=name, description=description, price=price)
    item_id = len(items) + 1
    items[item_id] = item
    return {"item_id": item_id}


@app.put("/items/{item_id}", tags=["items"])
async def update_item(item_id: int, name: str, price: int, description: str = ""):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = Item(name=name, description=description, price=price)
    return {"item_id": item_id}


@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"detail": "Item deleted"}


@app.post("/consumers/", tags=["consumers"])
async def create_consumer(name: str, email: str):
    consumer = Consumer(name=name, email=email)
    consumer_id = len(consumers) + 1
    consumers[consumer_id] = consumer
    return {"consumer_id": consumer_id}


@app.get("/consumers/{consumer_id}", tags=["consumers"])
async def read_consumer(consumer_id: int):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return consumers[consumer_id]


@app.get("/consumers/", tags=["consumers"])
async def read_consumers():
    return consumers.values()


@app.put("/consumers/{consumer_id}", tags=["consumers"])
async def update_consumer(consumer_id: int, consumer: Consumer):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumers[consumer_id] = consumer
    return {"consumer_id": consumer_id}


@app.delete("/consumers/{consumer_id}", tags=["consumers"])
async def delete_consumer(consumer_id: int):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    del consumers[consumer_id]
    return {"detail": "Consumer deleted"}


@app.post("/consumers/{consumer_id}/bucket_list/", tags=["consumers"])
async def add_to_bucket_list(consumer_id: int, item_id: int):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    consumer = consumers[consumer_id]
    item = items[item_id]
    consumer.bucket_list.append(item)
    return {
        "detail": f"Added item {item.name} to consumer {consumer.name}'s bucket list"
    }


@app.get("/consumers/{consumer_id}/bucket_list/", tags=["consumers"])
async def get_bucket_list(consumer_id: int):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumer = consumers[consumer_id]
    return consumer.bucket_list


@app.delete("/consumers/{consumer_id}/bucket_list/{item_id}", tags=["consumers"])
async def delete_from_bucket_list(consumer_id: int, item_id: int):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumer = consumers[consumer_id]
    if item_id not in [item.id for item in consumer.bucket_list]:
        raise HTTPException(
            status_code=404, detail="Item not found in consumer's bucket list"
        )
    consumer.bucket_list = [item for item in consumer.bucket_list if item.id != item_id]
    return {
        "detail": f"Removed item {item_id} from consumer {consumer.name}'s bucket list"
    }
