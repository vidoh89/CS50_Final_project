import pandas as pd
import plotly.express as px
import logging
import os
import pathlib
from dotenv import load_dotenv
from shiny import App,Inputs,Outputs,Session, render, ui
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
            str, pathlib.Path, ui.Theme
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
        :raise ValueError: if value is not None or type(str)
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
        :raise TypeError: if value is not None or type(str)
        :raise ValueError: if value is not None and value not found in LANG_CONST


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
    @property
    def get_custom_theme(self)->Optional[Union[str,pathlib.Path,ui.Theme]]:
        """
        Controls the theme of the current page
        :return: Returns the theme for page aesthetics
        :rtype:Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]
        """
        return self._theme
    @get_custom_theme.setter
    def get_custom_theme(self,css_value:str):
        """
        Setter for page theme
        :param css_value: Holds the path or file for UI theme
        :type css_value: Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]
        :raise ValueError: If Theme path is set to an empty string or not an instance of type(str)
        :raise TypeError: If css_value is not an instance of:Options[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]
        :raise FileNotFoundError: If css_value is valid (str,pathlib.Path) but file can't be found
        :raise ValueError: If theme_path  is not a .css
        """
        if isinstance(css_value,str) and not css_value:
            self.error("Theme cannot an empty string")
            raise ValueError("Theme path cannot be an empty string")
        if not isinstance(css_value,(str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider)):
            self.error(f"Incorrect datatype for theme:accepted types:Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]:Received {type(css_value).__name__}")
            raise TypeError(f"Incorrect datatype for theme: aceeptable types<Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]>:Received {type(css_value).__name__}")


        try:
            if css_value:
                if isinstance(css_value,(str,pathlib.Path)) and not pathlib.Path(css_value).exists():
                    raise FileNotFoundError
                if isinstance(css_value, (str, pathlib.Path)):
                    theme_path = pathlib.Path(css_value)
                    if theme_path.suffix.lower() not in ".css":
                        raise ValueError

        except FileNotFoundError:
            self.error(f'Could not locate css file from:{css_value}')
            return None
        except ValueError:
            self.warning('Theme file does not have correct extension type:Example<theme.css>')
            return None

        else:
            self._theme = css_value
            self.info(f"Successfully set custom theme to {self._theme}.")
        finally:
            self.info("Theme selection completed.")


    def app_ui(self,request):
        """
        Defines the UI for the Shiny app.
        :return:
        """
        #Create path to theme or .css
        self.info("Configuring path for theme.")
        theme_path = pathlib.Path(__file__).parent/".."/"www"/"theme"/"style.css"
        return ui.page_fluid(
            ui.h2("U.S GDP Data from the FRED API"),
            ui.layout_sidebar(
                ui.sidebar("Left sidebar content",id="sidebar_left"),
                ui.output_text_verbatim("state_left"),
            )
        )

my_app_ui = FRED_GDP_UI(title="Example page title",lang="en")

app = App(my_app_ui.app_ui, None)
if __name__ =="__main__":
    app.run()