import openai
import pandas as pd
import io
import os

API_KEY = os.getenv("API_KEY_OPENAI_MONKEY_BRANCH")
openai.api_key = API_KEY

dataframe = pd.read_csv('data/games_list.csv')

def add_columns_and_complete_information(prompt,data):

    completions = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant which have the same personality as Mario from Super Mario Bros. and are designed to output JSON."},
            {"role": "user", "content": prompt+"\n\n"+data}
        ],
        temperature=0.3,
    )
    message_received_from_model = completions.choices[0].message.content
    return message_received_from_model

def export_csv_with_addition_information(message_received_from_model):

    dataframe = pd.read_csv(io.StringIO(message_received_from_model))

    if not os.path.isfile('data/games_data_output'):
        dataframe.to_csv('data/games_data_output', index=False)

    else:
        dataframe.to_csv('data/games_data_output', mode='a', header=False, index=False)
