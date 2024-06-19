import openai
import pandas as pd
import os

class Sonic():
    API_KEY = os.getenv("API_KEY_OPENAI")
    openai.api_key = API_KEY

    @staticmethod
    def chat_with_Sonic(prompt: str, data: str) -> str:

        messages_default=[
                {"role": "system", "content": prompt},
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



