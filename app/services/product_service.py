from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from app.config import PRODUCT_INDEX
from app.es_client import es


def index_product(product):
    es.index(
        index=PRODUCT_INDEX,
        id=product.id,
        document=product.dict()
    )


def batch_index(products: list):
    actions = []

    for p in products:
        actions.append({
            "_op_type": "index",
            "_index": PRODUCT_INDEX,
            "_id": p.id,
            "_source": p.dict()
        })

    bulk(es, actions)
    return {"indexed": len(products)}


def search_products(q: str, page: int, size: int, sort_by: str):

    # Ensure valid sort fields
    allowed_sorts = ["price", "category"]
    if sort_by not in allowed_sorts:
        sort_by = "price"

    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["name", "description"]
            }
        },
        "from": (page - 1) * size,
        "size": size,
        "sort": [
            {sort_by: {"order": "asc"}}
        ]
    }

    return es.search(index=PRODUCT_INDEX, body=query)["hits"]["hits"]


def category_analytics():
    query = {
        "size": 0,
        "aggs": {
            "by_category": {
                "terms": {"field": "category"}
            }
        }
    }

    return es.search(index=PRODUCT_INDEX, body=query)["aggregations"]


def autocomplete(prefix: str):
    query = {
        "query": {
            "match_phrase_prefix": {
                "name": {
                    "query": prefix
                }
            }
        },
        "size": 5
    }

    return es.search(index=PRODUCT_INDEX, body=query)["hits"]["hits"]
