from collections import defaultdict
import re
from rake_nltk import Rake

from preprocessing import preprocess_query, remove_punctuations


class SearchEngine():
    def __init__(self, model, corpus, relevance_scores_file):
        """
        model: Search Engine that has `get_top_n(query_words, corpus, n=k)` method
        relevance_scores_file: stores (query, doc_id, rel_score) in this file
        """
        self.model = model
        self.corpus = corpus
        self.relevance_scores_file = relevance_scores_file

        self.relevance_scores = defaultdict(int)
        with open(self.relevance_scores_file, 'r') as f:
            for line in f:
                query, doc_id, rel_score = line.replace('\n','').split(',')
                
                query_words = preprocess_query(query)
                if len(query_words) > 10: # long query search
                    r = Rake(min_length=1, max_length=4)
                    r.extract_keywords_from_text(query)
                    phrases = r.get_ranked_phrases()
                    query_words = ' '.join(phrases).split()

                self.relevance_scores[(tuple(query_words), int(doc_id))] += int(rel_score)

    def get_top_k_docs(self, query, k=100):
        """
        Args:
            query: string
            k: int (default: 1)
        
        Returns:
            top_k_docs: dictionary keys: titles, abstracts, ids. Each element in dict[key] is a list of k elements in descending order of relevance
        """
        query_words = preprocess_query(query)
        if len(query_words) > 10: # long query search
            r = Rake(min_length=1, max_length=4)
            r.extract_keywords_from_text(query)
            phrases = r.get_ranked_phrases()
            query_words = ' '.join(phrases).split()

        top_k_docs = self.model.get_top_n(query_words, self.corpus, n=k)

        insensitive_comparers = {}
        for qw in query_words:
            insensitive_comparers[qw] = re.compile(re.escape(qw), re.IGNORECASE)

        results = {'titles': [], 'abstracts': [], 'ids': [], 'links': []}
        relevant = {'titles': [], 'abstracts': [], 'ids': [], 'links': []}
        not_relevant = {'titles': [], 'abstracts': [], 'ids': [], 'links': []}
        for i in top_k_docs:
            abstract = i['abstract'].replace('\n','')
            if abstract == '':
                abstract = i['introduction'].replace('\n','')
            if abstract == '':
                continue

            abstract = remove_punctuations(abstract)
            
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
            
            rel_score = self.relevance_scores[(tuple(query_words), i['id'])]
            if rel_score > 0:
                relevant['titles'].append(title.title())
                relevant['abstracts'].append(abstract)
                relevant['ids'].append(i['id'])
                relevant['links'].append(i['link'])
            elif rel_score < 0:
                not_relevant['titles'].append(title.title())
                not_relevant['abstracts'].append(abstract)
                not_relevant['ids'].append(i['id'])
                not_relevant['links'].append(i['link'])
            else:
                results['titles'].append(title.title())
                results['abstracts'].append(abstract)
                results['ids'].append(i['id'])
                results['links'].append(i['link'])
        
        for key in ['abstracts', 'ids', 'titles', 'links']:
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
            f.write(','.join([str(i) for i in (query.replace(',',''), doc_id, rel_score)]) + '\n')

        query_words = preprocess_query(query)
        if len(query_words) > 10: # long query search
            r = Rake(min_length=1, max_length=4)
            r.extract_keywords_from_text(query)
            phrases = r.get_ranked_phrases()
            query_words = ' '.join(phrases).split()

        self.relevance_scores[(tuple(query_words), int(doc_id))] += int(rel_score)
