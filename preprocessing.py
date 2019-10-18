from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from nltk.stem import WordNetLemmatizer
from os import listdir

lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

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
        return False

    text = re.split('\<(.*?)\>', data)
    tags = re.findall('\<(.*?)\>', data)
    tags.insert(0,'content')
    content = [item for item in text if item not in tags]
    output = dict(zip(tags,content))

    for tag, content in output.items():
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

    return(output)

def preprocess(dir_path, stemming = True, lower_case = True, lemma = True, stopword_removal = True):
    fout = "preprocessed_stemming_lemma.txt"
    fo = open(fout, "w")
    for doc_name in  listdir(dir_path):
        doc_path = dir_path + '/'+ doc_name
        processed_doc = preprocess_document(doc_path, stemming, lower_case, lemma, stopword_removal)
        if processed_doc:
            fo.write(doc_name + " " + str(processed_doc) + "\n")
    fo.close()

# Run these: 
# preprocess("C:/Users/Dell-pc/Desktop/UIUC/Fall 2019/CS 510 IR/grobid_processed", stemming = True, lower_case = True, lemma = True, stopword_removal = True)
# preprocess("C:/Users/Dell-pc/Desktop/UIUC/Fall 2019/CS 510 IR/grobid_processed", stemming = False, lower_case = True, lemma = False, stopword_removal = True)
