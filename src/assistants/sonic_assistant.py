import openai
import pandas as pd
import os

class Sonic():
    API_KEY = os.getenv("API_KEY_OPENAI")
    openai.api_key = API_KEY

    @staticmethod
    def collect_information_and_analyze(prompt: str, data: str) -> str:

        completions = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            # response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant which have the same personality as Sonic The Hedgehog."},
                {"role": "user", "content": prompt+"\n\n"+data}
            ],
            temperature=0.3,
        )
        message_received_from_model = completions.choices[0].message.content
        return message_received_from_model
    
    @staticmethod
    def chat_with_Sonic(data: str) -> str:

        messages_default=[
                {"role": "system", "content": "You are a helpful assistant which have the same personality as Sonic The Hedgehog. Remember to talk like Sonic every time."},
                {"role": "user", "content": "Read that csv, I want to talk with you about that data"+"\n\n"+data}
            ]
        
        while(True):
            completions = openai.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages_default,
                temperature=0.5,
            )

            message_received_from_model = completions.choices[0].message.content
            messages_default.append({"role": "assistant", "content": message_received_from_model})
            print("Sonic: ", message_received_from_model)
            
            user_message = input("You: ")
            messages_default.append({"role": "user", "content": user_message})



