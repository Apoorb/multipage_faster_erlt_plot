import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

erlt_df_2014_2014b_1 = pd.read_parquet("data/erlt_2014_2014b.parquet")


area_label_value = [
    {"label": area, "value": area} for area in erlt_df_2014_2014b_1.Area.unique()
]
pollutants_label_value = [
    {"label": pollutant, "value": pollutant}
    for pollutant in erlt_df_2014_2014b_1.Pollutant.unique()
]
avgspeed_values = erlt_df_2014_2014b_1["Average Speed (mph)"].unique()
avgspeed_values_marks_dict = {
    int(avg_speed) if avg_speed % 1 == 0 else avg_speed: f"{avg_speed}"
    for avg_speed in avgspeed_values
    if avg_speed % 5 == 0
}
avgspeed_values_marks_dict[2.5] = "2.5"
min_avgspeed = min(avgspeed_values)
max_avgspeed = max(avgspeed_values)

year_values = erlt_df_2014_2014b_1["Year"].unique()
year_values_marks_dict = {
    int(year) if year % 1 == 0 else year: f"{year}"
    for year in year_values
    if year % 5 == 0
}
min_year = min(year_values)
max_year = max(year_values)


app.layout = html.Div(
    [
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="eight columns",
                    children=[
                        html.H1(
                            "Current and Previous Study (MOVES 2014b vs. 2014) "
                            "Running Emission "
                            "Rate Look-Up Table Comparison"
                        ),
                        dcc.Dropdown(
                            id="area-dropdown",
                            options=area_label_value,
                            value="Austin",
                            multi=False,
                        ),
                        dcc.Dropdown(
                            id="pollutant-dropdown",
                            options=pollutants_label_value,
                            value="CO",
                            multi=False,
                        ),
                        dcc.Graph(id="erlt_comp_line"),
                        html.P(id="year_lab"),
                        dcc.Slider(
                            id="year-slider",
                            min=min_year,
                            max=max_year,
                            value=min_year,
                            marks=year_values_marks_dict,
                        ),
                        dcc.Graph(id="erlt_comp_line1"),
                        html.P(id="year_lab1"),
                        dcc.Slider(
                            id="year-slider1",
                            min=min_year,
                            max=max_year,
                            value=min_year,
                            marks=year_values_marks_dict,
                        ),
                    ],
                ),
                html.Div(
                    className="four columns",
                ),
            ],
        ),
    ]
)


@app.callback(Output("year_lab", "children"), [Input("year-slider", "value")])
def update_year_val(year_val):
    return f"Year Selected: {year_val}"


@app.callback(Output("year_lab1", "children"), [Input("year-slider1", "value")])
def update_year_val1(year_val1):
    return f"Year Selected: {year_val1}"


@app.callback(
    Output("erlt_comp_line", "figure"),
    [
        Input("area-dropdown", "value"),
        Input("pollutant-dropdown", "value"),
        Input("year-slider", "value"),
    ],
)
def update_line_chart(area_val, pollutant_val, year_val):
    max_em = erlt_df_2014_2014b_1.loc[
        lambda df: (df.Pollutant == pollutant_val), "Emission Rate (grams/mile)"
    ].values.max()

    min_em = erlt_df_2014_2014b_1.loc[
        lambda df: (df.Pollutant == pollutant_val), "Emission Rate (grams/mile)"
    ].values.min()

    erlt_df_2014_2014b_1_fil = erlt_df_2014_2014b_1.loc[
        lambda df: (
            (df.Area == area_val)
            & (df.Pollutant == pollutant_val)
            & (df["Year"] == year_val)
        )
    ].assign(Year=lambda df: df.Year.astype(int))
    fig = px.line(
        data_frame=erlt_df_2014_2014b_1_fil,
        x="Average Speed (mph)",
        y="Emission Rate (grams/mile)",
        hover_data=erlt_df_2014_2014b_1_fil.columns,
        line_dash="Study",
        color="Study",
        facet_col="Road Description",
        facet_col_wrap=2,
        template="plotly",
    )

    fig.update_layout(
        font=dict(family="Time New Roman", size=18, color="black"),
        yaxis=dict(
            range=(min_em, max_em * 1.2),
            showexponent="all",
            exponentformat="e",
            title_text="",
        ),
        xaxis=dict(
            range=(0, 80), showexponent="all", exponentformat="e", title_text=""
        ),
        yaxis3=dict(showexponent="all", exponentformat="e", title_text=""),
        xaxis2=dict(showexponent="all", exponentformat="e", title_text=""),
        hoverlabel=dict(font_size=14, font_family="Rockwell"),
    )
    fig.add_annotation(
        {
            "showarrow": False,
            "text": "Average Speed (mph)",
            "x": 0.5,
            "xanchor": "center",
            "xref": "paper",
            "y": 0,
            "yanchor": "top",
            "yref": "paper",
            "yshift": -30,
        }
    )
    fig.add_annotation(
        {
            "showarrow": False,
            "text": "Running Emission Rates (grams/mile)",
            "textangle": 270,
            "x": 0,
            "xanchor": "left",
            "xref": "paper",
            "y": 0.5,
            "yanchor": "middle",
            "yref": "paper",
            "xshift": -80,
        }
    )
    return fig


@app.callback(
    Output("erlt_comp_line1", "figure"),
    [
        Input("area-dropdown", "value"),
        Input("pollutant-dropdown", "value"),
        Input("year-slider1", "value"),
    ],
)
def update_line_chart(area_val, pollutant_val, year_val):
    max_em = erlt_df_2014_2014b_1.loc[
        lambda df: (df.Pollutant == pollutant_val), "Emission Rate (grams/mile)"
    ].values.max()

    min_em = erlt_df_2014_2014b_1.loc[
        lambda df: (df.Pollutant == pollutant_val), "Emission Rate (grams/mile)"
    ].values.min()

    erlt_df_2014_2014b_1_fil = erlt_df_2014_2014b_1.loc[
        lambda df: (
            (df.Area == area_val)
            & (df.Pollutant == pollutant_val)
            & (df["Year"] == year_val)
        )
    ].assign(Year=lambda df: df.Year.astype(int))
    fig = px.line(
        data_frame=erlt_df_2014_2014b_1_fil,
        x="Average Speed (mph)",
        y="Emission Rate (grams/mile)",
        line_dash="Study",
        color="Study",
        hover_data=erlt_df_2014_2014b_1_fil.columns,
        facet_col="Road Description",
        facet_col_wrap=2,
        template="plotly",
    )

    fig.update_layout(
        font=dict(family="Time New Roman", size=18, color="black"),
        yaxis=dict(
            range=(min_em, max_em * 1.2),
            showexponent="all",
            exponentformat="e",
            title_text="",
        ),
        xaxis=dict(
            range=(0, 80), showexponent="all", exponentformat="e", title_text=""
        ),
        yaxis3=dict(showexponent="all", exponentformat="e", title_text=""),
        xaxis2=dict(showexponent="all", exponentformat="e", title_text=""),
        hoverlabel=dict(font_size=14, font_family="Rockwell"),
    )
    fig.add_annotation(
        {
            "showarrow": False,
            "text": "Average Speed (mph)",
            "x": 0.5,
            "xanchor": "center",
            "xref": "paper",
            "y": 0,
            "yanchor": "top",
            "yref": "paper",
            "yshift": -30,
        }
    )
    fig.add_annotation(
        {
            "showarrow": False,
            "text": "Running Emission Rates (grams/mile)",
            "textangle": 270,
            "x": 0,
            "xanchor": "left",
            "xref": "paper",
            "y": 0.5,
            "yanchor": "middle",
            "yref": "paper",
            "xshift": -80,
        }
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
