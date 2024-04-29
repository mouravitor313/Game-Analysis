import pandas as pd
from src.assistants.mario_assistant import Mario
from src.prompts.mario_prompts import prompts_mario
from src.assistants.sonic_assistant import Sonic
from src.prompts.sonic_prompts import prompts_sonic

class Main():
    
    # Mario will read that:
    input_game_list = pd.read_csv('Game-Analisys/data/games_list.csv')
    input_game_list = input_game_list.to_string()

    # Sonic will read that:
    input_populated_data_frame = pd.read_csv('Game-Analisys/data/games_data_output.csv')
    input_populated_data_frame = input_populated_data_frame.to_string()

    def __init__(self) -> None:
        pass

    @classmethod
    def main(cls) -> None:

        message_received_from_mario = Mario.add_columns_and_complete_information(prompts_mario['complete_that_csv'], cls.input_game_list)

        Mario.export_csv_with_addition_information('\n' + message_received_from_mario, 'Game-Analisys/data/games_data_output.csv')

        message_received_from_sonic = Sonic.collect_information_and_analyze(prompts_sonic['most_played_overall'], cls.input_populated_data_frame)

        print(message_received_from_sonic)


if __name__ == '__main__':
    Main.main()