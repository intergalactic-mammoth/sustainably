"""
Providing charts based on user statistics.
"""

from flask import config
from flask_restful import Resource
import pandas as pd

import plotly.express as px
from plotly import offline
import plotly.graph_objects as go
import numpy as np

class Chart(Resource):

    def _carbon_footprint_over_time(self, user_id):
        # user_data = pd.read_csv(f"data/user/{user_id:03d}.csv")

        # Need function to create data, this is just some dummy data
        df = px.data.stocks()
        carbon_footprint_over_time_line_plot: go.Figure = px.line(
            data_frame=df,
            x="date",
            y="GOOG",
            template="plotly_dark",
        )


        carbon_footprint_over_time_line_plot.update_layout(
            xaxis_title="",
            yaxis_title="Carbon Footprint",
            modebar=None,
        )

        carbon_footprint_over_time_line_plot.show(
            config={
                "displayModeBar": False,
                "staticPlot": True,
            }
        )

    def get(self, user_id, chart_type=None):
        x = np.linspace(0, 2, 100)
        y = np.sin(x)

        fig = px.line(x=x, y=y)

        fig_div = offline.plot(
            figure_or_data=fig,
            include_plotlyjs=False,
            output_type="div"
        )

        return fig_div

if __name__ == "__main__":
    chart_resource = Chart()
    chart_resource._carbon_footprint_over_time(1)