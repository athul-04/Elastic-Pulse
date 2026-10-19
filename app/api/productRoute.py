from fastapi import APIRouter,status,Depends
from typing import Annotated
from elasticsearch import AsyncElasticsearch
from sqlalchemy.orm import Session
from app.Database.dbInstance import get_db
from app.ElasticSearch.dependencies import get_es_client
from app.Models.ProductModel import Product
from app.ElasticSearch.BulkUpload import bulk_upload_products
from app.Pipeline.sync import data_sync


router=APIRouter(
    prefix="/products",
    tags=["products funcs"]
)


#Dependencies
db_dependency=Annotated[Session,Depends(get_db)]
es_dependency=Annotated[AsyncElasticsearch,Depends(get_es_client)]


@router.post("/bulkupload",status_code=status.HTTP_201_CREATED)
async def bulkupload(db:db_dependency,es:es_dependency):


    products=db.query(Product).all()

    # debugging line...
    # print(products[0])


    response=await data_sync(es,products)

    return response



