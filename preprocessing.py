from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from nltk.stem import WordNetLemmatizer
from os import listdir
import ast
import pandas as pd
import string

lemmatizer = WordNetLemmatizer()
more_stopwords = [word.strip() for word in open("lemur-stopwords.txt", "r").readlines()]
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')

def preprocess_document():
    df = pd.DataFrame(columns=['id', 'title', 'abstract', 'introduction', 'link'])
    acad_papers = "C:/Users/Dell-pc/PycharmProjects/CS510Phase2/datasets/Academic_papers/docs.json"
    id = 0
    for x in open(acad_papers, "r").readlines():
        print(id)
        try:
            paper = {}
            x = ast.literal_eval(x)
            paper['id'] = id
            paper['title'] = ' '.join(x['title'])
            paper['abstract'] = ' '.join(x['paperAbstract'])
            paper['introduction'] = ' '.join(x['keyPhrases'])
            paper['link'] = ''
            df = df.append(paper, ignore_index=True)
            id += 1
        except:
            continue

    dir_path = "C:/Users/Dell-pc/Desktop/UIUC/Fall 2019/CS 510 IR/grobid_processed"
    for doc_name in listdir(dir_path):
        print(id)
        try:
            doc_path = dir_path + '/' + doc_name
            with open(doc_path, 'r') as f:
                data = f.read()
                text = re.split('\<(.*?)\>', data)
                tags = re.findall('\<(.*?)\>', data)
                tags.insert(0, 'content')
                content = [item.strip() for item in text if item not in tags]
                output = dict(zip(tags, content))
                output = {key: output[key] for key in {'title', 'abstract', 'introduction'}}
                output.update({'id': id})
                output.update({'link': doc_name})
                df = df.append(output, ignore_index=True)
            f.close()
            id += 1
        except:
            continue
    listdfs =  splitDataFrameIntoSmaller(df)
    listdfs[0].to_pickle('corpus1.pkl')
    listdfs[1].to_pickle('corpus2.pkl')

def preprocess_content(filename, fileno):
    df = pd.read_pickle(filename)
    df['tokens'] = df['title'] + " " + df['abstract'] + " " + df['introduction']
    tokenized_df = pd.DataFrame(columns=['id', 'tokens'])
    for i in range(df.shape[0]):
        print(i)
        paper = df.iloc[i]
        tokens = paper[['tokens']][0].lower().split()
        tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word in tokens if word not in stopwords.words('english') and word not in more_stopwords]
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        tokenized_df = tokenized_df.append({'id': paper[['id']], 'tokens': tokens}, ignore_index=True)
    if fileno == 1:
        tokenized_df.to_pickle('tokenized_corpus1.pkl')
    if fileno == 2:
        tokenized_df.to_pickle('tokenized_corpus2.pkl')

def splitDataFrameIntoSmaller(df, chunkSize = 20000):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf

def get_corpus(filename):
    df = pd.read_pickle(filename)
    corpus = []
    for i in range(df.shape[0]):
        link = ''
        if df.iloc[i]['link'] != '':
            link = 'https://www.aclweb.org/anthology/'+df.iloc[i]['link'].strip('.tei.xml')+'.pdf'
        corpus.append({'title': df.iloc[i]['title'], 'abstract': df.iloc[i]['abstract'], 'introduction': df.iloc[i]['introduction'],
                       'link': link, 'id': df.iloc[i]['id']})
    return corpus

def get_tokenized_corpus(filename):
    df = pd.read_pickle(filename)
    tokenized_corpus = []
    for i in range(df.shape[0]):
        tokenized_corpus.append(df.iloc[i]['tokens'])
    return tokenized_corpus

# preprocess_document()
# preprocess_content('corpus1.pkl', 1)
# preprocess_content('corpus2.pkl', 2)
# print(get_corpus('corpus1.pkl')[-1])
# print(get_tokenized_corpus('tokenized_corpus1.pkl'))

# test----------------------------------------------------------------------
# corpus, tokenized_corpus = get_corpus('corpus1.pkl'), get_tokenized_corpus('tokenized_corpus1.pkl')
# import rank_bm25
# bm25 = rank_bm25.BM25Plus(tokenized_corpus)
# doc_scores = bm25.get_scores(['natural','language'])
# doc_scores[::-1].sort()
# top_10_doc = bm25.get_top_n(['natural','language'], corpus, n=10)
# print(top_10_doc)

def preprocess_query(query_string):
    query_string = query_string.lower()
    new_text = tokenizer.tokenize(query_string)
    new_text = [word.translate(str.maketrans('', '', string.punctuation)) for word in new_text if word not in stopwords.words('english') and word not in more_stopwords]
    new_text = [lemmatizer.lemmatize(word) for word in new_text]
    return new_text
