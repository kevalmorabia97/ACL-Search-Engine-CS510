from preprocessing import preprocess_query
import time


def get_top_k_docs(model, query, corpus, k=100):
    """
    Args:
        model: Search Engine that has `get_top_n(tokenized_query, corpus, n=k)` method
        query: string
        k: int (default: 1)
    
    Returns:
        top_k_docs: dictionary keys: titles, abstracts, ids. Each element in dict[key] is a list of k elements in descending order of relevance
    """
    tokenized_query = preprocess_query(query)
    query_words = preprocess_query(query, stemming=False, lower_case=True, lemma=False, stopword_removal=True)
    top_k_docs = model.get_top_n(tokenized_query, corpus, n=k)

    results = {'titles': [], 'abstracts': [], 'ids': []}
    for i in top_k_docs:
        abstract = i['abstract'].replace('\n','')
        if abstract == '':
            abstract = i['introduction'].replace('\n','')
        if abstract == '':
            continue
        
        doc_text = i['title'].replace('\n','').lower() + ' ' + i['abstract'].replace('\n','').lower() + ' ' + i['introduction'].replace('\n','').lower()
        query_words_found = False
        for qw in query_words:
            if qw in doc_text:
                query_words_found = True
                break 
        if not query_words_found:
            continue

        results['abstracts'].append(abstract)
        results['ids'].append(i['id'])
        results['titles'].append(i['title'].replace('\n',''))

    return results


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
