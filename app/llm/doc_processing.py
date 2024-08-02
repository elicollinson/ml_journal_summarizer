from app.model.extracted_document import ExtractedDocument
from app.model.processed_document import ProcessedDocument

class DocProcessing():
    def __init__(self, docs):
        self.docs: [ExtractedDocument] = docs
        self.processed_docs: [ProcessedDocument] = []
    
    def process_docs(self):
        for doc in self.docs:
            print(f"Processing document from {doc.url}...")
            
            #Summarize the document text
            
            #Extract title from the document
            
            #Extract publication date from the document
            
            #Extract terms from the document
            
            #Extract novel ideas from the document
            
            #Chunk the document
            
            print(f"Document processed.")   

    