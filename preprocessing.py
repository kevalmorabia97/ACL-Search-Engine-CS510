from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from nltk.stem import WordNetLemmatizer
from os import listdir
import yaml

lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

def preprocess_query(query_string, stemming = True, lower_case = True, lemma = True, stopword_removal = True):
    #return processed tokenized query
    if lower_case:
        query_string = query_string.lower()
        new_text = tokenizer.tokenize(query_string)
    else:
        new_text = tokenizer.tokenize(query_string)
    if stopword_removal:
        new_text = [word for word in new_text if word not in stopwords.words('english')]
    if stemming:
        new_text = [porter_stemmer.stem(word) for word in new_text]
    if lemma:
        new_text = [lemmatizer.lemmatize(word) for word in new_text]
    return(new_text)

def preprocess_document(doc_path, stemming, lower_case, lemma, stopword_removal):
    '''
    :param doc_path: Directory path for document, ex: "C:/Users/Tara/Desktop/grobid_processed/docname.xml"
    :param stemming: True -> Do stemming for words in doc
    :param lower_case: True -> Convert all words to lowercase
    :param lemma: True -> Do lemmatization for words in doc
    :param stopword_removal: True -> Remove stopwords from doc
    :return: dict {content: [w1,w2..], figcaptions: [w1,w2..], tablecaptions: [w1,w2..], title: [w1,w2..], abstract: [w1,w2..], introduction: [w1,w2..]}
    '''
    try:
        with open(doc_path, 'r') as f:
            data = f.read()
        f.close()
    except:
        return (False,False,False)

    text = re.split('\<(.*?)\>', data)
    tags = re.findall('\<(.*?)\>', data)
    tags.insert(0,'content')
    content = [item for item in text if item not in tags]
    output = dict(zip(tags,content))
    output = {key: output[key] for key in {'title', 'abstract', 'introduction'}}
    temp = {key: output[key] for key in {'title', 'abstract', 'introduction'}}
    corpus = []

    for tag, content in output.items():
        corpus.append(content)
        if lower_case:
            content = content.lower()
            new_text = tokenizer.tokenize(content)
        else:
            new_text = tokenizer.tokenize(content)

        if stopword_removal:
            new_text = [word for word in new_text if word not in stopwords.words('english')]

        if stemming:
            new_text = [porter_stemmer.stem(word) for word in new_text]

        if lemma:
            new_text = [lemmatizer.lemmatize(word) for word in new_text]
        output[tag] = new_text

    corpus = " ".join(corpus).replace("\n",'')
    tokenized_corpus = [val for sublist in output.values() for val in sublist]
    return(corpus, tokenized_corpus, temp)

def preprocess(dir_path, stemming = True, lower_case = True, lemma = True, stopword_removal = True):
    corpus = open("corpus.txt", "w")
    tokenized_corpus = open("tokenized_corpus.txt","w")
    output = open("output.txt", "w")
    i=0
    for doc_name in  listdir(dir_path):
        doc_path = dir_path + '/'+ doc_name
        doc, tokenized_doc, output_dict = preprocess_document(doc_path, stemming, lower_case, lemma, stopword_removal)
        if doc:
            corpus.write(doc + "\n")
            tokenized_corpus.write(str(tokenized_doc) + "\n")
            output.write(str(output_dict) + "\n")
        i=i+1
        print(i)

# preprocess("C:/Users/Dell-pc/Desktop/UIUC/Fall 2019/CS 510 IR/grobid_processed")

def read_file(corpus = "corpus.txt", tokenized_corpus = "tokenized_corpus.txt"):
    #return tokenized_corpus and corpus.
    c = open(corpus, "r")
    tc = open(tokenized_corpus, "r")
    return(c.read().splitlines(), list(tc.read().splitlines()))


