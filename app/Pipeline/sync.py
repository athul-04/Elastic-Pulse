from app.ElasticSearch.BulkUpload import bulk_upload_products
from elasticsearch import AsyncElasticsearch
from typing import List
from app.Models.ProductModel import Product


async def load_data_sync(es:AsyncElasticsearch,products:List[Product]):
    return await bulk_upload_products(es,products)