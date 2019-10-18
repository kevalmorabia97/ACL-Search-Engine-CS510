from flask import Flask, render_template, request
from search_engine import get_top_k_docs

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def search():
    query = request.form['query']
    docs = get_top_k_docs(query, k=10)
    print(docs)
    return "<h1>The query is '" + query + "'</h1>" + str(docs)
    

if __name__ == '__main__':
    app.run()