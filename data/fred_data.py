import importlib
import os
import sys
import logging
import pandas as pd
import pandas_datareader as pdr
import requests
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

    def _request_data(
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
            response = requests.get(full_url, params=params)
            response.raise_for_status()  # raise exception if request fails: bad status code
        except requests.exceptions.HTTPError as e:
            self.error(f"Http error occurred: {e}")
            return None
        except requests.exceptions.RequestException() as e:
            self.error(f"Following error occurred while making request: {e}")
            return None
        except Exception as e:
            self.error(f"Error occurred while fetching data.Error:{e}")
            return None
        else:
            self.info("Successful request made")
            return response.json()
        finally:
            self.info("Request process concluded")
            return None
