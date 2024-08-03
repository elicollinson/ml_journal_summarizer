from app.config.config import settings
from openai import OpenAI, OpenAIError

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class OpenAI_Access():
    def __init__(self):
        self.model = settings.MODEL
        self.max_tokens = settings.MAX_TOKENS

    def request_with_context(self, prompt, text, temperature=0):
        full_prompt = f"{prompt}{text}"
        return self.get_response(full_prompt, temperature=temperature)

    def get_response(self, prompt, temperature=0, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                response = client.completions.create(
                    engine=self.model,
                    prompt=prompt,
                    max_tokens=self.max_tokens,
                    temperature=temperature
                )
                return response.choices[0].text.strip()
            except OpenAIError as e:
                retries += 1
                if retries == max_retries:
                    raise
                sleep_time = (2 ** retries) + random.uniform(0, 1)
                time.sleep(sleep_time)
                print(f"Retrying ({retries}/{max_retries}) after error: {e}")