from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

PRODUCT_INDEX = "products"


def create_product_index():
    if es.indices.exists(index=PRODUCT_INDEX):
        print("Index already exists.")
        return

    settings = {
        "settings": {
            "analysis": {
                "tokenizer": {
                    "autocomplete_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 20,
                        "token_chars": ["letter", "digit"]
                    }
                },
                "analyzer": {
                    "autocomplete_analyzer": {
                        "type": "custom",
                        "tokenizer": "autocomplete_tokenizer",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "analyzer": "autocomplete_analyzer",
                    "search_analyzer": "standard"
                },
                "description": {"type": "text"},
                "price": {"type": "float"},
                "category": {"type": "keyword"}
            }
        }
    }

    es.indices.create(index=PRODUCT_INDEX, body=settings)
    print("Created index:", PRODUCT_INDEX)
