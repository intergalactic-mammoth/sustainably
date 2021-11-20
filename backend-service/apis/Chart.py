"""
Providing charts based on user statistics.
"""

from flask_restful import Resource
import pandas as pd

import plotly.express as px
from plotly import offline
import plotly.graph_objects as go
import numpy as np

class Chart(Resource):

    def _carbon_footprint_over_time(self, user_id):
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

        return carbon_footprint_over_time_line_plot
    
    def _item_sustainability(self, user_id):
        """
        Create a pie plot with all items flagged as good, okay or bad
        """
        dummy_data = pd.DataFrame({
            "names": ["Good", "Okay", "Bad"],
            "values": [4, 7, 10]
        })

        item_sustainability_pie_chart = go.Figure(
            data=go.Pie(
                labels=dummy_data["names"],
                values=dummy_data["values"],
                showlegend=False,
            ),
            layout=go.Layout(
                template="plotly_dark",
            )
        )

        item_sustainability_pie_chart.update_traces(
            textinfo="label+value",
            hoverinfo="percent",
            marker=dict(
                colors=["green", "blue", "red"],
                line_width=3,
            ),
            textfont_size=30,
        )

        return item_sustainability_pie_chart

    
    def _convert_to_div(self, figure):
        """
        Takes a plotly figure object and turns it into a str with an html div
        object that can then be embedded into a webpage.
        """
        figure_div = offline.plot(
            figure_or_data=figure,
            include_plotlyjs=False,
            output_type="div",
            config={
                "displayModeBar": False,
            }
        )

        return figure_div


    def get(self, user_id, chart_type=None):
        if chart_type is None:
            time_series_chart_div = self._convert_to_div(
                self._carbon_footprint_over_time(
                    user_id=user_id,
                )
            )

            pie_chart_div = self._convert_to_div(
                self._item_sustainability(
                    user_id=user_id,
                )
            )

            return_dict = {
                "footprint_over_time": time_series_chart_div,
                "item_sustainability": pie_chart_div,
            }

            return return_dict

        elif chart_type == "footprint_over_time":
            time_series_chart_div = self._convert_to_div(
                self._carbon_footprint_over_time(
                    user_id=user_id,
                )
            )

            return time_series_chart_div

        elif chart_type == "item_sustainability":
            pie_chart_div = self._convert_to_div(
                self._item_sustainability(
                    user_id=user_id,
                )
            )

            return pie_chart_div
        
        else:
            raise ValueError("Requested Chart is not available")


if __name__ == "__main__":
    chart_resource = Chart()
    chart_resource._carbon_footprint_over_time(1).show(config={"displayModeBar": False})
    chart_resource._item_sustainability(1).show(config={"displayModeBar": False})