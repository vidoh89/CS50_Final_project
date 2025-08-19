import pandas as pd
import plotly.express as px
import logging
import os
import pathlib
from dotenv import load_dotenv
from shiny import App, render, ui
from data.fred_data import FRED_API
from logs.logs import Logs
from typing import Optional, Union
from htmltools import TagList, div

# Load environment variables
load_dotenv()


class FRED_GDP_UI(Logs):
    """
    Encapsulates UI and server logic for fred_data module
    """

    LANG_CONST = tuple(["en", "es", "fr", "de", "ja", "ko", "zh-CN", "zh-TW"])

    def __init__(
        self,
        title: Optional[str] = None,
        lang: Optional[str] = None,
        theme: Optional[Union[
            str, pathlib.Path, ui.Theme, ui.page_fluid.ThemeProvider
        ]] = None,
        **kwargs,
    ):
        """

        :param title: Holds the browser window title(defaults to host URL)
        :type title: Optional[str]
        :param lang: Used for the lang in the <html> tag (..e.g.,"en","ko")
        :type lang: Optional[str]
        :param theme: The path, URL, or object for a custom Shiny theme
        :type theme: Optional[Union[
            str, pathlib.Path, ui.Theme, ui.page_fluid.ThemeProvider]]
        """
        super().__init__(name="FRED_GDP_UI", level=logging.INFO)
        # Initialize private variables to instance variables
        self.info("Initializing instance variables for ui")
        self._title = title
        self._lang = lang
        self._theme = theme
        self.info("Variable initialization successful.")

    @property
    def ui_page_title(self) -> Optional[str]:
        """
        Getter for browser title window
        :return: Returns the title for page browser window
        """
        return self._title

    @ui_page_title.setter
    def ui_page_title(self, value: Optional[str]):
        """
        Setter for browser title window
        :param value: Holds the title for browser
        :type value: Optional[str]
        """
        if value is not None and not isinstance(value, str):
            self.error("Failed to set page title")
            raise ValueError(f"Ui page title must be Union[str,None] not:{type(value)}")

        self._title = value
        self.info(f"Ui page title set to: {self._title}")

    @property
    def ui_lang_selector(self)->Optional[str]:
        """
        Getter for language that will be displayed on page
        :return: language(...e.g."en" for English) displayed on page
        """
        return self._lang

    @ui_lang_selector.setter
    def ui_lang_selector(self, value:Optional[str]):
        """
        Setter for page language.
        Choices:LANG_CONST = tuple(["en","es","fr","de","ja","ko","zh-CN","zh-TW"])
        :param value: Holds the original page selection value,(...e.g.,"en")
        :type value: Optional[str]


        """
        if value is not None and not isinstance(value,str):

            self.error(f"Language input must be a string or None, not: {type(value).__name__}")
            raise TypeError(f"Language input must be a string or None, not {type(value).__name__}.")
        if value is not None and value not in self.LANG_CONST:
            accepted_lang = ",".join(self.LANG_CONST)
            self.error(f"Invalid language code {value}. Please select from acceptable choices.")
            raise ValueError(f"Language input incompatible. Please select from acceptable choices:<html lang={accepted_lang}>")
        self._lang = value
        self.info(f"Successfully set <html> language to: {self._lang}")

    def app_ui(self):
        return ui.page_fluid(...)
