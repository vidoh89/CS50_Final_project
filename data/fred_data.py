import aiohttp
import asyncio
import os
import sys
import logging
import pandas as pd
import pandas_datareader as pdr
import re
from dotenv import load_dotenv
from datetime import datetime
from logs.logs import Logs
from typing import Union, Optional, Dict, Any


class FRED_API(Logs):
    """
    St. Louis Federal Reserve (FRED) API client.
    This client provides methods to interact with the FRED API, it handles:
    ->API key management
    ->request to endpoints
    ->error handling
    FRED_API inherits from the Logs class for progress monitoring
    """

    BASE_LINK: str = "https://api.stlouisfed.org/fred/"

    def __init__(self, api_key: Union[str, None] = None):
        """
        Initializes FRED API client.
        api_key required,if not provided directly an attempt
        to load variables from environment variable named 'FRED_KEY'.

        :param api_key: Access key for FRED API
        :type api_key: Union[str,None]
        :raise ValueError: If api_key is not provided
                           and environment variable are not accessible
        """
        # Create logger instance
        super().__init__(name="fred_api", level=logging.DEBUG)
        self.API_KEY = api_key or os.getenv("FRED_KEY")
        # Load API key
        if not self.API_KEY:
            self.error("Could not load API_KEY:Loading parameters from os variable.")
            raise ValueError("Must provide api_key or set as an environment variable.")
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """
        Enter the async context manager
        :return:
        """
        self.info("Entering async context manager")
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the async context manager and close session.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.info('Exiting FRED_API async context manager')
        if self._session and not self._session.closed:
            await self._session.close()
        return False
    @property
    def session(self) -> aiohttp.ClientSession:
        """
        Manages a single aiohttp session for the class instance
        :return: Returns the session or a single aiohttp.ClientSession
        :rtype: Optional[aiohttp.ClientSession]
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

        return self._session

    async def _request_data(
        self, endpoint: str, params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Private method: Handles requests and error checking for API
        :param endpoint: Holds the search  value for wanted endpoint
        :type endpoint: str
        :param params:Dict for selecting category
        :type params: Dict

        """
        full_url = f"{self.BASE_LINK}{endpoint}"
        params.update(
            {"api_key": self.API_KEY, "file_type": "json"}
        )  # set key/value- api_key:API_KEY,"file_type":"json"

        try:
            self.info(f"Request sent to:{full_url},parameters used: {params}")
            session = self.session
            async with self.session.get(full_url, params=params) as response:
                response.raise_for_status()
                await_data = await response.json()
                self.info("Successful request made.")
                return await_data

        except aiohttp.ClientResponseError as http_e:
            self.error(f"Http error occurred: {http_e}")

        except aiohttp.ClientError as request_e:
            self.error(f"Following error occurred while making request: {request_e}")

        except Exception as exception_e:
            self.error(f"Error occurred while fetching data.Error:{exception_e}")

        self.info("Request process complete.")

        return None

    async def get_series_obs(
        self, series_id: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[pd.DataFrame]:
        """
        Fetches series observation data.
        :param series_id: ID to retrieve series data
        :type series_id:str
        :param params: Dict holds key/value for retrieving data
        :return: A pandas Dataframe with selected series data
        :rtype:Optional[pd.DataFrame]
        """
        endpoint = "series/observations"
        # Initialize empty dict if no params are provided
        if params is None:
            params = dict()
        params["series_id"] = series_id

        data = await self._request_data(
            endpoint,
            params
        )  # Holds the endpoint/params for data retrieval
        if data and "observations" in data:
            df = pd.DataFrame(
                data["observations"]
            )  # return a list of dict in observations key
            # Clean and convert data
            if not df.empty:

                # Convert 'date' column to datetime object
                df["date"] = pd.to_datetime(df["date"])

                # Convert 'value' column to numeric values
                df["value"] = pd.to_numeric(df["value"], errors="coerce")

                # Set the date column as the index for time series
                df.set_index("date", inplace=True)

                # Drop rows where 'values' are NaN(not a number)
                df.dropna(subset=["value"], inplace=True)

            self.info(
                f"Successfully processed observation data for series_id:{series_id}"
            )
            return df
        else:
            self.warning(f"No observation found for series:{series_id}")
            return None


async def main():
    """
    Main function to run the FRED client

    """
    load_dotenv()
    async with FRED_API() as fred_client:
        try:
            gdp_params = {'observation_start':'2020-01-01','observation_end':'2025-12-31'}
            real_gdp_df = await fred_client.get_series_obs('GDPC1',params=gdp_params)
            if real_gdp_df is not None:
                print("\nSuccessfully fetched Real GDP data from 2020")
                print(real_gdp_df)
        except ValueError as value_e:
            print(f'Failed to initialize FRED_API:{value_e}')

if __name__ == "__main__":
    asyncio.run(main())