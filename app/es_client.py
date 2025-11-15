from elasticsearch import Elasticsearch
from app.config import ES_HOST

es = Elasticsearch(ES_HOST,
                   request_timeout=50
                   )
