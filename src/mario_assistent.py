import os
from openai import OpenAI

API_KEY = os.getenv("API_KEY_OPENAI")
client = OpenAI(API_KEY)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Bom dia"}
  ]
)

print(completion.choices[0].message)