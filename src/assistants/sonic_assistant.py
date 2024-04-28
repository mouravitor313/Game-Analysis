import openai
import pandas as pd
import os

API_KEY = os.getenv("API_KEY_OPENAI_MONKEY_BRANCH")
openai.api_key = API_KEY

def collect_information_and_analyze(prompt: str) -> str:

    data = pd.read_csv('data/games_data_output')
    completions = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant which have the same personality as Sonic The Hedgehog and are designed to output JSON."},
            {"role": "user", "content": prompt+"\n\n"+data}
        ],
        temperature=0.3,
    )
    message_received_from_model = completions.choices[0].message.content
    return message_received_from_model

