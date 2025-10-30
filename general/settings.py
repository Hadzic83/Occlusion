########################################################################################################################
# Occlusion > General > Settings
# Version 2025.10.30
########################################################################################################################
# Copyright (c) 2025 Orobas
# https://www.orobas.com.au

from json import load as json_load
from os.path import dirname, join as path_join

class Settings:
    """
    Application settings.
    """

    # region Globals

    __root = dirname(dirname(__file__))
    """
    Application root directory.
    """

    # endregion

    # region Constructors

    def __init__(self) -> None:
        """
        Create new application settings.
        """

        with open(path_join(self.__root, "settings.json"), "rt") as file:
            self.__data = json_load(file)

    # endregion

    # region Properties

    @property
    def model_context(self) -> int:
        """
        Model context length.
        :return: Model context length.
        """

        return self.__data["model"]["context"]

    @property
    def model_destination(self) -> str:
        """
        Model destination path.
        :return: Model destination path.
        """

        return self.__data["model"]["destination"]

    @property
    def model_role(self) -> str:
        """
        Model role description.
        :return: Model role description.
        """

        return self.__data["model"]["role"]

    @property
    def model_source(self) -> str:
        """
        Model source URL.
        :return: Model source URL.
        """

        return self.__data["model"]["source"]

    # endregion
