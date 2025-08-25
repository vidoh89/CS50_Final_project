import pandas as pd
import numpy as np
import logging
from typing import Union,Optional
from data.fred_data import FRED_API
from logs.logs import Logs
from dotenv import load_dotenv

class Fred_Data_Cleaner(Logs):
    """
    Cleans and manipulates data provided via FRED_API module.
    """
    def __init__(self,df:Union[pd.DataFrame,pd.Series]):
        """
        Module cleans and manipulates (pd.DataFrame) provided by FRED_API.

        :param df: Dataframe containing FRED data(e.g.,GDP)
        :type df: Union[pd.DataFrame,pd.Series]

        """
        self.df:Union[pd.DataFrame,pd.Series] = df.copy()

        #Initialize logs
        super().__init__(name='Fred_Data_Cleaner',level= logging.INFO)

    def handle_missing_values(self):
        """
        Fills missing (NaN) values using method:forward-fill
        :return: Returns df object for method chaining or further manipulation
        :rtype: Fred_Data_Cleaner
        """
        if self.df.isnull().sum().sum() >0: #Check for NaN values
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

    def calculate_pct_change(self,column_name:str='value',new_column_name:str=None):
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
        if new_column_name is None:
            self.new_column_name = f"{column_name}_growth_rate"
        # Adjust df['value'] column to reflect df['Growth Rate']
        try:
            self.df.loc[:,'gdp_growth_rate'] = self.df[column_name].pct_change() * 100
            self.info(f'Successfully calculated growth rate for column: {column_name}')
            return self
        except Exception as e:
            self.error(f'Error during growth rate calculation: {e}')
            return self


    def get_cleaned_data(self)->pd.DataFrame:
        """
        Returns a cleaned copy for GDP data
        :return: Returns Final DataFrame object with cleaning and manipulation applied
        :rtype:pd.DataFrame
        """
        self.info('Returning cleaned DataFrame')
        return self.df



if __name__=="__main__":
    load_dotenv()

    try:
        fred_client = FRED_API()
        gdp_params = {'observation_start':'2020-01-01','observation_end':'2025-12-31'}
        real_gdp_df = fred_client.get_series_obs('GDPC1',params=gdp_params)
        if real_gdp_df is not None:
            print("\nSuccessfully fetched Real GDP data from 2020: ")
            print(real_gdp_df)
    except ValueError as e:
        print(f"Failed to initialize FRED_API:{e}")