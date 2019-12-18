from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
from rank_bm25 import BM25Okapi, BM25Plus

from preprocessing import get_corpus, get_tokenized_corpus
from search_engine import SearchEngine


application = Flask(__name__)
CORS(application)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/search/', methods=['POST'])
def search():
    query = request.form['query'].strip()
    docs = engine.get_top_k_docs(query, k=50)
    
    return jsonify(docs)


@application.route('/save_relevance/', methods=['POST'])
def save_relevance():
    query = request.form['query'].strip()
    doc_id = request.form['doc_id']
    rel_score = request.form['rel_score']

    engine.store_relevance_judgements(query, doc_id, rel_score)
    return ('', 204)


if __name__ == '__main__':
    print('Initializing Search Engine...')
    
    corpus = get_corpus('data/corpus1.pkl') + get_corpus('data/corpus2.pkl')
    tokenized_corpus = get_tokenized_corpus('data/tokenized_corpus1.pkl') + get_tokenized_corpus('data/tokenized_corpus2.pkl')
    model = BM25Plus(tokenized_corpus)
    engine = SearchEngine(model, corpus, 'data/relevance_feedback.txt')

    print('Done!')

    application.run()