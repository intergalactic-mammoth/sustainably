"""
Providing charts based on user statistics.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Response
from flask_restful import Resource
from plotly import offline

from apis.utils.ChartUtils import co2_footprint, product_sustainability_breakdown


class Chart(Resource):

    def _carbon_footprint_over_time(self, user_id):
        """
        Create a timeseries line plot of the carbon footprint per day
        """
        DAYS_BACK = 5
        co2_data = co2_footprint(user_id=user_id, tail_days=DAYS_BACK)
        g = [x.values for x in co2_data]
        g = np.array(g).flatten()
        # Need function to create data, this is just some dummy data
        # carbon_footprint_over_time_line_plot: go.Figure = px.scatter(
        #     x=list(range(DAYS_BACK)),
        #     y=g,
        #     template="plotly_dark",
        # )
        carbon_footprint_over_time_line_plot = go.Figure(
            go.Scatter(
                x=np.arange(5) - 4 ,
                y=g,
                line_shape="spline",
            )
        )

        carbon_footprint_over_time_line_plot.update_layout(
            xaxis_title="Days Back",
            yaxis_title="Carbon Footprint",
            modebar=None,
            template="plotly_dark",
            xaxis_dtick=1,
        )

        return carbon_footprint_over_time_line_plot
    
    def _item_sustainability(self, user_id):
        """
        Create a pie plot with all items flagged as good, okay or bad
        """
        DAYS_BACK = 5
        data = product_sustainability_breakdown(
            user_id=user_id,
            tail_days=DAYS_BACK,
        )

        item_sustainability_pie_chart = go.Figure(
            data=go.Pie(
                labels=data.index,
                values=data,
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
            textfont_size=10,
        )

        return item_sustainability_pie_chart

    
    def _convert_to_div(self, figure):
        """
        Takes a plotly figure object and turns it into a str with an html div
        object that can then be embedded into a webpage.
        """
        figure_div = figure.to_html(
            include_plotlyjs=True,
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

            return Response(time_series_chart_div, mimetype="text/html")

        elif chart_type == "item_sustainability":
            pie_chart_div = self._convert_to_div(
                self._item_sustainability(
                    user_id=user_id,
                )
            )

            return Response(pie_chart_div, mimetype="text/html")
        
        else:
            raise ValueError("Requested Chart is not available")


def test():
    chart_resource = Chart()
    chart_resource._carbon_footprint_over_time(1).show(config={"displayModeBar": False})
    chart_resource._item_sustainability(1).show(config={"displayModeBar": False})

if __name__ == "__main__":
    test()
