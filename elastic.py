#!/usr/bin/env python

import datetime
import feedparser
import json
import urllib2
import urllib

from flask import make_response
from flask import Flask
from flask import render_template
from flask import request

from elasticsearch import Elasticsearch
from elasticsearch import helpers

app = Flask(__name__)


ES = Elasticsearch()

@app.route("/")
def home():
    batchID = request.args.get("batchID")
    batches = get_batches()
    if not batchID:
        batchID = 1
    mapping = get_batchID(batchID)
    response = make_response(render_template("home.html",
                batchID=batchID,
                batches=batches,
                mapping=mapping))
    return response


def get_batches():
	batch_search = ES.search(index='mapping')
	batches = None
	if batch_search:
		batch_list = batch_search['hits']['hits']
		batches = set([batchID['_source']['batchID'] for batchID in batch_list])
	return batches


def get_batchID(query):
	batch_search = ES.search(index='mapping', body={'query': {'match': {'batchID': '{}'.format(query)}}})
	batchID = None
	if batch_search:
		batchID = batch_search['hits']['hits']
	return batchID


if __name__ == "__main__":
    app.run(port=5000, debug=True)
