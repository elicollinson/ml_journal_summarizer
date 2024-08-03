from app.model.extracted_document import ExtractedDocument
from app.model.processed_document import ProcessedDocument
from app.llm.openai_access import OpenAI_Access
from app.config.config import settings
import openai


class DocProcessing():
    def __init__(self, docs):
        self.docs: [ExtractedDocument] = docs
        self.processed_docs: [ProcessedDocument] = []
        self.openai_access = OpenAI_Access()

    def get_summary(self, text):
        return self.openai_access.request_with_context(settings.SUMMARIZE_PROMPT, text)
    
    def get_title(self, text):
        return self.openai_access.request_with_context(settings.TITLE_PROMPT, text)
    
    def get_publication_date(self, text):
        return self.openai_access.request_with_context(settings.PUBLICATION_DATE_PROMPT, text)
    
    # def get_terms(self, text):
    #     return self.openai_access.request_with_context(settings.TERMS_PROMPT, text)
    
    # def get_novel_ideas(self, text):    
    #     return self.openai_access.request_with_context(settings.NOVEL_IDEAS_PROMPT, text)
    
    # def chunk_text(self, text):
    #     return self.openai_access.request_with_context(settings.CHUNK_PROMPT, text)
    
    def process_docs(self):
        for doc in self.docs:
            print(f"Processing document from {doc.url}...")
            
            #Summarize the document text
            summary = self.get_summary(doc.text)
            
            #Extract title from the document
            title = self.get_title(doc.text)
            
            #Extract publication date from the document
            publication_date = self.get_publication_date(doc.text)
            
            #Extract terms from the document
            # terms = self.get_terms(doc.text)
            
            #Extract novel ideas from the document
            
            #Chunk the document
            print(f"Title: {title}")
            print(f"Publication Date: {publication_date}")
            print(f"Summary: {summary}")
            
            print(f"Document processed.")   


    