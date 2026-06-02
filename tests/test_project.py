
import pytest
from project import get_data, clean_data, data_plot
from data.fred_data import FRED_API
from logs import logs
from data import fred_data
import pandas as pd
import aiohttp
import asyncio
from unittest.mock import Mock, MagicMock, AsyncMock
from unittest.mock import patch


def test_get_data():
    """
    Test to ensure correct response is returned when get_data is called
    :return:
    """
    # Create mocked data
    mocked_data = {
        'date': ['2026-01-01', '2026-04-01'],
        'value': ['23548.210', '24000.150']
    }
    expected_df = pd.DataFrame(mocked_data)
    # Patch FRED_API
    with patch('project.FRED_API') as MockFredAPI:
        # Mock to handle async context manager
        mock_api_instance = AsyncMock()
        # Return mock data from get_series_obs
        mock_api_instance.get_series_obs.return_value = expected_df
        # Configure the context manager to mock instance
        MockFredAPI.return_value.__aenter__.return_value = mock_api_instance
        # Call results using get_data()
        result = get_data('GDPC1')
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'value' in result.keys()
    assert '2026-01-01' in result.values
    assert '23548.210' in result.values


def test_get_data_network_error():
    """
    Check for graceful exception handling and returns None for bad request
    :return: None
    """
    with patch('project.FRED_API') as MockFredAPI:
        mock_api_instance = AsyncMock()
        # Mock Exception as side_effect
        mock_api_instance.get_series_obs.side_effect = Exception("Connection Timeout")
        # Mock return value for MockFredAPI
        MockFredAPI.return_value.__aenter__.return_value = mock_api_instance

        result = get_data('GDPC1')

        assert result is None


def test_get_data_bad_input(capsys):
    """
    Checks for incorrect asset input and returns None if assets does not exist
    :raise Exception: For bad input
    :return: None
    """
    with patch('project.FRED_API') as Mock_Fred_API:
        mock_api_instance = AsyncMock()
        # Simulate a bad request to the FRED api
        mock_api_instance.get_series_obs.side_effect = Exception('Asset does not exist')
        # Set mocked data to Mock_Fred_API return value
        Mock_Fred_API.return_value.__aenter__.return_value = mock_api_instance
        # Holds result for bad input
        result = get_data('GGCC2')
        # Captures and returns the mocked error msg
        captured_err= capsys.readouterr()
        assert result is None
        assert "Asset does not exist" in captured_err.out
def test_clean_data():
    """
    Test to ensure clean_data handles a single-row DataFrame gracefully
    by returning an empty data frame due to look-back constraints.
    retrieved from the FRED_API
    """
    # Mock data
    mocked_data= {
        "realtime_start":["2013-08-14"],
        "realtime_end":["2013-08-20"],
        "value":["2182.681"]
    }
    # datetime index to mimic FRED'S data format
    mocked_df= pd.DataFrame(data=mocked_data,index=pd.to_datetime(["2013-01-01"]))

    # Call clean_data passing mocked_df
    result_df = clean_data(raw_data=mocked_df)

    # Assertions
    assert isinstance(result_df,pd.DataFrame)
    assert result_df.empty
    assert len(result_df)==0
def test_clean_data_incorrect_key():
    """
    Test to ensure an empty data frame is returned if
    key values are incorrect.
    :return:
    """
    bad_keys= {
        "incorrect_key_1":[1,2],
        "incorrect_key_2":[3,4]
    }
    # Pass bad_keys to the clean_data function
    result= clean_data(raw_data=pd.DataFrame(data=bad_keys))
    # Assertions
    assert isinstance(result,pd.DataFrame)
    assert len(result)==2
def test_clean_data_NaN():
    """
    Test the proper handling of NaN values
    :return:
    """
    import numpy as np
    # Create mock dataset
    mock_data={
        "realtime_start":["2013-08-14","2013-08-14","2013-08-14"],
        "realtime_end":["2013-08-20","2013-08-20","2013-08-20"],
        "value":["100.0",np.nan,"110.0"]
    }
    # Create data frame populated with mocked data
    mocked_df= pd.DataFrame(data=mock_data,index=pd.to_datetime(["2025-01-01","2025-04-01","2025-07-01"]))
    # Pass data to clean_data() for manipulation
    result= clean_data(raw_data=mocked_df)

    assert isinstance(result,pd.DataFrame)
    assert len(result)==2
    assert "value" in result.columns
    assert "value_growth_rate" in result.columns
    assert result.loc["2025-04-01","value"]== pytest.approx(100.0)
    assert result.loc["2025-04-01","value_growth_rate"]== pytest.approx(0.0)
    assert result.loc["2025-07-01","value_growth_rate"]== pytest.approx(10.0)
    assert result.loc["2025-07-01","value"]== pytest.approx(110.0)
def test_data_plot():
    """
    Test to verify correct plotting of data.
    :return:
    """
    import plotly.graph_objs as go
    mock_data= {
        "value":[24152.656,24300.100],
        "value_growth_rate":[0.402843,0.610123]

    }
    mock_df= pd.DataFrame(data=mock_data,index=pd.to_datetime(["2025-01-01","2025-02-01"]))
    fig=data_plot(mock_df)

    assert fig is not None
    assert isinstance(fig,go.Figure)
def test_data_plot_bad_data(capsys):
    """
    Test that, if passed an empty or <None> value data set,
    data_plot() returns None
    :return:
    """

    # Create df with a None value
    none_value_df= data_plot(df=None)
    capture_msg_none_value= capsys.readouterr()
    # Assertions for None value
    assert none_value_df is None
    assert "either missing or corrupted" in capture_msg_none_value.out

    # Create an empty data frame
    empty_df= pd.DataFrame()
    no_result= data_plot(df=empty_df)
    captured_msg= capsys.readouterr()
    # Assertions for empty df
    assert no_result is None
    assert "either missing or corrupted" in captured_msg.out





