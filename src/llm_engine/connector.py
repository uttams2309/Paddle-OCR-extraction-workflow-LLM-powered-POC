from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv() # Load API key from .env

class LLMClient:
    def __init__(self, config):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = config['llm']['model']
        self.temperature = config['llm']['temperature']

    def enhance_extraction(self, ocr_text, system_prompt):
        """
        Sends OCR text to LLM for cleaning and extraction.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Here is the raw OCR text:\n\n{ocr_text}"}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"} # Forces JSON output
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"