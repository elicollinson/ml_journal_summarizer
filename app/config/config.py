import os
from pydantic import BaseSettings, FilePath

def getenv(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value

class Settings(BaseSettings):
    MODEL: str = getenv("MODEL", "gpt-4o-mini")
    OPENAI_API_KEY: str = getenv("OPENAI_API_KEY", "")
    MAX_TOKENS: int = getenv("MAX_TOKENS", 1000)
    EXECUTION_IMAGE: str = getenv("EXECUTION_IMAGE", "python:3.12-slim")
    EXECUTION_TIMEOUT: str = getenv("EXECUTION_TIMEOUT", 120)
    SUMMARIZE_PROMPT: str = getenv("SUMMARIZE_PROMPT", "You are a paper summarizer. You will be given a paper published in a machine learning journal. Your task is to summarize the paper while capturing the import details.\n\nFollow these rules:\n1.Ensure the grammar is correct in your response.\n2.Ensure all key conclusions from the paper are documented and supported.\n3.Do not embelish or add additional information, only summarize what is stated in the paper.\n4.Ignore references to figures and images.\n5.Respond only with the text of the summary.\n\nPaper Text:\n") # type: ignore
    TITLE_PROMPT:str = getenv("TITLE_PROMPT", "You are a title extractor. You will be given the text of a journal article published in a machine learning journal. Your task is to extract the title of the article based on the given text. Respond only with the title. If you cannot find the title, respond with 'unknown'.\n\nJournal Text:\n") # type: ignore
    PUBLICATION_DATE_PROMPT:str = getenv("PUBLICATION_DATE_PROMPT", "You are a publication date extractor. You will be given the text of a journal article published in a machine learning journal. Your task is to extract the publication date of the article based on the given text. Respond only with the publication date. If you cannot find the publication date, respond with 'unknown'.\n\nJournal Text:\n") # type: ignore
    #TODO: fix invalid escape sequence
    INGESTED_LIST_FILE: str = getenv("INGESTED_LIST_FILE", "app\\resources\ingest_list.txt")
    SOURCE_URLS: list[str] = ["https://www.jmlr.org/"]
    BASE_SOURCE_URL: str = "https://www.jmlr.org/"
settings = Settings()