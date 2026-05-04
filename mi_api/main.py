from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Item
from database import engine
from database import Base
from dependencies import get_db
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a FastAPI!"}

app = FastAPI()

# Modelo de datos
#class Item(BaseModel):
#    nombre: str
#    apellido: str
#    edad: int

# GET
#@app.get("/items/{item_id}")
#def get_item(item_id: int):
#   return {"item_id": item_id, "Mensaje": "Mostrando información del item"}

# POST
#@app.post("/items/")
#def create_item(item: Item):
#    return {"mensaje": "bienvenida" + " " + item.nombre, "item": item}

# PUT
#@app.put("/items/{item_id}")
#def update_item(item_id: int, item: Item):
#    return {"mensaje": f"Item {item_id} actualizado", "item": item}

# DELETE
#@app.delete("/items/{item_id}")
#def delete_item(item_id: int):
#    return {"mensaje": f"Item {item_id} eliminado"}

class ItemCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    en_stock: bool = True

class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@app.get("/items/", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    await db.delete(item)
    await db.commit()
    return {"mensaje": "Item eliminado"}