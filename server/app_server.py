import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
import os
import pathlib
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from shinywidgets import render_widget, output_widget
from data.fred_data import FRED_API
from app_ui.graph_data import Graph_For_Data
from utils.fred_data_cleaner import Fred_Data_Cleaner
from utils.csv_data_retriever import Get_Data
from logs.logs import Logs
from typing import Optional, Union
from htmltools import TagList, div, Tag
from shiny.types import ImgData


class GDP_DATA_SERVER(Logs):
    """
    Server to handle output logic for FRED_GDP_UI application
    """

    def __init__(self):
        super().__init__(name='Server module', level=logging.INFO)

        # Initialize instance variables
        self.get_graph = Get_Data()
        self.graph_creator = Graph_For_Data()
        self.info("Loading GDP data.")
        self.gdp_df = self.get_graph.get_gdp_csv()
        if self.gdp_df is None or self.gdp_df.empty:
            self.warning("Failed to load GDP data or Dataframe is empty.")

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

            @render_widget
            def gdp_growth_plot():
                """
                Renders the Growth plot for the GDP
                :return:
                """
                self.info("Rendering plot.")
                if self.gdp_df is not None and not self.gdp_df.empty:
                    # Create plotly figure
                    fig = self.graph_creator.graph_generator(df=self.gdp_df)
                    return fig
                else:
                    self.warning("Could not plot GDP data")

                    return go.Figure()



        return server
