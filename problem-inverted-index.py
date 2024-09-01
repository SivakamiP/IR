import streamlit as st
import re
from collections import defaultdict

# Function to tokenize text
def tokenize(text):
    """Tokenize the input text into a set of lowercase words."""
    return set(re.findall(r'\b\w+\b', text.lower()))

# Function to build an inverted index
def build_inverted_index(docs):
    """Build an inverted index from a collection of documents."""
    index = defaultdict(set)
    for doc_id, text in docs.items():
        words = tokenize(text)
        for word in words:
            index[word].add(doc_id)
    return index

# Function to perform Boolean retrieval
def boolean_retrieval(index, query, documents):
    """Perform Boolean retrieval based on the inverted index."""
    query = query.lower()
    tokens = re.findall(r'\b\w+\b', query)
    
    if 'and' in tokens or 'not' in tokens:
        result_docs = set(documents.keys())
    else:
        result_docs = set()
    
    if 'and' in tokens:
        terms = query.split(' and ')
        for term in terms:
            term = term.strip()
            result_docs = result_docs.intersection(index.get(term, set()))
    
    elif 'or' in tokens:
        terms = query.split(' or ')
        for term in terms:
            term = term.strip()
            result_docs = result_docs.union(index.get(term, set()))
    
    elif 'not' in tokens:
        terms = query.split(' not ')
        if len(terms) == 2:
            result_docs = index.get(terms[0].strip(), set())
            term_to_exclude = terms[1].strip()
            result_docs = result_docs.difference(index.get(term_to_exclude, set()))
    
    else:
        for token in tokens:
            result_docs = result_docs.union(index.get(token, set()))
    
    return result_docs

# Streamlit UI
st.title("Boolean Retrieval System")

# Upload document files
uploaded_files = st.file_uploader("Upload Documents", type=["txt"], accept_multiple_files=True)


if uploaded_files:
    query = st.text_input("Enter your Boolean query:")
    documents = {}
    for i, uploaded_file in enumerate(uploaded_files):
        file_text = uploaded_file.read().decode("utf-8")
        documents[f"doc{i+1}"] = file_text
    
    # Build the inverted index
    inverted_index = build_inverted_index(documents)
    
    # Perform Boolean retrieval
    results = boolean_retrieval(inverted_index, query, documents)
    
    # Display results
    st.write(f"Query: '{query}'")
    st.write("Results:")
    
    if results:
        st.write("Matched Document IDs:")
        st.write(", ".join(results))  
    else:
        st.write("No documents matched the query.")
else:
    st.write("Please upload documents and enter a query.")
