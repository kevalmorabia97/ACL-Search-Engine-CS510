from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
from search_engine import get_top_k_docs, store_relevance_judgements

application = Flask(__name__)
CORS(application)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    docs = get_top_k_docs(query, k=10)
    
    print("The query is '" + query + "'")
    
    return jsonify(docs)


@application.route('/save_relevance/', methods=['POST'])
def save_relevance():
    query = request.form['query']
    doc_id = request.form['doc_id']
    ip = request.form['ip']
    is_rel = request.form['is_rel']

    print(query, doc_id, ip, is_rel)
    store_relevance_judgements(query, doc_id, ip, is_rel)
    return ('', 204)


if __name__ == '__main__':
    application.run()