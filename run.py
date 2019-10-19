from flask import Flask, jsonify, render_template, request
from search_engine import get_top_k_docs, store_relevance_judgements

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/', methods=['POST'])
def search():
    print(request.form)
    query = request.form['query']
    ip = request.form['ip']

    store_relevance_judgements()

    docs = get_top_k_docs(query, k=10)
    
    print(docs)
    print("The query is '" + query + "'")
    print("The IP is '" + ip + "'")
    
    return jsonify(docs)


if __name__ == '__main__':
    app.run()