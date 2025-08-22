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

class GDP_DATA_SERVER(Logs):
    """
    Server to handle output logic FRED_GDP_UI application
    """
    def __init__(self):
        super().__init__(name="GDP_DATA_SERVER",level=logging.INFO)
        # Instantiate FRED_API
        self.fred_client = FRED_API()
        def server(self,input,output,session):
            """
            Server logic, used to process data and generate output.
            :param input:
            :param output:
            :param session:
            :return:
            """