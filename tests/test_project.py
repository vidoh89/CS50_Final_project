import pytest
from project import get_data,clean_data,data_plot
from data.fred_data import FRED_API
from logs import logs
from data import fred_data
import pandas as pd
import aiohttp
import asyncio
from unittest.mock import Mock,MagicMock,AsyncMock
from unittest.mock import patch


def test_get_data():
    """
    Test to ensure correct response is returned when get_data is called
    :return:
    """
    # Create mocked data
    mocked_data = {
        'date':['2026-01-01','2026-04-01'],
        'value':['23548.210','24000.150']
    }
    expected_df= pd.DataFrame(mocked_data)
    # Patch FRED_API
    with patch('project.FRED_API') as MockFredAPI:
        # Mock to handle async context manager
        mock_api_instance= AsyncMock()
        # Return mock data from get_series_obs
        mock_api_instance.get_series_obs.return_value= expected_df
        # Configure the context manager to mock instance
        MockFredAPI.return_value.__aenter__.return_value= mock_api_instance
        # Call results using get_data()
        result= get_data('GDPC1')
    assert isinstance(result,pd.DataFrame)
    assert not result.empty
    assert 'value' in result.keys()
    assert '2026-01-01' in result.values
    assert '23548.210' in result.values



