import logging
import pandas as pd
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.fred_data_cleaner import Fred_Data_Cleaner
from utils.csv_data_retriever import Get_Data
from data.fred_data import FRED_API
from logs.logs import Logs
from typing import Union,Optional
from pathlib import Path

class Graph_For_Data(Logs):
    """
    Graph data provided by FRED_DATA_Cleaner
    """
    def __init__(self):
        """
        Initialize graph object to output data provided by FRED API
        """
        super().__init__(name ='Graphing module',level=logging.INFO)
        self.info('Initiating graphing process')

    def graph_generator(self,df:pd.DataFrame,fig_title:Optional[str]="US Real GDP and Quarterly Growth Rate"):
        """
        Graphing component for GRAPH_FOR_DATA object
        :param df: Data frame containing clean GDP data
        :type df: pd.DataFrame
        :return: A plotly.graph_objects.Figure object.
        :rtype: plotly.graph_objects.Figure
        """
        if df.empty:
            self.warning('DataFrame has no content,returning empty Figure.')
            return go.Figure()
        self.info("Generating Plotly figure")
        if not isinstance(df.index,pd.DatetimeIndex):
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

        # Create figure with secondary y_axis
        fig = make_subplots(specs=[[{"secondary_y":True}]])

        # GDP value trace
        fig.add_trace(
            go.Scatter(x=df.index,y=df['value'],name='Real GDP (Billions)',mode='lines+markers'),
            secondary_y=False,
        )
        # GDP value_growth_rate trace
        fig.add_trace(
            go.Scatter(x=df.index, y=df['value_growth_rate'], name='Growth Rate(%)',mode='lines+markers'),
            secondary_y=True,
        )
        # Update figure layout
        fig.update_layout(
            title_text =fig_title,
            template='seaborn',
            hovermode="x unified",
            legend=dict(x=0.01,y=0.99,bgcolor='rgba(255,255,255,0.9)'),
            margin=dict(l=40,r=40,b=25,t=120),
            title=dict(
                font=dict(size=11,weight='bold')

            ),
            title_font_family='Open Sans',

        )
        # Set x-axis properties
        fig.update_xaxes(
            title_text="Date(Quarterly)",
            type='date',
            showgrid=True,
            tickformat="%Y Q%q", #Date format Year(Quarter)
            # responsive tick settings
            tickfont=dict(size=8)

        )
        # set y-axes titles and properties
        fig.update_yaxes(
            title_text='Real GDP(Billions of $)',
            secondary_y=False,
            showgrid=True,
            zerolinewidth=2,
            zerolinecolor='LightGrey',
            range=[df['value'].min() * 0.9,df['value'].max()*1.1],
            # responsive settings for title and tick font
            title_font=dict(size=10),
            tickfont=dict(size=8)

        )
        fig.update_yaxes(
            title_text = "Growth Rate (%)",
            secondary_y  =True,
            showgrid=False,
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='LightGrey',
            range=[df['value_growth_rate'].min() * 1.2,df['value_growth_rate'].max() * 1.2],
            # responsive settings for title and tick font
            title_font=dict(size=10),
            tickfont=dict(size=8)
        )
        self.info("Plotly figure successfully generated.")
        return fig


if __name__ == '__main__':
    # Configure basic logging to see output from your custom Logs class during the test
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        # Step 1: Instantiate the data retriever to get the DataFrame
        logging.info("Attempting to load data...")
        data_loader = Get_Data()
        gdp_dataframe = data_loader.get_gdp_csv()

        # Step 2: Check if the DataFrame is valid before graphing
        if gdp_dataframe is not None and not gdp_dataframe.empty:
            logging.info("DataFrame loaded successfully. Now generating graph.")

            # Step 3: Instantiate the graphing class
            graph_creator = Graph_For_Data()

            # Step 4: Call the graphing method with the loaded DataFrame
            graph_creator.graph_generator(df=gdp_dataframe)
            logging.info("Graph generation complete.")

        else:
            logging.warning("Failed to load DataFrame or DataFrame is empty. Cannot generate graph.")

    except Exception as e:
        logging.error(f"An error occurred during the main execution: {e}", exc_info=True)
# --- TESTING BLOCK ---
if __name__ == '__main__':
    # Configure basic logging to see output from your custom Logs class during the test
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        # Step 1: Instantiate the data retriever to get the DataFrame
        logging.info("Attempting to load data...")
        data_loader = Get_Data()
        gdp_dataframe = data_loader.get_gdp_csv()

        # Step 2: Check if the DataFrame is valid before graphing
        if gdp_dataframe is not None and not gdp_dataframe.empty:
            logging.info("DataFrame loaded successfully. Now generating graph.")

            # Step 3: Instantiate the graphing class
            graph_creator = Graph_For_Data()

            # Step 4: Call the graphing method with the loaded DataFrame
            fig = graph_creator.graph_generator(df=gdp_dataframe)

            # Step 5: Save the figure to an HTML file and open it in a browser
            output_file = 'gdp_and_growth_rate_graph_practice.html'
            fig.write_html(output_file, auto_open=True)
            logging.info(f"Graph generation complete. Output saved to '{output_file}' and opened in browser.")

        else:
            logging.warning("Failed to load DataFrame or DataFrame is empty. Cannot generate graph.")

    except Exception as e:
        logging.error(f"An error occurred during the main execution: {e}", exc_info=True)





