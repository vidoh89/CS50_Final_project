import pandas as pd
import plotly.express as px
import logging
import os
import plotly.graph_objects as go
import pathlib

import shiny
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

    def gdp_nav_container(self):
        try:

            return ui.page_fluid(ui.page_navbar(
                ui.nav_panel("GDP","data for GDP"),
                ui.nav_panel("About"),
                title='GO GDP',
                fluid=True,
                window_title='GDP Growth Rate',
                lang='en',
                theme= ui.Theme(preset="flatly"),
                navbar_options= ui.navbar_options(position="fixed-top", collapsible=True)


            ),

                ui.output_ui(id='gdp_navbar_id')

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

app = App(my_app_ui.gdp_nav_container(), server)
if __name__ == "__main__":
    app.run()
