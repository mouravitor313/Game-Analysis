import pandas as pd
from src.assistants import mario_assistant, sonic_assistant
from src.prompts.mario_prompts import prompts

class Main():
    
    dataframe = pd.read_csv('Game-Analisys/data/games_list.csv')
    dataframe = dataframe.to_string()

    def __init__(self) -> None:
        pass

    @classmethod
    def main(cls) -> None:

        message_received_from_model = '\n' + mario_assistant.add_columns_and_complete_information(prompts['complete_that_csv'], cls.dataframe)

        mario_assistant.export_csv_with_addition_information(message_received_from_model, 'Game-Analisys/data/games_data_output.csv')

if __name__ == '__main__':
    Main.main()