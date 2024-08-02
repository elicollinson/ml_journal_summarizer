from dataclasses import dataclass

@dataclass
class Term():
    term: str
    definition: str
    
@dataclass
class NovelIdea():
    idea: str
    explanation: str

@dataclass
class ProcessedDocument():
    title: str
    publication_date: str
    text: str
    summary: str
    terms: list[Term]
    novel_ideas: list[NovelIdea]
    
@dataclass
class DocChunk():
    text: str
    vector: list[float]
    
