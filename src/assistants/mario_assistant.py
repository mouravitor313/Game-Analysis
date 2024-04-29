import openai
import pandas as pd
import io
import os

class Mario():
    API_KEY = os.getenv("API_KEY_OPENAI_MONKEY_BRANCH")
    openai.api_key = API_KEY

    @staticmethod
    def add_columns_and_complete_information(prompt: str, data: str) -> str:

        completions = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            #response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant which do not says nothing, only give what are user asking"},
                {"role": "user", "content": prompt+"\n\n"+data}
            ],
            temperature=0.3,
        )
        message_received_from_model = completions.choices[0].message.content
        return message_received_from_model

    @staticmethod
    def export_csv_with_addition_information(message_received_from_model: str, path: str) -> None:

        dataframe = pd.read_csv(io.StringIO(message_received_from_model))

        if not os.path.isfile(path):
            dataframe.to_csv(path, index=False)

        else:
            dataframe.to_csv(path, mode='a', header=False, index=False)
