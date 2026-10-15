"""
Write a function called get_valid_documents(documents) that:
- Accepts a list of dictionaries.
- Returns only documents whose status is "valid".
- Handles an empty list.
- Does not modify the original list.
- Returns the result to the caller rather than printing it.
"""


#1 Simple return using for loop
def get_valid_documents(documents):
    valid_doc=[]
    if not documents:
        return []

    for doc in documents:
        if doc.get("status")=="valid":
            valid_doc.append(doc)
    return valid_doc

#2 Return using list comprehension
def get_valid_documents_comprehension(documents):

    valid_doc=[doc for doc in documents if doc.get("status")=="valid"]
      
    return valid_doc

#3 Return using names list comprehension
def get_valid_documents_names(documents):

    valid_doc_name=[doc["name"] for doc in documents if doc.get("status")=="valid"]
      
    return valid_doc_name

#4 Return using unique names generator expression
def get_valid_documents_unique_names(documents):

    valid_doc_name=sorted(list(set(doc["name"] for doc in documents if doc.get("status")=="valid")))
      
    return valid_doc_name





documents = [
    {"name": "COREP C07", "version": "2025.1", "status": "valid"},
    {"name": "COREP C07", "version": "2025.2", "status": "valid"},
    {"name": "FINREP F01", "version": "2025.1", "status": "valid"},
    {"name": "FINREP F01", "version": "2025.3", "status": "invalid"},
]



results=get_valid_documents_unique_names(documents=documents)
print(results)