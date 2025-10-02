import asyncio
import datetime

import pandas as pd
import numpy as np
import logging
from typing import Union, Optional
from data.fred_data import FRED_API
from logs.logs import Logs
from dotenv import load_dotenv
from pathlib import Path


class Fred_Data_Cleaner(Logs):
    """
    Cleans and manipulates data provided via FRED_API module.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Module cleans and manipulates (pd.DataFrame) provided by FRED_API.

        :param df: Dataframe containing FRED data(e.g.,GDP)
        :type df: pd.DataFrame

        """
        self.df: pd.DataFrame = df.copy()

        # Initialize logs
        super().__init__(name='Fred_Data_Cleaner', level=logging.INFO)

    def handle_missing_values(self):
        """
        Fills missing (NaN) values using method:forward-fill
        :return: Returns df object for method chaining or further manipulation
        :rtype: Fred_Data_Cleaner
        """
        if self.df.isnull().sum().sum() > 0:  # Check for NaN values
            try:

                self.df.ffill(inplace=True)
                self.info('Successfully filled missing values.')
                return self
            except Exception as e:
                self.error(f"Error during value manipulation:{e}")
                return self
        else:
            self.info('No missing values to fill.Skipping forward-fill process.')
            return self

    def replace_columns(self):

        """
        Replaces specified column values to....specified_column_value
        """
        self.info("Removing specified columns")
        to_be_removed_col = ['realtime_start', 'realtime_end']
        found_col = [col for col in to_be_removed_col if col in self.df.columns]
        if found_col:
            try:
                self.df.drop(columns=found_col, inplace=True)

            except Exception as e:
                self.error(f'Could not replace specified values.Error:{e}')

        else:

            self.info("Specified columns where not found. Skipping removal")
        return self

    def str_to_numb(self, column_name: str = 'value'):
        """
        Converts specified column_name which should be type(str), to integer
        :param column_name: Original name of column to be converted
        :type column_name:str
        :return: self
        """
        if column_name in self.df.columns:
            self.df[column_name] = pd.to_numeric(self.df[column_name], errors='coerce')
            self.info('Column conversion successful')
            return self
        else:
            self.warning(f"Column '{column_name}' not found for numeric conversion.")
            return self

    def calculate_pct_change(self, column_name: str = 'value', new_column_name: str = None):
        """
        Calculates the rate of change quarter by quarter, for specified date
        :param column_name: Name of column containing values
        :type column_name:str
        :param new_column_name: Holds the value for chosen new column
        :type new_column_name:str
        :return: Returns Fred_Data_Cleaner object instance for method chaining
        :rtype: Fred_Data_Cleaner
        """
        if column_name not in self.df.columns:
            self.error(f'Column<{column_name}> not found in DataFrame. Could not calculate growth rate.')
            return self
        # variable for column name
        final_column_value = new_column_name if new_column_name else f'{column_name}_growth_rate'

        # Adjust df['value'] column to reflect df['Growth Rate']
        try:
            self.df[final_column_value] = self.df[column_name].pct_change() * 100
            # drop NaN row after % change
            self.df.dropna(subset=[final_column_value],inplace=True)
            self.info(f'Successfully calculated growth rate for column: {column_name}')
            return self
        except Exception as e:
            self.error(f'Error during growth rate calculation: {e}')
            return self

    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Returns a cleaned copy for GDP data
        :return: Returns Final DataFrame object with cleaning and manipulation applied
        :rtype:pd.DataFrame
        """
        self.info('Returning cleaned DataFrame')

        return self.df

    def export_file(self, file_name: str = None, output_dir: str = 'data/csv_data'):
        """
        Exports cleaned data file to following file extensions:[]
        If file_name is not provided,name defaults to a default name with timestamp.

        :param file_name: Name for csv file: defaults to a default name with timestammp
        :type file_name:str
        :param output_dir: Path to csv directory
        :type output_dir:str
        :return:
        """
        try:
            # Create export path for file
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # set file_name default
            if file_name is None:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
                final_file_name = f"GDP_data:{timestamp}.csv"
            else:
                if not file_name.endswith('.csv'):
                    file_name += '.csv'
                final_file_name = file_name
        except Exception as e:
            self.error('Could not complete csv export process')
            raise Exception(f"Error{e}")
        else:
            full_path = output_dir / final_file_name
            self.df.to_csv(full_path, index=True)
            self.info(f'Successfully created and exported csv to: {full_path}')
        finally:
            self.info('Export process complete')



