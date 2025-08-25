import logging
import pandas as pd
import io
import matplotlib.pyplot as plt
from utils.fred_data_cleaner import Fred_Data_Cleaner
from data.fred_data import FRED_API
from logs.logs import Logs
class Graph_data(Logs):
    """
    Graph data provided by FRED_DATA_Cleaner
    """
    def __init__(self):
        super().__init__("Graphing module",level=logging.INFO)
        self.info("Starting data pipeline. ")
        gdp_df = self._fetch_cleaned_data()

    def _fetch_cleaned_data(self):
        """
        Private method to handle data fetching and cleaning
        """
        try:
            self.info("Fetching raw data from FRED_API")
            api = FRED_API()
            fred_raw_data = api.get_series_obs('UNRATE')
            if fred_raw_data is None or fred_raw_data.empty:
                return None
        except  Exception as e:
            self.error(f"Failed to fetch data from FRED_API:Error{e}")
        else:
            clean_df = Fred_Data_Cleaner(df=fred_raw_data)
            return clean_df



