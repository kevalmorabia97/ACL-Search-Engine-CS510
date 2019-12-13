from collections import defaultdict
import re

from preprocessing import preprocess_query


class SearchEngine():
    def __init__(self, model, corpus, relevance_scores_file):
        """
        model: Search Engine that has `get_top_n(tokenized_query, corpus, n=k)` method
        relevance_scores_file: stores (query, doc_id, rel_score) in this file
        """
        self.model = model
        self.corpus = corpus
        self.relevance_scores_file = relevance_scores_file

        self.relevance_scores = defaultdict(int)
        with open(self.relevance_scores_file, 'r') as f:
            for line in f:
                query, doc_id, rel_score = line.replace('\n','').split(',')
                self.relevance_scores[(tuple(preprocess_query(query)), int(doc_id))] += int(rel_score)

    def get_top_k_docs(self, query, k=100):
        """
        Args:
            query: string
            k: int (default: 1)
        
        Returns:
            top_k_docs: dictionary keys: titles, abstracts, ids. Each element in dict[key] is a list of k elements in descending order of relevance
        """
        tokenized_query = preprocess_query(query)
        query_words = preprocess_query(query, stemming=False, lower_case=True, lemma=False, stopword_removal=True)
        top_k_docs = self.model.get_top_n(tokenized_query, self.corpus, n=k)

        insensitive_comparers = {}
        for qw in query_words:
            insensitive_comparers[qw] = re.compile(re.escape(qw), re.IGNORECASE)

        results = {'titles': [], 'abstracts': [], 'ids': []}
        relevant = {'titles': [], 'abstracts': [], 'ids': []}
        not_relevant = {'titles': [], 'abstracts': [], 'ids': []}
        for i in top_k_docs:
            abstract = i['abstract'].replace('\n','')
            if abstract == '':
                abstract = i['introduction'].replace('\n','')
            if abstract == '':
                continue
            
            title = i['title'].replace('\n','')
            if title == '':
                continue

            doc_text = title.lower() + ' ' + abstract.lower() + ' ' + i['introduction'].replace('\n','').lower()
            query_words_found = False
            for qw in query_words:
                if qw in doc_text:
                    query_words_found = True
                    break 
            if not query_words_found:
                continue
            
            # Bold mark query words in abstract
            for qw in query_words:
                abstract = insensitive_comparers[qw].sub('<b>' + qw + '</b>', abstract)
            
            rel_score = self.relevance_scores[(tuple(tokenized_query), i['id'])]
            if rel_score > 0:
                relevant['abstracts'].append(abstract)
                relevant['ids'].append(i['id'])
                relevant['titles'].append(title.title())
            elif rel_score < 0:
                not_relevant['abstracts'].append(abstract)
                not_relevant['ids'].append(i['id'])
                not_relevant['titles'].append(title.title())
            else:
                results['abstracts'].append(abstract)
                results['ids'].append(i['id'])
                results['titles'].append(title.title())
        
        for key in ['abstracts', 'ids', 'titles']:
            results[key] = relevant[key] + results[key] + not_relevant[key]

        return results

    def store_relevance_judgements(self, query, doc_id, rel_score):
        """
        Args:
            query: str
            doc_id: unique ID corresponding to a document
            rel_score: -1 (not rel) or 1 (rel)
        """
        if rel_score not in ['-1','1']:
            print('Invalid Relevance Feedback:', rel_score)
            return
        
        with open(self.relevance_scores_file, 'a') as f:
            f.write(','.join([str(i) for i in (query, doc_id, rel_score)]) + '\n')

        self.relevance_scores[(tuple(preprocess_query(query)), int(doc_id))] += int(rel_score)
