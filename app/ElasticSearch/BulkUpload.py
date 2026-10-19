from typing import Any,List
from elasticsearch.helpers import async_bulk
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from app.Models.ProductModel import Product
from .Mapper import map_product_to_document
from elasticsearch import AsyncElasticsearch





async def bulk_upload_products(es:AsyncElasticsearch,products:List[Product]):

    actions: list[dict[str, Any]] = [
        {
            "_index": "products",
            "_id": product.ec_product_id,
            "_source": map_product_to_document(product)
        }
        for product in products
    ]

    try:
        uploaded, errors = await async_bulk(
            es,
            actions,
            raise_on_error=False,
            stats_only=False,
        )
        # For debugging purposes
        print(actions[0])

        return {
            "total_submitted": len(actions),
            "uploaded": uploaded,
            "failed": len(errors),
            "errors": errors[:5],
        }

    

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Bulk upload to Elasticsearch failed",
        ) from exc