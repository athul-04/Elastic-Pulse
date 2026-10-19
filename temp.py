from typing import Any

from elasticsearch.helpers import async_bulk
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["Products"])


class Product(BaseModel):
    id: str = Field(min_length=1)
    name: str
    description: str


class BulkUploadRequest(BaseModel):
    products: list[Product] = Field(min_length=1, max_length=1000)


@router.post("/bulk-upload")
async def bulk_upload_products(
    request: Request,
    payload: BulkUploadRequest,
):
    es = request.app.state.es_client

    actions: list[dict[str, Any]] = [
        {
            "_index": "products",
            "_id": product.id,
            "_source": {
                "name": product.name,
                "description": product.description,
            },
        }
        for product in payload.products
    ]

    try:
        uploaded, errors = await async_bulk(
            es,
            actions,
            raise_on_error=False,
            stats_only=False,
        )

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