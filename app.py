import pandas as pd
import logging
import pathlib
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from logs.logs import Logs
from shinywidgets import output_widget, render_widget
from server.app_server import GDP_DATA_SERVER

# Load environment variables
load_dotenv()

app_dir = pathlib.Path(__file__).parent
class FRED_GDP_UI(Logs):
    """
    Encapsulates UI and server logic for fred_data module
    """

    LANG_CONST = tuple(["en", "es", "fr", "de", "ja", "ko", "zh-CN", "zh-TW"])

    def __init__(self):
        super().__init__(name="app module", level=logging.INFO)
        self.gdp_navbar = None
        # Set current file to base directory
        self._max_date = None
        self._min_date = None

    def gdp_nav_container(self):
        try:
            self._min_date = pd.to_datetime("1987-01-01")
            self._max_date = pd.to_datetime("2025-01-01")

            # Object to hold logo
            gdp_logo = ui.tags.a(
                ui.tags.img(src="logo_2.png", alt="Go GDP Homepage.Click Logo to be taken to homepage"),
                href="/",
                class_="Logo"
            )
            # Navigational links
            # GDP page content
            gdp_panel = ui.nav_panel(
                "GDP",
                ui.div(
                    # GDP card
                    ui.div(
                        ui.h4("Latest GDP Insights"),
                        ui.input_slider(
                            "date_range",
                            "Select Date Range",
                            min=self._min_date,
                            max=self._max_date,
                            value=(
                                pd.to_datetime("2020-01-01"),
                                pd.to_datetime("2024-01-01"),
                            ),
                            time_format="%Y-%m-%d",
                            animate=ui.AnimationOptions(
                                interval=400,
                                loop=False,
                                play_button="Time lapse data",
                                pause_button="Stop Time lapse",
                            ),
                        ),
                        class_="slider_card",
                    ),
                    # Graph card
                    ui.div(
                        #ui.output_ui("gdp_growth_plot"),
                        output_widget("gdp_growth_plot"),
                        class_="plot_card",
                    ),
                    class_="main-container",
                ),
            )
            # About page content
            about_panel = ui.nav_panel(
                "About",
                ui.div(
                    ui.h2("About the GDP Visualizer"),
                    ui.p(
                        "Welcome! This interactive dashboard was created to explore and visualize ",
                        "U.S. Real GDP and quarterly growth trends."
                    ),

                    ui.h2("Project Purpose"),
                    ui.p(
                        "This application was developed as the final project for the ",
                        ui.a(
                            "CS50 Introduction to Programming with Python",
                            href="https://cs50.harvard.edu/python/2022/",
                            target="_blank",
                        ),
                        " course from Harvard University. The goal was to demonstrate proficiency ",
                        "in Python by building a full-stack web application that interacts with a live API."
                    ),

                    ui.h2("Technology Stack"),
                    ui.p("This application is built in Python, utilizing the following libraries:"),
                    ui.tags.ul(
                        ui.tags.li(ui.tags.strong("Shiny for Python:"), " For the web framework and user interface."),
                        ui.tags.li(ui.tags.strong("Pandas:"), " For data manipulation and analysis."),
                        ui.tags.li(ui.tags.strong("Plotly:"), " For creating interactive visualizations."),
                        ui.tags.li(ui.tags.strong("aiohttp / requests:"),
                                   " For fetching data from the FRED API.")
                    ),

                    ui.h2("Data Source"),
                    ui.p(
                        "All economic data is sourced from the ",
                        ui.a(
                            "Federal Reserve Economic Data (FRED) API",
                            href="https://fred.stlouisfed.org/",
                            target="_blank",
                        ),
                        "."
                    ),

                    ui.h2("Developer"),
                    ui.p(
                        "Created by Vince Dority. You can view the source code on ",
                        # Replace with your actual GitHub repo link
                        ui.a(
                            "GitHub",
                            href="https://github.com/vidoh89/CS50_Final_project",
                            target="_blank",
                        ),
                        "."
                    ),
                    class_="main-container",
                ),
            )
            ####################

            return ui.page_bootstrap(
                ui.tags.head(
                    ui.tags.meta(charset="UTF-8"),
                    ui.tags.meta(name="viewport",content="width=device-width,initial-scale=1.0"),
                    ui.tags.meta(name="description",content="An application visualizing US Real GDP and Quarterly "
                                                            "Growth Rate data from FRED."),
                    ui.tags.title("GDP Growth Rate"),
                    ui.include_css("www/theme/style.css")
                             ),

                ui.div(
                    ui.page_navbar(
                        gdp_panel, about_panel, title=gdp_logo, id="main_nav", bg=None
                    ),
                    class_="page-container"
                )
            )

        except Exception as e:
            self.error(f"Could not generate UI: Error{e}")
            return ui.page_fluid(ui.p("Error building the application ui"))


my_app_ui = FRED_GDP_UI()
server_inst = GDP_DATA_SERVER()

# call server method
server = server_inst.get_server()
base_dir = pathlib.Path(__file__).parent.resolve()

app = App(my_app_ui.gdp_nav_container(), server, static_assets=app_dir/"www")
if __name__ == "__main__":
    app.run()
