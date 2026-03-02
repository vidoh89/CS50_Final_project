import pytest
import pandas as pd
import os
import logging
from unittest.mock import patch, Mock, AsyncMock, MagicMock
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
    :return:
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
