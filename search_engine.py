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

def store_relevance_judgements(query, doc_id, ip, is_rel):
    """
    Args:
        query: str
        doc_id: unique ID corresponding to a document
        ip: IP address of the user
        is_rel: 0 (not rel) or 1 (rel)
    """
    if is_rel not in ['0','1']:
        print('Invalid Relevance Feedback:', is_rel)
        return
    
    with open('data/relevance_feedback.txt', 'a') as f:
        f.write(','.join([str(i) for i in (query, doc_id, ip, is_rel)]) + '\n')



#topk = [line["title"] for line in get_top_k_docs("natural search", 3)]

