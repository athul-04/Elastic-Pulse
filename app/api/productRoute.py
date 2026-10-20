from datetime import datetime, timezone

from fastapi import APIRouter,status,Depends,HTTPException
from typing import Annotated
from elasticsearch import AsyncElasticsearch
from sqlalchemy.orm import Session
from app.Database.dbInstance import get_db
from app.ElasticSearch.dependencies import get_es_client
from app.Models.ProductModel import Product
from app.Models.sync_table import SyncTable
from app.ElasticSearch.BulkUpload import bulk_upload_products
from app.Pipeline.sync import load_data_sync


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
    pipeline=db.query(SyncTable).filter(SyncTable.pipeline_name=="mysql_to_elasticsearch".casefold()).first()
    if pipeline is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="The pipeline record dosent exist in the aiven database")


    response=await load_data_sync(es,products)

    
    setattr(pipeline,"last_sync_time",datetime.now(timezone.utc).replace(tzinfo=None))

    db.commit()
    db.refresh(pipeline)

    return response





@router.post("/incremental_load",status_code=status.HTTP_200_OK)
async def incremental_load(db:db_dependency,es:es_dependency):

    pipeline=db.query(SyncTable).filter(SyncTable.pipeline_name=="mysql_to_elasticsearch".casefold()).first()
    if pipeline is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="The pipeline record dosent exist in the aiven database")
    products=db.query(Product).filter(Product.updated_at>pipeline.last_sync_time).order_by(Product.updated_at,Product.ec_product_id).all()

    if len(products)==0:
        return {
            "success":True,
            "message":"All data are in sync with the last update",
            "total_submitted": 0,
            "uploaded": 0,
            "failed": 0,
            "errors": 0,
        }

    response=await load_data_sync(es,products)
    
    pipeline=db.query(SyncTable).filter(SyncTable.pipeline_name=="mysql_to_elasticsearch".casefold()).first()
    setattr(pipeline,"last_sync_time",datetime.now(timezone.utc).replace(tzinfo=None))
    
    db.commit()
    db.refresh(pipeline)
    
    return response



