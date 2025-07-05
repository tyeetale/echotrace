from openai import OpenAI

class ChatEngine:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def get_response(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content.strip()