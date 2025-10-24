import logging
import pandas as pd
import io
import plotly.graph_objects as go
from plotly import graph_objects
from plotly.subplots import make_subplots
from utils.fred_data_cleaner import Fred_Data_Cleaner
from utils.csv_data_retriever import Get_Data
from data.fred_data import FRED_API
from logs.logs import Logs
from typing import Union, Optional
from pathlib import Path


class Graph_For_Data(Logs):
    """
    Graph data provided by FRED_DATA_Cleaner
    """

    def __init__(self):
        """
        Initialize graph object to output data provided by FRED API
        """
        super().__init__(name='Graphing module', level=logging.INFO)
        self.info('Initiating graphing process')

    def graph_generator(self, df: pd.DataFrame, fig_title: Optional[str] = "US Real GDP and Quarterly Growth Rate") -> \
            Union[graph_objects.Figure,
            go.Figure]:
        """
        Graphing component for GRAPH_FOR_DATA object
        :param fig_title:
        :param df: Data frame containing clean GDP data
        :type df: pd.DataFrame
        :return: A plotly.graph_objects.Figure object.
        :rtype: plotly.graph_objects.Figure
        """

        if df.empty:
            self.warning('DataFrame has no content,returning empty Figure.')
            return go.Figure()
        self.info("Generating Plotly figure")
        if not isinstance(df.index, pd.DatetimeIndex):
            self.error("DataFrame index is not a DatetimeIndex. Attempting auto conversion")
            try:
                if "date" in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.set_index('date')
                else:
                    self.error("No 'date' column for conversion.")

            except Exception as e:
                self.error(f"Error converting DataFrame index to DateIndex: {e}")
                return go.Figure()

        # Create a new Figure()
        _fig = go.Figure()

        # adds trace for primary y-axis (Real GDP)
        _fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['value'].tolist(),
                name='Real GDP(Billions)',
                mode='lines+markers',
                line=dict(color='cyan',width=2),
                textfont=dict(size=4)
            )

        )
        # adds second trace for the gdp (Growth Rate)
        _fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['value_growth_rate'].tolist(),
                name='Growth Rate(%)',
                mode='lines+markers',
                line=dict(color='#ff6a00', width=2),
                yaxis='y2'
            )
        )
        # update figure layout
        _fig.update_layout(
            template='plotly_dark',
            title_text=fig_title,
            title="US Real GDP and Quarterly Growth Rate",
            title_x=0.5,
            title_y=0.75,
            font=dict(size=9.5,weight=500,color='#E8EAF6',textcase='normal',shadow='0px 1px 2px #9FA8DA'),
            hovermode="x unified",


            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.00,
                xanchor= 'center',
                x=0.5,
                bgcolor='rgba(0,0,0,0)',

            ),
            #margin=dict(l=500,r=5,b=50,t=100,pad=5),
            xaxis=dict(
                title_text="Date (Quarterly)",
                type='date',
                showgrid=True,
                tickformat="%Y Q%q",
                tickfont=dict(size=6),
            ),
            yaxis=dict(
                title_text="Real GDP($B)",
                showgrid=True,
                zerolinewidth=2,
                zerolinecolor='LightGrey',
                type='linear',
                title_font=dict(size=10),
                tickfont=dict(size=10)
            ),
            # plt secondary_y axis
            yaxis2=dict(
                title_text="Growth Rate (%)",
                overlaying='y',
                side='right',
                showgrid=False,
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='LightGrey',
                type='linear',
                title_font=dict(size=10),
                tickfont=dict(size=10),

            )

        )
        self.info("Manual Plotly figure successfully generated")
        return _fig
