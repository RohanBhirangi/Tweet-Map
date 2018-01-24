from django.http import HttpResponse
from django.shortcuts import render
from Map.scripts import elasticsearch_script
import json


def home(request):
    return render(request, "map/home.html")


def elasticsearch(request):
	keyword = list(request.GET.keys())[0].strip('"')
	response_data = []
	if keyword == "":
		res = elasticsearch_script.searchInElasticsearch(None)
	else:
		res = elasticsearch_script.searchInElasticsearch(keyword)
	for tweet in res:
	    response_data.append(tweet['_source'])
	response_json = json.dumps(response_data)
	return HttpResponse(response_json, content_type="application/json")
