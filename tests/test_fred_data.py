import pytest
import pandas as pd
import os
import logging
from unittest.mock import patch,Mock
from data.fred_data import FRED_API
import requests

def test_fred_initialization_key():
    """
    Test initialization of FRED_API when an API key is provided
    """
    fred_client = FRED_API(api_key="TEST_KEY")
    assert fred_client.API_KEY == "TEST_KEY"
def test_fred_initialization_env():
    """
    Test initialization of FRED_API when an API key is not provided.
    Loads API key from environment variables
    """
    with patch.dict(os.environ,{"FRED_KEY":"ENV_TEST_KEY"},clear=True):
        fred_client = FRED_API()
        assert fred_client.API_KEY == "ENV_TEST_KEY"
def test_api_key_value_error(caplog):
    """
    Test that a ValueError is raised if no api key is provided
    and no can could be loaded from environment variables
    """
    with patch.dict(os.environ,dict(),clear=True):
        with pytest.raises(ValueError,match="Must provide api_key or set as an environment variable"):
            FRED_API()
def test_successful_request():
    fred_client = FRED_API(api_key="TEST_KEY")
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value={'observations':[{"date":"2020-01-01","value":"123.45"}]}

    with patch("requests.get",return_value=mock_response) as mock_get:
        data = fred_client._request_data("series/observations",{"series_id":"TEST_SERIES"})

    assert data is not None
    assert "observations" in data
    assert len(data["observations"]) ==1
    assert data["observations"][0]["value"]== "123.45"

    mock_get.assert_called_once()

    expected_url = "https://api.stlouisfed.org/fred/series/observations"
    expected_params = {
        "series_id": "TEST_SERIES",
        "api_key": "TEST_KEY",
        "file_type":"json"
    }
    mock_get.assert_called_once_with(expected_url,params=expected_params)

def test_request_data_http_error(caplog):

    fred_client = FRED_API(api_key="TEST_KEY")

    fred_client._logger.addHandler(caplog.handler)

    with caplog.at_level(level=logging.INFO):
        with patch("requests.get",side_effect=requests.exceptions.HTTPError("404 Not Found")):
            data = fred_client._request_data("series/observations",{"series_id":"TEST_SERIES"})
    fred_client.close()
    assert data is None
    assert "Http error occurred: 404 Not Found" in caplog.text

def test_get_series_obs_data_trans():
    """
    Test that get_series_obs returns a pd.DataFrame with correct formatting
    """
    fred_client = FRED_API(api_key="TEST_KEY")
    mock_data ={
        "observations":[
            {"date":"2020-01-01","value":"100.5"},
            {"date":"2020-04-01","value":"101.2"},
            {"date":"2020-07-01","value":"."}
        ]
    }
    with patch.object(fred_client,'_request_data',return_value= mock_data) as mock_request:
        df = fred_client.get_series_obs("TEST_SERIES")

    assert isinstance(df,pd.DataFrame)
    assert len(df) ==2

    assert pd.api.types.is_datetime64_dtype(df.index)

    assert pd.api.types.is_numeric_dtype(df['value'])

    assert df.loc["2020-01-01","value"] == 100.5

    mock_request.assert_called_once_with(
        "series/observations",
        {'series_id':'TEST_SERIES'}
    )

