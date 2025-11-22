import pytest
import pandas as pd
import plotly.graph_objects as go
import logging
from app_ui.graph_data import Graph_For_Data

@pytest.fixture
def graph():
    """
    Returns an instance of the Graph_For_Data object
    """
    return Graph_For_Data()
@pytest.fixture
def valid_df():
    data = {
        "value":[100,140,150],
        "value_growth_rate":[1.0,5.0,4.7]
    }
    dates = pd.to_datetime(["2020-01-01","2020-04-01","2021-12-02"])
    df = pd.DataFrame(data,index=dates)
    return df

def test_graph_initialization(graph):
    """
    Test that Graph_For_Data object initialize as expected
    :param graph: Holds Graph_For_Data object
    :return: An instance of Graph_For_Data
    """
    assert isinstance(graph,Graph_For_Data)

