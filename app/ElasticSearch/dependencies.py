from elasticsearch import AsyncElasticsearch
from fastapi import Request

async def get_es_client(request:Request)->AsyncElasticsearch:
    return request.app.state.es_client