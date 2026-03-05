from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    nom: str
    description: Optional[str] = None
    prix: float
    quantite_stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    prix: Optional[float] = None
    quantite_stock: Optional[int] = None

class Product(ProductBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
