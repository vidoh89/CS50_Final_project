import shiny.ui as ui
from shiny import App, render, reactive, Inputs, Outputs, Session
from datetime import date

app_ui = ui.page_fluid(
    ui.h3("Minimal Reactivity Test"),
    ui.input_slider(
        "date_range",
        "Select Date Range",
        min=date(2020, 1, 1),
        max=date(2024, 1, 1),
        value=(date(2021, 1, 1), date(2023, 1, 1)),
        time_format="%Y-%m-%d"
    ),
    ui.hr(),
    ui.h4("Output:"),
    ui.output_ui("result")
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def get_slider_values():
        print(f"--- Reactive Calc is running with: {input.date_range()} ---")
        return input.date_range()

    @render.ui
    def result():
        start, end = get_slider_values()
        print(f"--- Render UI is running with dates: {start} to {end} ---")
        return ui.p(f"The graph would be displayed here for the range: {start} to {end}")


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
