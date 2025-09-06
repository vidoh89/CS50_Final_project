import pandas as pd
import plotly.express as px
import logging
import os
import plotly.graph_objects as go
import pathlib
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from data.fred_data import FRED_API
from logs.logs import Logs
from typing import Optional, Union
from app_ui.navbar import Navbar
from htmltools import TagList, div
from shinywidgets import output_widget, render_widget
from utils.fred_data_cleaner import Fred_Data_Cleaner
from app_ui.graph_data import Graph_For_Data
from server import app_server

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

        # Instantiate the Navbar
        self.navbar = Navbar()

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
    def ui_lang_selector(self) -> Optional[str]:
        """
        Getter for language that will be displayed on page
        :return: language(...e.g."en" for English) displayed on page
        """
        return self._lang

    @ui_lang_selector.setter
    def ui_lang_selector(self, value: Optional[str]):
        """
        Setter for page language.
        Choices:LANG_CONST = tuple(["en","es","fr","de","ja","ko","zh-CN","zh-TW"])
        :param value: Holds the original page selection value,(...e.g.,"en")
        :type value: Optional[str]
        :raise TypeError: if value is not None or type(str)
        :raise ValueError: if value is not None and value not found in LANG_CONST


        """
        if value is not None and not isinstance(value, str):
            self.error(f"Language input must be a string or None, not: {type(value).__name__}")
            raise TypeError(f"Language input must be a string or None, not {type(value).__name__}.")
        if value is not None and value not in self.LANG_CONST:
            accepted_lang = ",".join(self.LANG_CONST)
            self.error(f"Invalid language code {value}. Please select from acceptable choices.")
            raise ValueError(
                f"Language input incompatible. Please select from acceptable choices:<html lang={accepted_lang}>")
        self._lang = value
        self.info(f"Successfully set <html> language to: {self._lang}")

    @property
    def get_custom_theme(self) -> Optional[Union[str, pathlib.Path, ui.Theme]]:
        """
        Controls the theme of the current page
        :return: Returns the theme for page aesthetics
        :rtype:Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]
        """
        return self._theme

    @get_custom_theme.setter
    def get_custom_theme(self, css_value: str):
        """
        Setter for page theme
        :param css_value: Holds the path or file for UI theme
        :type css_value: Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]
        :raise ValueError: If Theme path is set to an empty string or not an instance of type(str)
        :raise TypeError: If css_value is not an instance of:Options[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]
        :raise FileNotFoundError: If css_value is valid (str,pathlib.Path) but file can't be found
        :raise ValueError: If theme_path  is not a .css
        """
        if isinstance(css_value, str) and not css_value:
            self.error("Theme cannot an empty string")
            raise ValueError("Theme path cannot be an empty string")
        if not isinstance(css_value, (str, pathlib.Path, ui.Theme, ui.page_fluid.ThemeProvider)):
            self.error(
                f"Incorrect datatype for theme:accepted types:Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]:Received {type(css_value).__name__}")
            raise TypeError(
                f"Incorrect datatype for theme: aceeptable types<Optional[Union[str,pathlib.Path,ui.Theme,ui.page_fluid.ThemeProvider]]>:Received {type(css_value).__name__}")

        try:
            if css_value:
                if isinstance(css_value, (str, pathlib.Path)) and not pathlib.Path(css_value).exists():
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

    def app_ui(self, request):
        """
        Defines the UI for the Shiny app.
        :return:
        """
        # Create path to theme or .css
        self.info("Configuring path for theme.")
        current_file_dir = pathlib.Path(__file__).parent
        theme_path = current_file_dir / "www" / "theme" / "style.css"
        configured_theme = None
        if theme_path.exists():
            configured_theme = theme_path
            self.info(f"Theme loaded from {theme_path}")
        else:
            self.warning(f"Theme file not found at {theme_path}. Using default theme.")
        home_nav_panel = self.navbar.ui_generator()
        return ui.page_navbar(
            home_nav_panel,
            ui.nav_panel(
                "GDP Data Plot",
                ui.h2("US Real GDP and Quarterly Growth Rate"),
                output_widget("gdp_plot")
            ),
            self.navbar.ui_generator(),
            title=self.ui_page_title,
            lang=self.ui_lang_selector,
            theme=configured_theme,
        )


my_app_ui = FRED_GDP_UI(title="Go GDP", lang="en")


# Server Logic
def server(input: Inputs, output: Outputs, session: Session):
    fred_api_logger = Logs(name="FRED_API_Server_Logger", level=logging.INFO)

    @reactive.Calc
    def get_cleaned_gdp_data():
        try:
            fred_api_logger.info("Starting FRED API data fetching in server")
            current_file_dir = pathlib.Path(__file__).parent
            csv_file_path = current_file_dir / "data" / "csv_data" / "GDP quarterly data.csv"
            if not csv_file_path.exists():
                fred_api_logger.error(f"CSV file not found at {csv_file_path}.")
                return pd.DataFrame()
            df = pd.read_csv(
                filepath_or_buffer=csv_file_path,
                index_col='date',
                parse_dates=True,

            )

            df['value']= pd.to_numeric(df['value'],errors='coerce')
            df['value_growth_rate'] = pd.to_numeric(df['value_growth_rate'],errors='coerce')
            gdp_cleaner = Fred_Data_Cleaner(df=df)
            cleaned_data = (
                gdp_cleaner
                .handle_missing_values()
                .get_cleaned_data()
            )
            fred_api_logger.info("Successfully loaded data from CSV.")
            return cleaned_data
            # async with FRED_API() as fred_client:
            # gdp_params = {'observation_start':'1989-01-01','observation_end':'2024-01-01'}
            # real_gdp_df = await fred_client.get_series_obs('GDPC1',params=gdp_params)
            # if real_gdp_df is not None and not real_gdp_df.empty:
            # fred_api_logger.info("Successfully fetched Real GDP data.")
            # gdp_cleaner = Fred_Data_Cleaner(df=real_gdp_df)
            # cleaned_data = (
            # gdp_cleaner
            # .replace_columns()
            # .handle_missing_values()
            # .calculate_pct_change()
            # .get_cleaned_data()
            # )
            # fred_api_logger.info('Data cleaned successfully, returning cleaned DataFrame')
            # return cleaned_data
            # else:
            # fred_api_logger.warning('Fred_API returned no data or an emptu DataFrame')
            # return pd.DataFrame()
        except Exception as e:
            fred_api_logger.error(f"Error fetching or cleaning data:{e}")
            return pd.DataFrame()

    @output
    @render_widget
    def gdp_plot():
        df = get_cleaned_gdp_data()
        if not df.empty:
            print("DataFrame passed to graph_generator:")
            print(df.head())
            print("\nDataFrame columns and dtypes:")
            print(df.info())
            grapher = Graph_For_Data()
            fig = grapher.graph_generator(df)
            fred_api_logger.info(f'Returning figure')
            return fig
        return go.Figure().update_layout(title_text="No Data Available for Plot")


app = App(my_app_ui.app_ui, server)
if __name__ == "__main__":
    app.run()
