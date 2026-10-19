from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from app.Settings.SecretSettings import settings
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize connection using Cloud ID and API Key
    app.state.es_client = AsyncElasticsearch(
        cloud_id=settings.elastic_cloud_id,
        api_key=settings.elastic_API_key
    )
    yield
    # Clean up and close connection pools on shutdown
    await app.state.es_client.close()

