from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import properties

host, access_key, access_secret, region = properties.getElasticsearchCredentials()
awsauth = AWS4Auth(access_key, access_secret, region, "es")

es = Elasticsearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def storeToElasticsearch(id, data):
    res = es.index(index="tweet-data", doc_type="tweets", id=id, body=data)
    return res["result"]


def searchInElasticsearch(query):
    if query is None:
        res = es.search(index="tweet-data", doc_type="tweets",
                        body={"query": {"match_all": {}}}, size=10000)
    else:
        res = es.search(index="tweet-data", doc_type="tweets",
                        body={"query": {"match": {"text": query}}}, size=10000)
    return res["hits"]["hits"]


def deleteFromElasticsearch(id):
    res = es.delete(index="tweet-data", doc_type="tweets", id=id)
    return res


def deleteAllFromElasticsearch():
    res = es.indices.delete(index='tweet-data', ignore=[400, 404])
    return res


if __name__ == "__main__":
    # id = 1
    # data = '{"default": "default", "text": "I am not surprised", "coordinates": [39.02834, 50.98378]}'
    # storeToElasticsearch(id, data)
    # res = searchInElasticsearch(None)
    # for tweet in res:
    #     deleteFromElasticsearch(int(tweet['_id']))
    deleteAllFromElasticsearch()
