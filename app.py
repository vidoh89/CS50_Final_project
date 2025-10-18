import pandas as pd
import plotly.express as px
import logging
import os
import plotly.graph_objects as go
import pathlib
import shiny
import shinywidgets
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
import theme_style
from logs.logs import Logs
from typing import Optional, Union
from app_ui.navbar import Navbar
from htmltools import TagList, div
from shinywidgets import output_widget, render_widget
from utils.fred_data_cleaner import Fred_Data_Cleaner
from app_ui.graph_data import Graph_For_Data
from server.app_server import GDP_DATA_SERVER

# Load environment variables
load_dotenv()


class FRED_GDP_UI(Logs):
    """
    Encapsulates UI and server logic for fred_data module
    """

    LANG_CONST = tuple(["en", "es", "fr", "de", "ja", "ko", "zh-CN", "zh-TW"])

    def __init__(self):
        super().__init__(name="app module", level=logging.INFO)
        self.gdp_navbar = None
        # Set current file to base directory
        base_dir = pathlib.Path(__file__).resolve().parent
        try:
            self.css_path = base_dir / "theme" / "style.css"
        except Exception as e:
            self.error(f"Error handling css file: {e}")
            self.css_path = None
        self._max_date = None
        self._min_date = None

    def gdp_nav_container(self):
        try:
            base_path = pathlib.Path(__file__).parent.resolve()
            full_path = base_path / "www" / "theme" / "style.css"
            self._min_date = pd.to_datetime("1987-01-01")
            self._max_date = pd.to_datetime("2025-01-01")

            # Object to hold logo
            gdp_logo = ui.tags.a(
                ui.tags.img(src="logo_2.png", alt="Go GDP Homepage.Click Logo to be taken to homepage"),
                href="/",
                class_="Logo"
            )
            # Navigational links
            # GDP page content
            gdp_panel = ui.nav_panel(
                "GDP",
                ui.div(
                    # GDP card
                    ui.div(
                        ui.h4("Latest GDP Insights"),
                        ui.input_slider(
                            "date_range",
                            "Select Date Range",
                            min=self._min_date,
                            max=self._max_date,
                            value=(
                                pd.to_datetime("2020-01-01"),
                                pd.to_datetime("2024-01-01"),
                            ),
                            time_format="%Y-%m-%d",
                            animate=ui.AnimationOptions(
                                interval=400,
                                loop=False,
                                play_button="Time lapse data",
                                pause_button="Stop Time lapse",
                            ),
                        ),
                        class_="slider_card",
                    ),
                    # Graph card
                    ui.div(
                        #ui.output_ui("gdp_growth_plot"),
                        output_widget("gdp_growth_plot"),
                        class_="plot_card",
                    ),
                    class_="main-container",
                ),
            )
            # About page content
            about_panel = ui.nav_panel(
                "About",
                ui.div(
                    ui.h2("About This Application"),
                    ui.p(
                        "This application visualizes US Real GDP and Quarterly Growth Rate data sourced from FRED."
                    ),
                    ui.a(
                        "Data Source: FRED API",
                        href="https://fred.stlouisfed.org/",
                        target="_blank",
                    ),
                    class_="main-container",
                ),
            )
            ####################

            return ui.page_bootstrap(
                ui.tags.head(
                    ui.tags.title("GDP Growth Rate"),
                    ui.include_css(full_path)
                             ),
                ui.div(
                    ui.page_navbar(
                        gdp_panel, about_panel, title=gdp_logo, id="main_nav", bg=None
                    ),
                    class_="page-container"
                )
            )

        except Exception as e:
            self.error(f"Could not generate UI: Error{e}")
            return ui.page_fluid(ui.p("Error building the application ui"))


my_app_ui = FRED_GDP_UI()
server_inst = GDP_DATA_SERVER()

# call server method
server = server_inst.get_server()
base_dir = pathlib.Path(__file__).parent.resolve()

app = App(my_app_ui.gdp_nav_container(), server, static_assets=base_dir / "www")
if __name__ == "__main__":
    app.run()
