########################################################################################################################
# Occlusion > General > Model
# Version 2025.10.30
########################################################################################################################
# Copyright (c) 2025 Orobas
# https://www.orobas.com.au

from general.settings import Settings
from general.terminal import Terminal
from json import dumps as json_dumps
from llama_cpp import Llama
from os.path import abspath, isfile
from typing import List

class Model:
    """
    Large language model.
    """

    # region Globals

    __verbose = False
    """
    True to show verbose debugging information; otherwise, false.
    """

    # endregion

    # region Constructors

    def __init__(self) -> None:
        """
        Create a new large language model.
        """

        self.__settings = Settings()
        self.__terminal = Terminal()

        model_path = abspath(self.__settings.model_destination)

        if not isfile(abspath(model_path)):
            print("Downloading the AI model...")
            self.__terminal.download(
                self.__settings.model_source,
                abspath(self.__settings.model_destination),
            )

        print("Loading the AI model...")
        self.__model = self.__terminal.progress(
            lambda: Llama(
                model_path = model_path,
                n_gpu_layers = -1,
                n_ctx = self.__settings.model_context,
                verbose = self.__verbose,
            )
        )

    # endregion

    # region Methods

    def query(self, message: str = "") -> List[str]:
        """
        Query the model.
        :param message: Query message, or blank to prompt the user for input.
        :return: List of responses.
        """

        if not message:
            message = self.__terminal.input_string("Query", False)

        response = self.__terminal.progress(
            lambda: self.__model.create_chat_completion(
                messages = [
                    {"role": "system", "content": self.__settings.model_role},
                    {"role": "user", "content": message},
                ],
            ),
        )

        if self.__verbose:
            print(json_dumps(response, indent=4))

        responses = []

        if "choices" in response:
            for choice in response["choices"]:
                responses.append(choice["message"]["content"])

        return responses

    def query_one(self, message: str = "") -> str:
        """
        Query the model and return exactly one response.
        :param message: Query message, or blank to prompt the user for input.
        :return: Response.
        """

        responses = self.query(message)
        return responses[0] if responses else "No response."

    # endregion
