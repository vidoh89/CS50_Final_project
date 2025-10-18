import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
import os
import pathlib
import plotly.io as pio
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from shinywidgets import render_widget, output_widget
from data.fred_data import FRED_API
from app_ui.graph_data import Graph_For_Data
from utils.fred_data_cleaner import Fred_Data_Cleaner
from utils.csv_data_retriever import Get_Data
from logs.logs import Logs
from typing import Optional, Union
from htmltools import TagList, div, Tag
from shiny.types import ImgData


class GDP_DATA_SERVER(Logs):
    """
    Server to handle output logic for FRED_GDP_UI application
    """

    def __init__(self):
        super().__init__(name='Server module', level=logging.INFO)

        # Initialize instance variables
        self.get_graph = Get_Data()
        self.graph_creator = Graph_For_Data()
        self.info("Loading GDP data.")
        self.gdp_df = self.get_graph.get_gdp_csv()
        if self.gdp_df is None or self.gdp_df.empty:
            self.warning("Failed to load GDP data or Dataframe is empty.")
        self.fred_client = FRED_API()

    def get_server(self):
        """
        Main server function to tie inputs to outputs.
        """

        def server(input: Inputs, output: Outputs, session: Session):
            """
            Server logic to generate output for input variables
            :param input:
            :param output:
            :param session:
            :return:
            """

            @render_widget
            async def gdp_growth_plot():
                """
                Plots gdp data

                """
                await asyncio.sleep(0.1)
                if not self.fred_client:
                    self.warning('Error fetching data from fred client using slider values provided')
                    return ui.p("Error: Fred client not initialized.")

                try:
                    # get start and end dates from input slider
                    start_date, end_date = input.date_range()
                    #start_date = pd.to_datetime("2020-01-01")
                    #end_date = pd.to_datetime("2024-01-01")
                    self.info(f'Slider date range selected {start_date} to{end_date}')
                    # format dates str('Year-month-date')
                    start_date_str = start_date.strftime('%Y-%m-%d')
                    end_date_str = end_date.strftime('%Y-%m-%d')

                    # API call parameters
                    gdp_params = {
                        'observation_start': start_date_str,
                        'observation_end': end_date_str
                    }
                    self.info(f"Fetching data for series <GDPC1> ,Params: {gdp_params} ")

                    async with self.fred_client:
                        df = await self.fred_client.get_series_obs('GDPC1', params=gdp_params)
                    if df is None or df.empty:
                        self.warning('No data returned from FRED API for the selected date range')
                        return ui.p(
                            "No data available for the selected date range.",
                            style="text-align:center;padding:2rem;"
                        )

                    cleaner = Fred_Data_Cleaner(df=df)
                    gdp_df = (
                        cleaner
                        .handle_missing_values()
                        .replace_columns()
                        .str_to_numb()
                        .calculate_pct_change()
                        .get_cleaned_data()
                    )

                    self.info('Successfully transformed GDP data.')
                    if gdp_df is not None and not gdp_df.empty:
                        self.info(f"Generating plot HTML with {len(gdp_df)} data points")
                        # fig = self.graph_creator.graph_generator(df=gdp_df)
                        # print(gdp_df.head())
                        # print(gdp_df.info())

                        # html_content = fig.to_html(
                        #     full_html=False,
                        #     config={'responsive':True},
                        #     div_id="custom_graph_scheme",
                        #
                        #     )
                        # print(type(html_content))
                        fig=go.Figure()
                        fig.add_trace(
                            go.Scatter(
                                x=gdp_df.index,
                                y=gdp_df['value'],
                                name='Real GDP(Billions)',
                                mode='lines+markers',
                                line=dict(color='cyan', width=2),
                            )
                        )

                        # adds second trace for the gdp (Growth Rate)
                        fig.add_trace(
                            go.Scatter(
                                x=gdp_df.index,
                                y=gdp_df['value_growth_rate'],
                                name='Growth Rate(%)',
                                mode='lines+markers',
                                yaxis='y2',
                                line=dict(color='#ff6a00', width=2)
                            )
                        )

                        # update figure layout
                        fig.update_layout(
                            template='plotly_dark',
                            title_text="US Real GDP and Quarterly Growth Rate",
                            title_x=0.5,
                            title_y=0.94,
                            font=dict(size=9.5, color='#E8EAF6'),
                            hovermode="x unified",
                            legend=dict(
                                orientation='h', yanchor='bottom', y=1.00,
                                xanchor='center', x=0.5, bgcolor='rgba(0,0,0,0)'
                            ),
                            margin=dict(l=50, r=50, b=50, t=100, pad=5),
                            xaxis=dict(
                                title_text="Date (Quarterly)", type='date',
                                showgrid=True, tickformat="%Y Q%q"
                            ),
                            yaxis=dict(
                                title_text="Real GDP($B)", showgrid=True,
                                zerolinewidth=2, zerolinecolor='LightGrey'
                            ),
                            yaxis2=dict(
                                title_text="Growth Rate (%)", overlaying='y',
                                side='right', showgrid=False, zeroline=True,
                                zerolinewidth=2, zerolinecolor='LightGrey'
                            )
                        )
                        return fig
                    else:
                        self.warning('Dataframe is empty after processing; rendering default message.')
                        return go.Figure()
                except Exception as e:
                    self.error(f'An error occurred while fetching FRED data:{e}')
                    return go.Figure()

        return server
