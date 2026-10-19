from fastapi import FastAPI,status,APIRouter,Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.Database.dbInstance import get_db
from app.Models.ProductModel import Product
from app.ElasticSearch.Client import lifespan
from elasticsearch import AsyncElasticsearch
from app.ElasticSearch.dependencies import get_es_client

app=FastAPI(lifespan=lifespan)



db_dependency=Annotated[Session,Depends(get_db)]
es_dependency=Annotated[AsyncElasticsearch,Depends(get_es_client)]





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




@app.get("/clusterhealth")
async def check_health(es:es_dependency):
    try:
        cluster_info = await es.info()
        return {"status": "connected", "cluster_name": cluster_info["cluster_name"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    