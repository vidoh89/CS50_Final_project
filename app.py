import pandas as pd
import plotly.express as px
import logging
import os
import plotly.graph_objects as go
import pathlib

import shiny
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive

import theme_style
from data.fred_data import FRED_API
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
        super().__init__(name='app module', level=logging.INFO)
        self.gdp_navbar = None
        # Set current file to base directory
        base_dir = pathlib.Path(__file__).resolve().parent
        try:
            self.css_path = base_dir / 'theme' / 'style.css'
        except Exception as e:
            self.error(f'Error handling css file: {e}')
            self.css_path = None

    def gdp_nav_container(self):
        try:
            base_path = pathlib.Path(__file__).parent.resolve()
            full_path = base_path / 'www' / 'theme' / 'style.css'

            # Object to hold logo
            gdp_logo = ui.tags.a(
                ui.tags.img(
                    ui.output_image("logo"),
                    src='logo_2.png',

               ),
                href='#',
                class_='navbar-brand'  # The `navbar-brand` class should be on the parent div

            )

            return ui.page_fluid(

                ui.tags.head(
                    ui.include_css(
                        full_path
                    )
                ),
                ui.page_navbar(

                    ui.nav_control(gdp_logo),

                    ui.nav_panel("GDP",
                                 ui.h4('Latest GDP insights'),
                                 output_widget("gdp_growth_plot")),
                    ui.nav_panel("About", "About section for gdp"),
                    fluid=True,
                    window_title='GDP Growth Rate',
                    lang='en',
                    theme=ui.Theme(preset="flatly"),
                    navbar_options=ui.navbar_options(position="fixed-top", collapsible=True),

                ),
                ui.output_ui('nav_bar', inline=True)

            )

        except Exception as e:
            self.error(f'Could not generate navbar element with preset theme:Error{e}')
            return ui.page_fluid(
                ui.p("Error building the application ui")
            )


my_app_ui = FRED_GDP_UI()
server_inst = GDP_DATA_SERVER()

# call server method
server = server_inst.get_server()
base_dir = pathlib.Path(__file__).parent.resolve()

app = App(
    my_app_ui.gdp_nav_container(),
    server,
    static_assets=base_dir / "www"
)
if __name__ == "__main__":
    app.run()
