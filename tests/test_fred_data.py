import pytest
import pandas as pd
import os
import logging
from unittest.mock import patch, Mock, AsyncMock, MagicMock

import pytest_aiohttp

from data.fred_data import FRED_API
import requests
import aiohttp
from aiohttp import ClientResponseError, helpers

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
@pytest.mark.asyncio
async def test_successful_request():
    """
    Mocks a successful request for data, made to the FRED_API
    """
    # Setup mock response
    mock_response = AsyncMock()
    # mock a successful request
    mock_response.status= 200
    # mock parameter values for response
    mock_response.json = AsyncMock(return_value={'observations': [{'date': "2020-01-01", 'value': '124.45'}]})
    # ensure exception is not raised
    mock_response.raise_for_status = Mock()


    # Setup session Mock
    mock_session_instance = MagicMock()

    # mock async session
    mock_session_instance.get.return_value.__aenter__.return_value = mock_response
    # isolate session using patch
    with patch("aiohttp.ClientSession",return_value=mock_session_instance):
        # Mock request for data
        async with FRED_API(api_key='TEST_KEY') as fred_client:
            data = await fred_client._request_data("series/observations",{"series_id":"TEST_SERIES"})

            assert data is not None
            assert data["observations"][0]['value'] == '124.45'
@pytest.mark.asyncio
async def test_failed_request(caplog):
    """
    Mocks a failed request made to the FRED_API
    """
    # mock response for request
    mock_response= MagicMock()
    # mock bad request value
    mock_response.status= 400
    # Trigger exception

    # mock json data for requested data
    mock_response.json= AsyncMock(return_value={'error':'Invalid Request'})
    # mock session instance
    mock_session_instance = MagicMock()
    mock_session_instance.get.return_value.__aenter__.return_value = mock_response
    # mock error behavior
    mock_response.raise_for_status.side_effect= aiohttp.ClientResponseError(
        request_info=MagicMock(),
        history=MagicMock(),
        status=400,
        message='Bad Request'
   )
    #isolate session using patch
    with patch("aiohttp.ClientSession",return_value=mock_session_instance):
        # mock request for data
        async with FRED_API(api_key="TEST_INVALID_REQUEST") as fred_client:
            # capture error logs
            with caplog.at_level(logging.ERROR):
                fred_client._logger.addHandler(caplog.handler)
                data = await fred_client._request_data("series/observations",{"series_id":"TEST"})

            assert data is None
            assert "Http error occurred" in caplog.text
@pytest.mark.asyncio
async def test_bad_session_input(caplog):
    """
    Test for bad input to client session object
    :param caplog: captures logging errors
    """
    # mock response
    mock_response = MagicMock()
    # mock bad status code
    mock_response.status= 404
    # mock error to be raised
    mock_response.raise_for_status.side_effect= aiohttp.ClientResponseError(
        request_info=MagicMock(),
        history=MagicMock(),
        status=404,
        message='Not Found'
    )
    # Set up the mock session
    mock_session= MagicMock()
    # mock session __aenter__ with response
    mock_session.get.return_value.__aenter__.return_value= mock_response

    # patch session
    with patch('data.fred_data.aiohttp.ClientSession',return_value=mock_session):
        async with FRED_API(api_key='TEST') as fred:
            # attach logger
            fred._logger.addHandler(caplog.handler)
            with caplog.at_level(logging.ERROR):
                response= await fred._request_data("invalid/endpoint",{})

        # Assertions
        assert response is None
        assert "Http error occurred" in caplog.text
        assert "404" in caplog.text
        assert "Not Found" in caplog.text

@pytest.mark.asyncio
async def general_failure(caplog):
    """
    Mock for general Exceptions
    :param caplog:
    """
    # Mock response variable
    mock_response= MagicMock()
    # Mock general error
    mock_response.json.side_effect= Exception('System Crash')
    # Mock session
    mock_session= MagicMock()
    # Set the Mock's return_value
    mock_session.get.return_value.__aenter__.return_value= mock_response
    # Patch the session
    with patch('data.fred_data.aiohttp.ClientSession',return_value=mock_session):
        async with FRED_API(api_key='TEST') as fred:
            fred._logger.addHandler(caplog.handler)
            # await response
            response = await fred._request_data("some/endpoint",{})
    assert response is None
    assert "Error occurred while fetching data" in caplog.text
    assert "System Crash" in caplog.text

@pytest.mark.asyncio
async def test_series_obs(caplog):
    """
    Test for successful parameter input and DataFrame processing.
    :param caplog: Captures log messages
    """
    # Mock payload data
    mock_api_data= {'observations':[
        {'date':"2020-01-01",'value':'10.5'},
        {'date':"2020-01-02",'value':'11.3'},
        {'date':"2020-01-03",'value':'.'} # test none numeric data
    ]}
    # Setup for mocks
    mock_response= MagicMock()
    mock_response.status= 200
    # mock to await data
    mock_response.json= AsyncMock(return_value=mock_api_data)
    # mock session
    mock_session= MagicMock()
    mock_session.get.return_value.__aenter__.return_value= mock_response

    # patch fred_data session
    with patch('data.fred_data.aiohttp.ClientSession',return_value=mock_session):
        # Initialize FRED_API
        async with FRED_API(api_key='TEST_KEY') as fred:
            df = await fred.get_series_obs("GDP")
    assert isinstance(df,pd.DataFrame)
