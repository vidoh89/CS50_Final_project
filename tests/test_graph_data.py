import plotly.graph_objects
import plotly
import pytest
import pandas as pd
import plotly.graph_objects as go
import logging
from app_ui.graph_data import Graph_For_Data

@pytest.fixture
def grapher():
    """
    Returns an instance of the Graph_For_Data object
    """
    return Graph_For_Data()
@pytest.fixture
def valid_df():
    """
    DataFrame mocking FRED data
    :return: pd.DataFrame
    """
    data = {
        "value":[100,140,150],
        "value_growth_rate":[1.0,5.0,4.7]
    }
    dates = pd.to_datetime(["2020-01-01","2020-04-01","2021-12-02"])
    df = pd.DataFrame(data,index=dates)
    return df

def test_graph_initialization(grapher):
    """
    Test that Graph_For_Data object initialize as expected
    :param graph: Holds Graph_For_Data object
    :return: An instance of Graph_For_Data
    """
    assert isinstance(grapher,Graph_For_Data)
def test_graph_generator_traces(grapher, valid_df):
    """
    Test Figure
    :param grapher: Instance of the Graph_For_Data
    :param valid_df: Holds mocked data
    :return:
    """
    test_fig = grapher.graph_generator(valid_df,fig_title="TEST_DATA")

    assert isinstance(test_fig,go.Figure)

    # Assertion for two traces being added to graph
    assert len(test_fig.data) ==2
    trace_1 = test_fig.data[0]
    assert trace_1.name == 'Real GDP(Billions)'
    assert trace_1.mode == 'lines+markers'
    assert list(trace_1.x) == list(valid_df.index)
    assert trace_1.line.color =='cyan'
    assert trace_1.line.width == 2
    assert trace_1.textfont.size== 4


    trace_2 = test_fig.data[1]
    assert list(trace_2.x) == list(valid_df.index)
    assert trace_2.name == 'Growth Rate(%)'
    assert trace_2.mode == 'lines+markers'
    assert trace_2.yaxis == 'y2'

def test_graph_layout(grapher,valid_df):
    """
    Test that plotly updates the graph object with correct parameter values
    :param grapher: Figure object
    :param valid_df: Test data for testing environment
    :return:
    """
    test_fig = grapher.graph_generator(valid_df,fig_title="TEST_DATA")
    test_layout = test_fig.layout
    assert test_layout.font.size == 9.5
    assert test_layout.hovermode == 'x unified'
    assert test_layout.title.text == 'US Real GDP and Quarterly Growth Rate'
    assert test_layout.title.x== 0.5
    assert test_layout.title.y == 0.75
    assert test_layout.legend.orientation == 'h'
    assert test_layout.legend.yanchor == 'bottom'
    assert test_layout.legend.xanchor == 'center'
    assert test_layout.legend.y == 1.00
    assert test_layout.legend.x == 0.5
    assert test_layout.legend.bgcolor == 'rgba(0,0,0,0)'
def test_graph_layout_xaxis(grapher,valid_df):
    test_graph = grapher.graph_generator(valid_df,fig_title='TEST_DATA_xaxis')
    test_layout = test_graph.layout.xaxis
    assert test_layout.title.text == 'Date (Quarterly)'
    assert test_layout.type =='date'
    assert test_layout.tickformat=='%Y Q%q'
    assert test_layout.tickfont.size ==6











