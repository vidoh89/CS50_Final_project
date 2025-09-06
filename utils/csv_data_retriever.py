import logging
import pathlib

import pandas as pd
import os
from pathlib import Path
from logs.logs import Logs
from typing import Optional, Union
from utils.fred_data_cleaner import Fred_Data_Cleaner


class Get_Data(Logs):
    """
    Retrieves preprocessed csv data
    """

    def __init__(self, csv_file: str = 'GDP quarterly data.csv'):
        """
        Initialize private variable to csv_file
        :param csv_file: Holds the data for the GDP
        :type csv_file: str
        :raise TypeError: If csv_file is not type(str)
        :raise FileNotFoundError: If csv_file cannot be found

        """
        super().__init__(name='csv_data_retriever', level=logging.INFO)
        if not isinstance(csv_file, str):
            raise TypeError('Incorrect type for csv_file,must be:type(str)')

        # Instantiate instance variables
        df = None
        self._csv_file_name = csv_file
        self.info('CSV type check completed successfully')
        self._df = df

    def get_gdp_csv(self) -> Optional[pd.DataFrame]:
        """
        Attempts to load csv data from constructed path.
        Converts csv data into pd.Dataframe.
        :return: Converted pd.DataFrame
        :rtype: pd.DataFrame
        :raise FileExistError: If file cannot be located
        :raise TypeError: If invalid type is used for gdp_csv
        :raise ValueError: If gdp_csv is missing correct extension type: <.csv>
        :raise Exception: If other unforeseen errors occur during csv retrival
        """
        try:
            # Construct path to .csv
            current_path = Path(__file__).resolve().parent.parent
            full_path = f'{current_path}/data/csv_data/GDP quarterly data.csv'

        except Exception as e:
            self.error(f'Could not construct file path. Error:{e}')
            return None
        try:
            df = pd.read_csv(filepath_or_buffer=full_path)
            self.info('csv to pd.Dataframe successful, returning dataFrame.')
            clean_data = Fred_Data_Cleaner(df=df).get_cleaned_data()
            clean_data.set_index('date',inplace=True,verify_integrity=True)
            self._df = clean_data
            return self._df
        except FileNotFoundError:
            self.error('File not found at path: %s', full_path)
            raise FileNotFoundError(f"CSV file '{self._csv_file_name}'not found")
        except Exception as e:
            self.error('An unexpected error occurred while loading the CSV.')
            raise Exception(f'Failed to load CSV file:{e}')





