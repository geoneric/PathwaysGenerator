import threading

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html


def application() -> Dash:
    # Incorporate data
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
    )

    # Initialize the app
    app = Dash(__name__)

    # TODO Set the title. Currently it is "Dash".

    # App layout
    app.layout = html.Div(
        [
            html.Div(children="My First App with Data, Graph, and Controls"),
            html.Hr(),
            dcc.RadioItems(
                options=["pop", "lifeExp", "gdpPercap"],
                value="lifeExp",
                id="my-final-radio-item-example",
            ),
            dash_table.DataTable(data=df.to_dict("records"), page_size=6),
            dcc.Graph(figure={}, id="my-final-graph-example"),
        ]
    )

    # Add controls to build the interaction
    @callback(
        Output(component_id="my-final-graph-example", component_property="figure"),
        Input(component_id="my-final-radio-item-example", component_property="value"),
    )
    def update_graph(col_chosen):
        fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
        return fig

    return app


def serve_dashboard(port_nr: int):
    app = application()

    process = threading.Thread(
        target=app.run,
        kwargs={"debug": False, "port": port_nr},
    )
    process.start()
