import os 
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self):
        self.client =  Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-opus-4-5"
    
    def think(self, messages, system_prompt):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text