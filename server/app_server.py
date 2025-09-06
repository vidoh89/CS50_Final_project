import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
import os
import pathlib
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from data.fred_data import FRED_API
from app_ui.graph_data import Graph_For_Data
from utils.fred_data_cleaner import Fred_Data_Cleaner
from logs.logs import Logs
from typing import Optional, Union
from htmltools import TagList, div
from app import FRED_GDP_UI



class GDP_DATA_SERVER(Logs):
    """
    Server to handle output logic for FRED_GDP_UI application
    """

    def __init__(self, fred_client:FRED_API= FRED_API):
        """
        Handles server logic for FRED_GDP_UI object
        :param fred_client: Holds data to be retrieved by server
        :type fred_client: FRED_API
        :raise TypeError: If incorrect value type is passed for fred_client
        """
        super().__init__(name="GDP_DATA_SERVER", level=logging.INFO)
        # Initiate data access object <fred_client>
        try:
            if fred_client and isinstance(fred_client,FRED_API):
                self.info('Initializing fred_client')
        except TypeError as e:
            self.error('Could not load object for fred_client')
            raise TypeError(f'fred_client should be an object of FRED_GDP_UI. Error:{e}')
        else:
            self.fred_client = fred_client
            self.info('Successfully loaded fred_client object')
        finally:
            self.info('Client initialization process complete.')

        def get_server():
            """
             Main server function to tie inputs to outputs.
            """
            def server(input:Inputs,output:Outputs,session):
                """
                Server logic to generate output for input variables
                :param input:
                :param output:
                :param session:
                :return:
                """
                @reactive.Calc
                def get_cleaned_data():
                    # Access ui inputs
                    try:
                        self.info("Data fetching process started for Server")
                        df = self.fred_client.get_series_obs({'observation_start':'1989-01-01',"observation_end":'2025-09-01'})
                    except (Exception,BrokenPipeError) as e:
                        self.error("Could not fetch data for server")
                        raise BrokenPipeError(f"Error:{e}")


