from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
from rank_bm25 import BM25Okapi, BM25Plus

from preprocessing import read_file
from search_engine import get_top_k_docs, store_relevance_judgements


application = Flask(__name__)
CORS(application)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    docs = get_top_k_docs(model, query, corpus, k=100)
    
    return jsonify(docs)


@application.route('/save_relevance/', methods=['POST'])
def save_relevance():
    query = request.form['query']
    doc_id = request.form['doc_id']
    ip = request.form['ip']
    is_rel = request.form['is_rel']

    store_relevance_judgements(query, doc_id, ip, is_rel)
    return ('', 204)


if __name__ == '__main__':
    print('Loading Corpus...')
    corpus, tokenized_corpus = read_file()
    model = BM25Plus(tokenized_corpus)
    print('Corpus Loaded!')

    application.run()