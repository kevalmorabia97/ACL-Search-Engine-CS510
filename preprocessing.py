from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from nltk.stem import WordNetLemmatizer
from os import listdir
import ast
import pandas as pd

# lemmatizer = WordNetLemmatizer()
# porter_stemmer = PorterStemmer()
# tokenizer = RegexpTokenizer(r'\w+')

import spacy

def preprocess_document(dir_path):
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

def preprocess_content(filename, i):
    df = pd.read_pickle(filename)
    df['tokens'] = df['title'] + " " + df['abstract'] + " " + df['introduction']
    nlp = spacy.load("en_core_web_md")
    nlp.max_length = 1500000
    tokenized_df = pd.DataFrame(columns=['id', 'tokens'])
    for i in range(df.shape[0]):
        print(i)
        paper = df.iloc[i]
        tokens = paper[['tokens']][0].lower()
        lem_tokens = nlp(tokens)
        tokens = [token.lemma_ for token in lem_tokens if (not token.is_oov and (str(token) not in stopwords.words('english')))]
        tokenized_df = tokenized_df.append({'id': paper[['id']], 'tokens': tokens}, ignore_index=True)
    if i ==1:
        tokenized_df.to_pickle('tokenized_corpus1.pkl')
    else:
        tokenized_df.to_pickle('tokenized_corpus2.pkl')

def splitDataFrameIntoSmaller(df, chunkSize = 20000):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf

# preprocess_document("C:/Users/Dell-pc/Desktop/UIUC/Fall 2019/CS 510 IR/grobid_processed")
# preprocess_content('corpus1.pkl', 1)
# preprocess_content('corpus2.pkl', 2)

# def preprocess_query(query_string, stemming = True, lower_case = True, lemma = True, stopword_removal = True):
#     #return processed tokenized query
#     if lower_case:
#         query_string = query_string.lower()
#         new_text = tokenizer.tokenize(query_string)
#     else:
#         new_text = tokenizer.tokenize(query_string)
#     if stopword_removal:
#         new_text = [word for word in new_text if word not in stopwords.words('english')]
#     if stemming:
#         new_text = [porter_stemmer.stem(word) for word in new_text]
#     if lemma:
#         new_text = [lemmatizer.lemmatize(word) for word in new_text]
#     return(new_text)

# def preprocess_document(doc_path, stemming, lower_case, lemma, stopword_removal):
#     '''
#     :param doc_path: Directory path for document, ex: "C:/Users/Tara/Desktop/grobid_processed/docname.xml"
#     :param stemming: True -> Do stemming for words in doc
#     :param lower_case: True -> Convert all words to lowercase
#     :param lemma: True -> Do lemmatization for words in doc
#     :param stopword_removal: True -> Remove stopwords from doc
#     :return: dict {content: [w1,w2..], figcaptions: [w1,w2..], tablecaptions: [w1,w2..], title: [w1,w2..], abstract: [w1,w2..], introduction: [w1,w2..]}
#     '''
#     try:
#         with open(doc_path, 'r') as f:
#             data = f.read()
#         f.close()
#     except:
#         return (False,False,False)
#         # return False
#
#     text = re.split('\<(.*?)\>', data)
#     tags = re.findall('\<(.*?)\>', data)
#     tags.insert(0,'content')
#     content = [item for item in text if item not in tags]
#     output = dict(zip(tags,content))
#     output = {key: output[key] for key in {'title', 'abstract', 'introduction'}}
#     temp = {key: output[key] for key in {'title', 'abstract', 'introduction'}}
#     corpus = []
#
#     for tag, content in output.items():
#         corpus.append(content)
#         if lower_case:
#             content = content.lower()
#             new_text = tokenizer.tokenize(content)
#         else:
#             new_text = tokenizer.tokenize(content)
#
#         if stopword_removal:
#             new_text = [word for word in new_text if word not in stopwords.words('english')]
#
#         if stemming:
#             new_text = [porter_stemmer.stem(word) for word in new_text]
#
#         if lemma:
#             new_text = [lemmatizer.lemmatize(word) for word in new_text]
#         output[tag] = new_text
#
#
#     corpus = " ".join(corpus).replace("\n",'')
#     tokenized_corpus = [val for sublist in output.values() for val in sublist]
#     return(corpus, tokenized_corpus, temp)
#     # return(tokenized_corpus)
#     # return temp

# def preprocess(dir_path, stemming = True, lower_case = True, lemma = True, stopword_removal = True):
#     corpus = open("corpus.txt", "w")
#     tokenized_corpus = open("tokenized_corpus.txt","w")
#     # output = open("output.txt", "w")
#     i=0
#     for doc_name in  listdir(dir_path):
#         doc_path = dir_path + '/'+ doc_name
#         doc, tokenized_doc, output_dict = preprocess_document(doc_path, stemming, lower_case, lemma, stopword_removal)
#         # tokenized_doc = preprocess_document(doc_path, stemming, lower_case, lemma, stopword_removal)
#         if doc:
#             output_dict["id"] = i
#             corpus.write(str(output_dict) + "\n")
#             tokenized_corpus.write(", ".join(tokenized_doc) + "\n")
#             # output.write(str(output_dict) + "\n")
#         i=i+1
#         print(i)
#         if i==5000:
#             break

# preprocess("C:/Users/Dell-pc/Desktop/UIUC/Fall 2019/CS 510 IR/grobid_processed")

# def read_file():
#     #return tokenized_corpus and corpus.
#     c = [(ast.literal_eval(line)) for line in open("corpus.txt", "r").read().splitlines()]
#     tc = [line.split(',') for line in open("tokenized_corpus.txt", "r", encoding="ISO-8859-1").read().splitlines()]
#     # print(c)
#     # print(tc)
#     return(c, tc)

# import json
# read_file()


# split_file("corpus.txt")
# split_file("output.txt")
# split_file("tokenized_corpus.txt")
