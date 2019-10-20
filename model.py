import sys
import numpy as np

from rank_bm25 import BM25Okapi
from rank_bm25 import BM25Plus

test_corpus = [
    "Hello there good man",
    "It is quite windy in London",
    "How is the weather today"
]

tokenized_corpus = [doc.split(" ") for doc in test_corpus]
query = "windy London"
tokenized_query = query.split(" ")

if len(sys.argv) > 1:
	model = sys.argv[1]
else:
	model = ''

if model == 'bm25':
	bm25 = BM25Plus(tokenized_corpus)
	doc_scores = bm25.get_scores(tokenized_query)
	doc_scores[::-1].sort()
	top_10_doc = bm25.get_top_n(tokenized_query, test_corpus, n=10)

else:
	doc_scores = 'Input what model to use: bm25, ...,'
	top_10_doc = ''


print(doc_scores)
print(top_10_doc)
