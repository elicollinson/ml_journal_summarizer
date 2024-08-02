import os
import tempfile
from autogen import ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor
from app.util.scrape_utils import ScrapeUtils
from app.config.config import settings

class ScholarlySummary(self):
    
    def __init__(self):
        self.scrape_utils = ScrapeUtils()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs = self.scrape_utils.get_docs()

    
    