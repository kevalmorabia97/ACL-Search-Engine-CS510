import sys
import numpy as np

from rank_bm25 import BM25Okapi
from rank_bm25 import BM25Plus
import preprocessing as p

def get_top_k_docs(query, k=10):
    """
    Args:
        query: string
        k: int (default: 1)
    
    Returns:
        top_k_docs: dictionary keys: titles, abstracts, urls, ids. Each element in dict[key] is a list of k elements in descending order of relevance
    """
    tokenized_query = p.preprocess_query(query)
    corpus, tokenized_corpus = p.read_file()

    bm25 = BM25Plus(tokenized_corpus)
    top_k_docs = bm25.get_top_n(tokenized_query, corpus, n=k)

    return top_k_docs



def store_relevance_judgements():
    ## TODO ##
    pass


#topk = [line["title"] for line in get_top_k_docs("natural search", 3)]
