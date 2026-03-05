from fastapi import FastAPI, HTTPException
from typing import List, Dict

from app.models import Product, ProductCreate, ProductUpdate

app = FastAPI(
    title="Gestion de Produits API",
    description="API CRUD pour la gestion de produits de la boutique en ligne",
    version="1.0.0"
)

# Stockage en mémoire (simulant une base de données)
db: Dict[int, Product] = {}
current_id = 1

@app.post("/products", response_model=Product, status_code=201)
def create_product(product_in: ProductCreate):
    global current_id
    product = Product(id=current_id, **product_in.model_dump())
    db[current_id] = product
    current_id += 1
    return product

@app.get("/products", response_model=List[Product])
def read_products():
    return list(db.values())

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    return db[product_id]

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_in: ProductUpdate):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_product = db[product_id]
    update_data = product_in.model_dump(exclude_unset=True)
    
    # Met à jour les champs
    updated_product = existing_product.model_copy(update=update_data)
    db[product_id] = updated_product
    return updated_product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    del db[product_id]
    return None
