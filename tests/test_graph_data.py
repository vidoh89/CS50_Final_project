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
def test_graph_layout_yaxis(grapher,valid_df):
    test_graph = grapher.graph_generator(df=valid_df,fig_title='TEST_DATA_yaxis')
    test_layout_y = test_graph.layout.yaxis
    assert test_layout_y.title.text == "Real GDP($B)"
    assert test_layout_y.showgrid == True
    assert test_layout_y.zerolinewidth == 2
    assert test_layout_y.zerolinecolor == 'LightGrey'
    assert test_layout_y.type =='linear'
    assert test_layout_y.titlefont.size==10
    assert test_layout_y.tickfont.size==10
def test_graph_final_info_msg(grapher,valid_df,caplog):
    caplog.set_level(logging.INFO)
    target_msg = logging.getLogger('Graphing module')
    target_msg.addHandler(caplog.handler)
    grapher.graph_generator(df=valid_df,fig_title='TEST_LOGS')
    assert "Manual Plotly figure successfully generated" in caplog.text
def test_empty_df(grapher,caplog):
    """
    Verify correctly handling of empty dataframe
    :param grapher:
    :param caplog:
    :return:
    """
    caplog.set_level(logging.WARNING)
    target_warning_msg = logging.getLogger('Graphing module')
    target_warning_msg.addHandler(caplog.handler)
    empty_data = pd.DataFrame(data=None)
    test_graph = grapher.graph_generator(df=empty_data,fig_title='TEST_EMPTY_DF')

    assert isinstance(test_graph,go.Figure)
    assert len(test_graph.data) ==0
    assert "DataFrame has no content,returning empty Figure." in caplog.text
def test_incorrect_index(grapher,caplog):
    """
    Ensures that a none DatetimeIndex type raises an error when index values are not of type(pd.DatetimeIndex)
    :param grapher:
    :param caplog:
    :return:
    """
    caplog.set_level(logging.ERROR)
    inc_index = ['2020-01-01','2021-01-01','2022-01-01']
    test_data =  {
            "value":[100,140,150],
            "value_growth_rate": [1.0, 5.0, 4.7]
    }
    test_df= pd.DataFrame(data=test_data,index=inc_index)
    target_msg_error = logging.getLogger('Graphing module')
    target_msg_error.addHandler(caplog.handler)
    test_graph = grapher.graph_generator(df=test_df,fig_title='TEST_INDEX_ERROR')
    assert isinstance(test_graph,go.Figure)
    assert len(test_graph.data) == 0
    assert 'DataFrame index is not a DatetimeIndex. Attempting auto conversion' in caplog.text
    assert "No 'date' column for conversion." in caplog.text

def test_auto_conversion(grapher,caplog):
    """
    Test that dates are correctly converted to a DatetimeIndex object automatically
    :param grapher:
    :param caplog:
    :return:
    """
    caplog.set_level(logging.INFO)

    test_values = {
        "date":['2021-01-01','2022-01-01','2023-01-01'],
        "value":[100,140,150],
        "value_growth_rate":[1.0,5.0,4.7]
    }

    test_df = pd.DataFrame(data=test_values)
    test_logs = logging.getLogger('Graphing module')
    test_logs.addHandler(caplog.handler)
    test_graph = grapher.graph_generator(df=test_df,fig_title='TEST_INDEX_AUTO_CONVERSION')
    assert isinstance(test_graph,go.Figure)
    assert len(test_graph.data) ==2
    assert 'DataFrame index is not a DatetimeIndex. Attempting auto conversion' in caplog.text
    assert 'Manual Plotly figure successfully generated' in caplog.text

@pytest.mark.filterwarnings('ignore::UserWarning')
def test_bad_dates(caplog,grapher):
    """
    Test that an error is logged if the dates are not able
    to be converted, to a DatetimeIndex
    :param caplog: captures logging messages
    :param grapher: holds go.Figure object
    :return:
    """
    caplog.set_level(logging.ERROR)
    target_error_msg = logging.getLogger('Graphing module')
    target_error_msg.addHandler(caplog.handler)
    # construct df with bad data to force an exception
    bad_data = {
        'date':['lizard-king','Squid'],
        'value':[100,200],
        'value_growth_rate':[0.1,0.2]
    }
    bad_df = pd.DataFrame(data=bad_data)
    test_graph = grapher.graph_generator(df=bad_df,fig_title='TEST FINAL EXCEPTION')
    assert isinstance(test_graph,go.Figure)
    assert len(test_graph.data) == 0
    assert 'Error converting DataFrame index' in caplog.text


    


    
















