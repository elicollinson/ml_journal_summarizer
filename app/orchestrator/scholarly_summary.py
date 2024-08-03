import os
import tempfile
from autogen import ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor
from app.util.scrape_utils import ScrapeUtils
from app.config.config import settings
from app.llm.doc_processing import DocProcessing

class ScholarlySummary:
    
    def __init__(self):
        self.scrape_utils = ScrapeUtils()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs = self.scrape_utils.get_docs()
        
    def run(self):
        DocProcessing(self.docs).process_docs()

    
    