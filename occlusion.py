########################################################################################################################
# Occlusion
# Version 2025.10.30
########################################################################################################################
# Copyright (c) 2025 Orobas
# https://www.orobas.com.au

from general.model import Model
from general.settings import Settings
from general.terminal import Terminal
from sys import exit
from typing import List

class Occlusion:
    """
    Occlusion application.
    """

    # region Constructors

    def __init__(self) -> None:
        """
        Create a new occlusion application.
        """

        self.__settings = Settings()
        self.__terminal = Terminal()
        self.__model = Model()

        while True:
            option = self.__terminal.options(self.options)

            if option == self.option_query_index:
                print(self.__model.query_one())
            elif option == self.option_exit_index:
                print("Goodbye.")
                exit(0)
            else:
                raise RuntimeError("Invalid option.")

    # endregion

    # region Properties

    @property
    def option_exit_index(self) -> int:
        """
        Exit option index.
        :return: Exit option index.
        """

        return self.options.index(self.option_exit_label)

    @property
    def option_exit_label(self) -> str:
        """
        Exit option label.
        :return: Exit option label.
        """

        return "Exit"

    @property
    def option_query_index(self) -> int:
        """
        Query option index.
        :return: Query option index.
        """

        return self.options.index(self.option_query_label)

    @property
    def option_query_label(self) -> str:
        """
        Query option label.
        :return: Query option label.
        """

        return "General Query"

    @property
    def options(self) -> List[str]:
        """
        List of main menu options.
        :return: List of main menu options.
        """

        return [
            self.option_query_label,
            self.option_exit_label,
        ]

    # endregion

if __name__ == "__main__":
    print("=========")
    print("Occlusion")
    print("=========")
    Occlusion()
