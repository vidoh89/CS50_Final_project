import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
import os
import pathlib
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from shinywidgets import render_widget
from data.fred_data import FRED_API
from app_ui.graph_data import Graph_For_Data
from utils.fred_data_cleaner import Fred_Data_Cleaner
from utils.csv_data_retriever import Get_Data
from logs.logs import Logs
from typing import Optional, Union
from htmltools import TagList, div, Tag


class GDP_DATA_SERVER(Logs):
    """
    Server to handle output logic for FRED_GDP_UI application
    """

    def __init__(self):
        super().__init__(name='Server module', level=logging.INFO)

    def ui_output_ui(self) -> Tag:
        """
        Creates an output container for UI(HTML) element
        :return: returns a tag object
        :rtype: Tag
        """

    def get_server(self):
        """
        Main server function to tie inputs to outputs.
        """

        def server(input: Inputs, output: Outputs, session: Session):
            """
            Server logic to generate output for input variables
            :param input:
            :param output:
            :param session:
            :return:
            """

            @render.ui
            def gdp_navbar_id() -> Union[ui.navset_tab, Tag]:
                self.info('Setting navbar component in server')
                return ui.navset_tab(
                    ui.nav_panel("GDP Data","Latest GDP insights"),
                    ui.nav_panel("About","About section for GDP")
                )

        return server
