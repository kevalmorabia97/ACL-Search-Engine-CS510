

def get_top_k_docs(query, k=1):
    """
    Args:
        query: string
        k: int (default: 1)
    
    Returns:
        top_k_docs: dictionary keys: titles, abstracts, urls, ids. Each element in dict[key] is a list of k elements in descending order of relevance
    """
    query = preprocess(query)

    top_k_docs = {"titles":["WHY NLP SHOULD MOVE INTO IAS","NLP Lean Programming Framework: Developing NLP Applications More Effectively","The NLP Role in Animated Conversation for CALL","The MultiTal NLP tool infrastructure","SiSSA -An Infrastructure for NLP Application Development","On the Role of NLP in Linguistics","Blueprint for a High Performance NLP Infrastructure","Kathaa: A Visual Programming Framework for NLP Applications","The glass ceiling in NLP","ITU Turkish NLP Web Service"],"abstracts":["The paper introduces the ways in which methods and resources of natural language processing <b>(NLP)</b> can be fruitfully employed in the domain of information assurance and security (IAS). IAS may soon claim a very prominent status both conceptually and in terms of future funding for <b>NLP,</b> alongside or even instead of established applications, such as machine translation (MT).","This paper presents <b>NLP</b> Lean Programming framework <b>(NLPf),</b> a new framework for creating custom natural language processing <b>(NLP)</b> models and pipelines by utilizing common software development build systems. ","Language learning is a relatively new application for natural language processing <b>(NLP)</b> and for intelligent tutoring and learning environments (ITLEs). <b>NLP</b> has a crucial role to play in foreign language ITLEs, whether they are designed for explicit or implicit learning of the vocabulary and grammar.","This paper gives an overview of the MultiTal project, which aims to create a research infrastructure that ensures long-term distribution of <b>NLP</b> tools descriptions. The goal is to make <b>NLP</b> tools more accessible and usable to end-users of different disciplines.","Recently there has been a growing interest in infrastructures for sharing <b>NLP</b> tools and resources. This paper presents SiSSA, a project that aims at developing an infrastructure for prototyping, editing and validation of <b>NLP</b> application architectures.","This paper summarizes some of the applications of <b>NLP</b> techniques in various linguistic sub-fields, and presents a few examples that call for a deeper engagement between the two fields.","Natural Language Processing <b>(NLP)</b> system developers face a number of new challenges. Interest is increasing for real-world systems that use <b>NLP</b> tools and techniques.","In this paper, we present Kathaa 1 , an open source web based Visual Programming Framework for <b>NLP</b> applications.","In this paper, we provide empirical evidence based on a rigourously studied mathematical model for bi-populated networks, that a glass ceiling within the field of <b>NLP</b> has developed since the mid 2000s.","We present a natural language processing <b>(NLP)</b> platform, namely the &quot;ITU Turk-ish <b>NLP</b> Web Service&quot; by the natural language processing group of Istanbul Technical University. The platform (available at <b>tools.nlp.itu.edu.tr)</b> operates as a SaaS (Software as a Service) and provides the researchers and the students the state of the art <b>NLP</b> tools in many layers: preprocessing, morphology, syntax and entity recognition."],"urls":["http://www.aclweb.org/anthology/W02-1303.pdf","http://www.aclweb.org/anthology/N18-5001.pdf","http://www.aclweb.org/anthology/A97-1019.pdf","http://www.aclweb.org/anthology/W16-4021.pdf","http://www.aclweb.org/anthology/W01-1505.pdf","http://www.aclweb.org/anthology/W10-2103.pdf","http://www.aclweb.org/anthology/W03-0806.pdf","http://www.aclweb.org/anthology/N16-3019.pdf","http://www.aclweb.org/anthology/D18-1301.pdf","http://www.aclweb.org/anthology/E14-2001.pdf"],"ids":["paperidb'W021303'","paperidb'N185001'","paperidb'A971019'","paperidb'W164021'","paperidb'W011505'","paperidb'W102103'","paperidb'W030806'","paperidb'N163019'","paperidb'D181301'","paperidb'E142001'"]}
    ## TODO ##
    ## Decide on a format of return k documents

    return top_k_docs


def preprocess(doc):
    """
    Args:
        input: string
    
    Returns:
        proprocessed_input: string/list of tokens ???
    """
    return doc


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