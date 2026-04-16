from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a FastAPI!"}

app = FastAPI()

# Modelo de datos
class Item(BaseModel):
    nombre: str
    apellido: str
    edad: int

# GET
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "Mensaje": "Mostrando información del item"}

# POST
@app.post("/items/")
def create_item(item: Item):
    return {"mensaje": "bienvenida" + " " + item.nombre, "item": item}

# PUT
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"mensaje": f"Item {item_id} actualizado", "item": item}

# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"mensaje": f"Item {item_id} eliminado"}