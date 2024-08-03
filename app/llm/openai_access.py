from app.config.config import settings
import openai

class OpenAI_Access():
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.MODEL
        self.max_tokens = settings.MAX_TOKENS
        
    def request_with_context(self, prompt, text, temperature=0):
        full_prompt = f"{prompt}{text}"
        return self.get_response(full_prompt, temperature=temperature)

    def get_response(self, prompt, temperature=0):
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=1000,
            temperature=temperature
        )
        return response.choices[0].text.strip()