import pandas as pd
from src.assistants import mario_assistant, sonic_assistant
from src.prompts.mario_prompts import prompts

class Main():
    
    dataframe = pd.read_csv('Game-Analisys/data/games_list.csv')

    def __init__(self):
        pass

    @classmethod
    def main(cls):

        message_received_from_model = mario_assistant.add_columns_and_complete_information(prompts['complete_that_csv'], cls.dataframe)

        mario_assistant.add_columns_and_complete_information(message_received_from_model)


if __name__ == '__main__':
    Main.main()