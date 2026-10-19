from fastapi import FastAPI,status,APIRouter,Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.Database.dbInstance import get_db
from app.Models.ProductModel import Product
from app.ElasticSearch.Client import lifespan



app=FastAPI(lifespan=lifespan)


db_dependency=Annotated[Session,Depends(get_db)]



@app.get("/healthy",status_code=status.HTTP_200_OK)
def check_server():
    return {
        "status" :"Server is Healthy",
        "success":True
    }



@app.get("/products",status_code=status.HTTP_200_OK)
async def get_products(db:db_dependency):

    products=db.query(Product).all()
    print(products)

    return {
        "success":True
    }


    