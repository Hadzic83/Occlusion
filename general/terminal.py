########################################################################################################################
# Occlusion > General > Terminal
# Version 2025.10.30
########################################################################################################################
# Copyright (c) 2025 Orobas
# https://www.orobas.com.au

from concurrent.futures import ThreadPoolExecutor
from itertools import cycle as itertools_cycle
from os import makedirs
from os.path import abspath, dirname, isdir, isfile
from requests import get as requests_get, Response
from subprocess import run as subprocess_run
from sys import platform
from threading import Event as ThreadingEvent, Thread
from time import sleep
from typing import Any, Callable, List

# noinspection PyMethodMayBeStatic
class Terminal:
    """
    Terminal functions.
    """

    # region Globals

    __chunk = 1048576
    """
    Download chunk size.
    """

    __threads = 8
    """
    Maximum number of threads to use.
    """

    # endregion

    # region Properties

    @property
    def is_linux(self) -> bool:
        """
        Determines whether the current operating system is Linux.
        :return: True if the current operating system is Linux; otherwise, false.
        """

        return platform in ("linux", "linux2")

    @property
    def is_macos(self) -> bool:
        """
        Determines whether the current operating system is macOS.
        :return: True if the current operating system is macOS; otherwise, false.
        """

        return platform == "darwin"

    @property
    def is_windows(self) -> bool:
        """
        Determines whether the current operating system is Windows.
        :return: True if the current operating system is Windows; otherwise, false.
        """

        return platform in ("cygwin", "msys", "win32")

    # endregion

    # region Methods

    def clear(self) -> None:
        """
        Clear the terminal.
        """

        if self.is_windows:
            subprocess_run("cls")
        elif self.is_linux or self.is_macos:
            subprocess_run("clear")
        else:
            print("\n" * 120)

    def download(self, source: str, destination: str) -> None:
        """
        Download a file with a progress indicator.
        :param source: Source URL.
        :param destination: Destination path.
        """

        directory = dirname(abspath(destination))
        makedirs(directory, exist_ok=True)

        response = requests_get(source, stream=True)
        response.raise_for_status()
        size = int(response.headers.get("content-length", 0))

        if not size:
            self.__download_indeterminate__(destination, response)
        else:
            total = 0

            with open(destination, "wb") as file:
                for data in response.iter_content(chunk_size=self.__chunk):
                    file.write(data)
                    total += len(data)
                    print(f"{int((total / size) * 100)}%", end="\r", flush=True)

            print(" " * 8, end="\r", flush=True)

    def __download_indeterminate__(self, destination: str, response: Response) -> None:
        """
        Download a file with an indeterminate progress indicator.
        :param destination: Destination path.
        :param response: Web response.
        """

        with open(destination, "wb") as file:
            self.progress(lambda: file.write(response.content))

    def input_directory(self, prompt: str, directory_must_exist: bool = None) -> str:
        """
        Prompts the user to enter a directory path.
        :param prompt: Message prompt to be displayed.
        :param directory_must_exist: True if the directory must exist, false if it must not exist, or otherwise none.
        :return: The directory path entered by the user.
        """

        if not prompt.endswith(": "):
            prompt += ": "

        while True:
            value = input(prompt)

            try:
                if directory_must_exist:
                    if isdir(value):
                        return abspath(value)
                elif directory_must_exist is False:
                    if not isdir(value):
                        return abspath(value)
                else:
                    return abspath(value)
            except OSError:
                pass

            print("Please enter a valid response.")

    def input_file(self, prompt: str, file_must_exist: bool = None) -> str:
        """
        Prompts the user to enter a file path.
        :param prompt: Message prompt to be displayed.
        :param file_must_exist: True if the file must exist, false if it must not exist, or otherwise none.
        :return: The file path entered by the user.
        """

        if not prompt.endswith(": "):
            prompt += ": "

        while True:
            value = input(prompt)

            try:
                if file_must_exist:
                    if isfile(value):
                        return abspath(value)
                elif file_must_exist is False:
                    if not isfile(value):
                        return abspath(value)
                else:
                    return abspath(value)
            except OSError:
                pass

            print("Please enter a valid response.")

    def input_integer(self, prompt: str, minimum: int = None, maximum: int = None) -> int:
        """
        Prompts the user to enter an integer.
        :param prompt: Message prompt to be displayed.
        :param minimum: Minimum value, or none for no minimum.
        :param maximum: Maximum value, or none for no maximum.
        :return: The integer entered by the user.
        """

        if not prompt.endswith(": "):
            prompt += ": "

        while True:
            try:
                value = int(input(prompt).strip())

                if (minimum is None or value >= minimum) and (maximum is None or value <= maximum):
                    return value
            except ValueError:
                pass

            print("Please enter a valid response.")

    def input_string(self, prompt: str, can_be_empty: bool = True) -> str:
        """
        Prompts the user to enter a string.
        :param prompt: Message prompt to be displayed.
        :param can_be_empty: True if the string can be empty; otherwise, false.
        :return: The string entered by the user.
        """

        if not prompt.endswith(": "):
            prompt += ": "

        while True:
            value = input(prompt).strip()

            if can_be_empty or value:
                return value

            print("Please enter a valid response.")

    def options(self, options: List[str]) -> int:
        """
        Prompts the user to select an option.
        :param options: List of options.
        :return: The index of the selected option.
        """

        print("Select an option:")

        minimum = 1
        maximum = len(options) + 1
        length = len(str(maximum))

        for index in range(len(options)):
            value = str(index + 1).rjust(length, " ")
            print(f"  {value}. {options[index]}")

        return self.input_integer("Selection", minimum, maximum) - 1

    def progress(self, method: Callable[[], Any]) -> Any:
        """
        Run a method with an indeterminate progress indicator.
        :param method: Method to run.
        :return: The output of the method.
        """

        stop = ThreadingEvent()

        animation = Thread(target=self.__progress_animation__, args=(stop,))
        animation.daemon = True
        animation.start()

        with ThreadPoolExecutor(max_workers=self.__threads) as executor:
            future = executor.submit(method)

        stop.set()
        animation.join()

        return future.result()

    def __progress_animation__(self, stop: ThreadingEvent) -> None:
        """
        Display an indeterminate progress indicator.
        :param stop: Thread stop event.
        """

        for dots in itertools_cycle([".  ", ".. ", "..."]):
            if stop.is_set():
                print(" " * 16, end="\r", flush=True)
                break

            print(f"Processing{dots}", end="\r", flush=True)
            sleep(1)

        print(" " * 16, end="\r", flush=True)

    # endregion
