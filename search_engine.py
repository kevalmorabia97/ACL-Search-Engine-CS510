

def get_top_k_docs(query, k=1):
    """
    Args:
        query: string
        k: int (default: 1)
    
    Returns:
        top_k_docs: list of k documents in descending order of relevance
    """
    query = preprocess(query)

    top_k_docs = ["Doc1", "Doc2", "Doc3"]
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