from datetime import date

class ExtractedDocument():
    def __init__(self, text, url):
        self.text = text
        self.extracted_date = date.today()
        self.url = url