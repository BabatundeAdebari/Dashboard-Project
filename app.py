import os
import pathlib

import random
import json
import plotly.graph_objs as go
import dash_daq as daq

import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input, State, callback_context
import plotly.graph_objects as go
import dash_bootstrap_components as dbc 
from dash.dash_table.Format import Group
from datetime import datetime as dt

from business.index import get_analysis


# from dash.dash_table.Format import Group

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Traffic Dashboard"
server = app.server
# app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "spc_data.csv")))

params = list(df)
max_length = len(df)

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"

# Plotly mapbox public token
# mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_access_token = "pk.eyJ1IjoiZGV2cnVzIiwiYSI6ImNsbW9nbXlhbTBzNmIybHIyeTFodmttYWoifQ.qermGc0O6fT9BA2yx6RfCQ"

# Dictionary of important locations in New York
list_of_locations = {
    "London": {"lat": 51.509865, "lon": -0.118092},
    "Manchester": {"lat":  53.483959, "lon": -2.244644},
    "Glassgow": {"lat": 55.860916, "lon": -4.251433},
    "Edinburgh": {"lat": 55.953251, "lon":-3.188267},
    "Cardiff": {"lat":  51.481583, "lon": -3.179090 },
    "Norwich": {"lat":  52.630886, "lon": 1.297355},
    "Birmingham": {"lat": 52.489471, "lon": -1.898575},
    "Cambridge": {"lat": 52.205276, "lon": 0.119167},
    "Peterborough ": {"lat":52.573921, "lon":  -0.250830},
}

list_of_algorithm = [
    "DecisionTree",
    "RandomForest",
    "LogisticRegression",
    "SVM",
    "K Neighbors"
]



query =  get_analysis('pandas')


state_dict = query.init_data()

cities  = query.get_cities()


(x_years_label,y_years_label,v_years_label )= query.get_all_year_traffic()

YEARS = query.YEARS
CURRENT_YEAR = query.CURRENT_YEAR

(x_location,y_location) = query.get_traffic_by_location()
(x_season,y_season) = query.get_traffic_by_season()
(x_times,y_days,v_heat_map) = query.get_traffic_by_hours_and_days()
(x_hourly,y_hourly,text_hourly) = query.get_traffic_hourly_by_year(CURRENT_YEAR)



totalList = query.get_traffic_cities()

# APP_PATH = str(pathlib.Path(__file__).parent.resolve())
# ffpath = os.path.join(APP_PATH, os.path.join("data", "uk-district.json"))
# fpath =json.load(open(ffpath,'r'))

# la_data = []

# for i in range(len(fpath["features"])):
#     # Extract local authority name
#     la = fpath["features"][i]['properties']['LAD21NM']
#     # Assign the local authority name to a new 'id' property for later linking to dataframe
#     fpath["features"][i]['id'] = la
#     # While I'm at it, append local authority name to a list to make some dummy data to test, along with i for a value to test on map
#     la_data.append([la,i])

# df3 = pd.DataFrame(la_data)
# # update column names
# df3.columns = ['LA','Val']



# for i in fpath['features']:
#     i['properties']["id"] = i['properties']["LAD21NM"] 



def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("UK Traffic Analysis"),
                    html.H6("Process Control and System Reporting"),

                 
                ],
            ),
            html.Div(children=[

                dcc.Dropdown(
                    id="dropdown-year",
                    multi=False,
                    options=[{'label':x,'value':x} for x in YEARS],
                    value=YEARS
                )
            ],
             style={"width":"74%"},),
        ],
    )

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Analysis by city",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Control Charts Dashboard",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="MachineLearning-tab",
                        label="Machine Learning Dashboard",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="DynamicInput-tab",
                        label="Dynamic Input",
                        value="tab4",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def build_tab_1():
    return [
       
        html.Div(
            # id="settings-menu",
            children=[
               # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        
                        html.H5("SEE TRAFFIC CONGESTION BY CITY"),
                        html.P(
                            """Select different days using the date picker"""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2014, 4, 1),
                                    max_date_allowed=dt(2014, 9, 30),
                                    initial_visible_month=dt(2014, 4, 1),
                                    date=dt(2014, 4, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            placeholder="Select a location",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Select certain hours",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                       
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                            ],
                        )
                    ],
                ),
            ],
        ),
    ]

pct_data = [
     {
        "day":"Day of week",
        "value":"value(%)"
    },
    {
        "day":"Monday",
        "value":34
    },
    {
        "day":"Tuesday",
        "value":24
    },
    {
        "day":"Wednesday",
        "value":14
    },
    {
        "day":"Thursday",
        "value":67
    },
    {
        "day":"Friday",
        "value":12
    },
    {
        "day":"Saturday",
        "value":19
    },
    {
        "day":"Sunday",
        "value":36
    }
]

def aaa(a):
    return dbc.Button(
         className="dflex-space-around day",
        children=[
            a.get('day'),
            a.get('value')
        ])
    # return  html.Div(
    #     className="dflex-space-around day",
    #     children=[
    #         html.Span(children={'testing 1'}),
    #         html.Span(children={'testing 2'}),
    #     ]
    # )

def build_tab_3():
    return [ 
        html.Div(
            # id="settings-menu",
            children=[
               # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        
                        html.P(
                            """Select different location and algorithm"""
                        ),
                    
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                 html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location2-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            placeholder="Select a location",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="algorithm-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_algorithm
                                            ],
                                            placeholder="Select an Algorithm",
                                        )
                                    ],
                                ),
                              
                            ],
                        ),
                        html.Div(children=[
                        generate_section_banner("Scores"),
                        dbc.Row(
                            className="dflex",
                            style={"margin": "20px 0"},
                            children=[
                                # card_score("purple","Prediction","Tendency of 57%' chance of traffic on Fridays than any other days than most region",""),
                                # card_score("blue","Score","4.5","")
                            ]
                        )
                    ])

                        # html.P(id="total-rides-selection"),
                        # html.P(id="date-value"),
                       
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        
                        html.P(
                            """Days of week breakdown by pct(%)"""
                        ),
                    
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                dbc.Row(
                                    className="dflex",
                                    style={"margin": "20px 0"},
                                    children=[ 
                                        dbc.Col(
                                            children=[aaa(x) for x in pct_data]
                                        )
                                    ])
                            ],
                        )
                    ]
                ),
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        
                        # html.H5("SEE TRAFFIC CONGESTION BY CITY"),
                        html.P(
                            """Result"""
                        ),
                    
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                # html.Div(
                                #     className="div-for-dropdown",
                                #     children=[
                                #         # Dropdown for locations on map
                                #         dcc.Dropdown(
                                #             id="location-dropdown",
                                #             options=[
                                #                 {"label": i, "value": i}
                                #                 for i in list_of_locations
                                #             ],
                                #             placeholder="Select a location",
                                #         )
                                #     ],
                                # ),
                                # html.Div(
                                #     className="div-for-dropdown",
                                #     children=[
                                #         # Dropdown to select times
                                #         dcc.Dropdown(
                                #             id="bar-selector",
                                #             options=[
                                #                 {
                                #                     "label": str(n) + ":00",
                                #                     "value": str(n),
                                #                 }
                                #                 for n in range(24)
                                #             ],
                                #             multi=True,
                                #             placeholder="Select certain hours",
                                #         )
                                #     ],
                                # ),
                            ],
                        ),
                        # html.P(id="total-rides"),
                        # html.P(id="total-rides-selection"),
                        # html.P(id="date-value"),
                       
                    ],
                ),
            ],
        )
    ]


def build_tab_4():
      return [
       
        html.Div(
            # id="settings-menu",
            children=[
               "Testing for errors"
            ]
        )
    ]


def generate_heat_map():

    return html.Div(
        children=[
            generate_section_banner("Hourly traffic by days"),
            html.Div(children=[
                dcc.Graph(
                figure= go.Figure(
                    data=go.Heatmap(
                        x=x_times,
                        y=y_days,
                        type="heatmap",
                        hovertemplate="<b> %{y}  %{x} <br><br> %{z} Patient Records",
                        z=v_heat_map,
                        text=v_heat_map,
                        texttemplate="%{text}",
                        textfont={"size":10},
                        showscale=False,
                        colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
                    ),
                    layout = dict(
                        # margin=dict(l=70, b=50, t=50, r=50),
                        modebar={"orientation": "v"},
                        font=dict(family="Open Sans"),
                        paper_bgcolor= "rgba(0,0,0,0)",
                        plot_bgcolor= "rgba(0,0,0,0)",
                        # annotations=annotations,
                        # shapes=shapes,
                        xaxis=dict(
                            side="top",
                            ticks="",
                            ticklen=2,
                            tickfont=dict(family="sans-serif"),
                            tickcolor="#ffffff",
                            color="#f8f8f8"
                        ),
                        yaxis=dict(
                            side="left", 
                            ticks="", 
                            tickfont=dict(
                                family="sans-serif"), 
                                ticksuffix=" ",
                                color="#f8f8f8"
                        ),
                        hovermode="closest",
                        showlegend=False,
                    )
              )
                )
            ])
        ]
    )


# def populate_ooc(data, ucl, lcl):
#     ooc_count = 0
#     ret = []

#     for i in range(len(data)):
#         if data[i] >= ucl or data[i] <= lcl:
#             ooc_count += 1
#             ret.append(ooc_count / (i + 1))
#         else:
#             ret.append(ooc_count / (i + 1))
#     return ret



# ud_usl_input = daq.NumericInput(
#     id="ud_usl_input", className="setting-input", size=200, max=9999999
# )
# ud_lsl_input = daq.NumericInput(
#     id="ud_lsl_input", className="setting-input", size=200, max=9999999
# )
# ud_ucl_input = daq.NumericInput(
#     id="ud_ucl_input", className="setting-input", size=200, max=9999999
# )
# ud_lcl_input = daq.NumericInput(
#     id="ud_lcl_input", className="setting-input", size=200, max=9999999
# )



# @app.callback(
#     Output("patient_volume_hm", "figure"),
#     [
#         Input("date-picker-select", "start_date"),
#         Input("date-picker-select", "end_date"),
#         Input("clinic-select", "value"),
#         Input("patient_volume_hm", "clickData"),
#         Input("admit-select", "value"),
#         Input("reset-btn", "n_clicks"),
#     ],
# )
# def update_heatmap(start, end, clinic, hm_click, admit_type, reset_click):
#     start = start + " 00:00:00"
#     end = end + " 00:00:00"

#     reset = False
#     # Find which one has been triggered
#     ctx = dash.callback_context

#     if ctx.triggered:
#         prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
#         if prop_id == "reset-btn":
#             reset = True

#     # Return to original hm(no colored annotation) by resetting
#     return generate_patient_volume_heatmap(
#         start, end, clinic, hm_click, admit_type, reset
#     )



def build_value_setter_line(line_num, label, value, col3):
    return html.Div(
        id=line_num,
        children=[
            html.Label(label, className="four columns"),
            html.Label(value, className="four columns"),
            html.Div(col3, className="four columns"),
        ],
        className="row",
    )


def build_quick_stats_panel():
    return html.Div(
        # id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    generate_section_banner("Traffic by year"),
                    html.Div(
                        children=dcc.Graph(
                            id="bar-h",
                             className="mt-3",
                            figure=go.Figure(
                                {
                                    "data": [
                                        {
                                            "type": "bar",
                                            "x": x_years_label,
                                            "y": y_years_label,
                                            "text":v_years_label,
                                            "textposition": "auto",
                                            "width":1,
                                            "marker": {
                                                "color": '#2c7be5',
                                                "opacity": 0.6,
                                                "line": {
                                                  "color": '#fff',
                                                }
                                            },
                                            "orientation":"h",
                                            "name": ''
                                        }
                                    ],
                                    "layout": {
                                        "width":300,
                                        # "bargap": .1,
                                        # "height":300,
                                        "margin": dict(t=0, b=1, l=10, r=0, pad=1),
                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                        "plot_bgcolor": "rgba(0,0,0,0)",
                                        "xaxis": dict(
                                            showline=False, showgrid=False, zeroline=False,showticklabels= False
                                        ),
                                        "yaxis": dict(
                                            showgrid=False, showline=False, zeroline=False,showticklabels= True,color="#f8f8f8"
                                        ),
                                        "autosize": False,
                                    },
                                }
                            )
                        )
                    )
                ]
            ),
            html.Div(
                # id="card-2",
                children=[
                     html.Div(
                        id="ooc-piechart-outer2",
                        className="",
                        children=[
                            generate_section_banner("Location"),
                            generate_piechart()
                        ],
                    )
                ],
            ),
            # html.Div(
            #     id="utility-card",
            #     children=[daq.StopButton(id="stop-button", size=160, n_clicks=0)],
            # ),
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


def build_top_panel(stopped_interval):
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("2023 Traffic metric summary"),
                    html.Div(
                        id="metric-div",
                        children=[
                            generate_metric_list_header(),
                            html.Div(
                                id="metric-rows",
                                children=[
                                    generate_metric_row_helper(stopped_interval, 1),
                                    generate_metric_row_helper(stopped_interval, 2),
                                    generate_metric_row_helper(stopped_interval, 3),
                                    generate_metric_row_helper(stopped_interval, 4),
                                    generate_metric_row_helper(stopped_interval, 5),
                                    generate_metric_row_helper(stopped_interval, 6),
                                    generate_metric_row_helper(stopped_interval, 7),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Piechart
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("Road Condition"),
                    generate_piechart_road_type(),
                ],
            ),
        ],
    )


def generate_piechart():
    return dcc.Graph(
        id="piechart",
        figure={
            "data": [
                {
                    "labels": x_location,
                    "values": y_location,
                    "type": "pie",
                    "hole":.9,
                    "pull":[0.04, 0.04],
                    "textinfo":'value', # "label"
                    "marker": {
                        "colors":[ '#2c7be5', '#a6c5f7', '#d2ddec'],
                     
                        "opacity": 0.6,
                        "line":{
                            "color": "#a6c5f7", "width": .5
                        }
                    },
                    "hoverinfo": "label"
                }
            ],
            
            "layout": {
                
                # "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True
            },
        },
    )


def generate_piechart_road_type():
    return dcc.Graph(
        id="piechart",
        figure={
            "data": [
                {
                    "labels": x_season,
                    "values": y_season,
                    "type": "pie",
                    "hole":.9,
                    "pull":[0.04, 0.04, 0.04],
                    "textinfo":'value', # "label"
                    "marker": {
                        "colors":[  '#d2ddec', '#a6c5f7', '#2c7be5' ],
                        "line":{
                            "color": "#B39DDB", 
                            "width": .5
                        }
                    },
                    "hoverinfo": "value"
                }
            ],
            
            "layout": {
                
                # "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True
            },
        },
    )

# Build header
def generate_metric_list_header():
    return generate_metric_row(
        "metric_header",
        {"height": "3rem", "margin": "1rem 0", "textAlign": "center"},
        {"id": "m_header_1", "children": html.Div("Month")},
        {"id": "m_header_2", "children": html.Div("Count")},
        {"id": "m_header_3", "children": html.Div("Lines")},
        {"id": "m_header_4", "children": html.Div("OOC%")},
        {"id": "m_header_5", "children": html.Div("%OOC")},
        {"id": "m_header_6", "children": "Pass/Fail"},
    )


def generate_metric_row_helper(stopped_interval, index):
   
    item = params[index]
    months = ["","JAN","FEB","MAR","APR","MAY","JUN","JUL"]
    counts = ["","1.3k","3.4k","6.4k","2.3k","7.4k",".3k","5.3k"]

    div_id = item + suffix_row
    button_id = item + suffix_button_id
    sparkline_graph_id = item + suffix_sparkline_graph
    count_id = item + suffix_count
    ooc_percentage_id = item + suffix_ooc_n
    ooc_graph_id = item + suffix_ooc_g
    indicator_id = item + suffix_indicator

    return generate_metric_row(
        div_id,
        None,
        {
            "id": months[index],
            "className": "metric-row-button-text",
            "children": html.Button(
                id=button_id,
                className="metric-row-button",
                children=months[index],
                title="Click to visualize live SPC chart",
                n_clicks=0,
            ),
        },
        {"id": count_id, "children": counts[index]},
        {
            "id": item + "_sparkline",
            "children": dcc.Graph(
                id=sparkline_graph_id,
                style={"width": "100%", "height": "95%"},
                config={
                    "staticPlot": False,
                    "editable": False,
                    "displayModeBar": False,
                },
                figure=go.Figure(
                    {
                        "data": [
                            {
                                "x": state_dict["Batch"]["data"].tolist()[
                                    :stopped_interval
                                ],
                                "y": state_dict[item]["data"][:stopped_interval],
                                "mode": "lines+markers",
                                "name": item,
                                "line": {"color": "#f4d44d"},
                            }
                        ],
                        "layout": {
                            "uirevision": True,
                            "margin": dict(l=0, r=0, t=4, b=4, pad=0),
                            "xaxis": dict(
                                showline=False,
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                            ),
                            "yaxis": dict(
                                showline=False,
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                            ),
                            "paper_bgcolor": "rgba(0,0,0,0)",
                            "plot_bgcolor": "rgba(0,0,0,0)",
                        },
                    }
                ),
            ),
        },
        {"id": ooc_percentage_id, "children": "0.00%"},
        {
            "id": ooc_graph_id + "_container",
            "children": daq.GraduatedBar(
                id=ooc_graph_id,
                color={
                    "ranges": {
                        "#92e0d3": [0, 3],
                        "#f4d44d ": [3, 7],
                        "#f45060": [7, 15],
                    }
                },
                showCurrentValue=False,
                max=15,
                value=0,
            ),
        },
        {
            "id": item + "_pf",
            "children": daq.Indicator(
                id=indicator_id, value=True, color="#91dfd2", size=12
            ),
        },
    )


def generate_metric_row(id, style, col1, col2, col3, col4, col5, col6):
    if style is None:
        style = {"height": "8rem", "width": "100%"}

    return html.Div(
        id=id,
        className="row metric-row",
        style=style,
        children=[
            html.Div(
                id=col1["id"],
                className="one column",
                style={"margin-right": "2.5rem", "minWidth": "50px"},
                children=col1["children"],
            ),
            html.Div(
                id=col2["id"],
                style={"textAlign": "center"},
                className="one column",
                children=col2["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"height": "100%"},
                className="four columns",
                children=col3["children"],
            ),
            html.Div(
                id=col4["id"],
                style={},
                className="one column",
                children=col4["children"],
            ),
            html.Div(
                id=col5["id"],
                style={"height": "100%", "margin-top": "5rem"},
                className="three columns",
                children=col5["children"],
            ),
            html.Div(
                id=col6["id"],
                style={"display": "flex", "justifyContent": "center"},
                className="one column",
                children=col6["children"],
            ),
        ],
    )


def generate_hourly_map():
    return go.Figure(
        {
            "data": [
                {
                    "type": "bar",
                    "x": x_hourly,
                    "y": y_hourly,
                    "text":text_hourly,
                    "textposition": "outside",

                    "textfont":dict(
                        family="tahoma",
                        size=10,
                        color="#f8f8f8"
                    ),
                    "width":1,
                    "marker": {
                        'colorscale': px.colors.sequential.RdBu,
                        # 'colorscale': px.colors.sequential.Viridis,
                        "color": y_hourly,
                        # "opacity": 0.6,
                        "line": {
                          # "color": 'blue',
                        }
                    },
                    "orientation":"v",
                    "name": ''
                }
            ],
            "layout": {
                "width":1050,
                "bargap": .1,
                "height":350,
                "margin": dict(t=0, b=1, l=10, r=0, pad=1),
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "xaxis": dict(
                    showline=False, showgrid=False, zeroline=False,showticklabels= True,color="#f8f8f8"
                ),
                "yaxis": dict(
                    showgrid=False, showline=False, zeroline=False,showticklabels= True,color="#f8f8f8"
                ),
                "autosize": False,
            },
        }
    )


def card_severity(style,title,value,icon):
    return html.Div(
    className=f"card {style}",
    children=[
        html.Div(
        className="card-body",
        children=[

            html.Div(
              className="col",
              children=[
                html.H6(
                  className="text-uppercase text-muted mb-2",
                  children=title
                ),
                html.Span(
                  className="h2 mb-0",
                  children=value
                )
              ]
            ),
            html.Div(
              className="col-auto",
              children=[
                html.Span(
                  className="h2 fe fe-briefcase text-muted mb-0",
                  children=[

                  ]
                )
            ]
            )
        ]
    )
    ]
)

def card_score(style,title,value,icon):
    return html.Div(
    className=f"card {style}",
    children=[
        html.Div(
        className="card-body",
        children=[

            html.Div(
              className="col",
              children=[
                html.H6(
                  className="text-uppercase text-muted mb-2",
                  children=title
                ),
                html.Span(
                  className="h2 mb-0",
                  children=value
                )
              ]
            ),
            html.Div(
              className="col-auto",
              children=[
                html.Span(
                  className="h2 fe fe-briefcase text-muted mb-0",
                  children=[

                  ]
                )
            ]
            )
        ]
    )
    ]
)

def build_severity():
    return html.Div(children=[
        generate_section_banner("Severity"),
        dbc.Row(
            className="dflex",
            style={"margin": "20px 0"},
            children=[
                card_severity("purple","Construction","745.3 M",""),
                card_severity("blue","Minor","612.7 M",""),
                card_severity("light-blue","Fatal","367.1 M",""),
                # card_severity("white-blue","Fatal","142.3 M","")
            ]
        )
    ])


def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("Hourly Traffic"),
            dcc.Graph(
                # id="control-chart-live",
                figure=generate_hourly_map()
            ),
        ],
    )


def generate_graph(interval, specs_dict, col):
    stats = state_dict[col]
    col_data = stats["data"]
    mean = stats["mean"]
    ucl = specs_dict[col]["ucl"]
    lcl = specs_dict[col]["lcl"]
    usl = specs_dict[col]["usl"]
    lsl = specs_dict[col]["lsl"]

    x_array = state_dict["Batch"]["data"].tolist()
    y_array = col_data.tolist()

    total_count = 0

    if interval > max_length:
        total_count = max_length - 1
    elif interval > 0:
        total_count = interval

    ooc_trace = {
        "x": [],
        "y": [],
        "name": "Out of Control",
        "mode": "markers",
        "marker": dict(color="rgba(210, 77, 87, 0.7)", symbol="square", size=11),
    }

    for index, data in enumerate(y_array[:total_count]):
        if data >= ucl or data <= lcl:
            ooc_trace["x"].append(index + 1)
            ooc_trace["y"].append(data)

    histo_trace = {
        "x": x_array[:total_count],
        "y": y_array[:total_count],
        "type": "histogram",
        "orientation": "h",
        "name": "Distribution",
        "xaxis": "x2",
        "yaxis": "y2",
        "marker": {"color": "#f4d44d"},
    }

    fig = {
        "data": [
            {
                "x": x_array[:total_count],
                "y": y_array[:total_count],
                "mode": "lines+markers",
                "name": col,
                "line": {"color": "#f4d44d"},
            },
            ooc_trace,
            histo_trace,
        ]
    }

    len_figure = len(fig["data"][0]["x"])

    fig["layout"] = dict(
        margin=dict(t=40),
        hovermode="closest",
        uirevision=col,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": "darkgray"}, "orientation": "h", "x": 0, "y": 1.1},
        font={"color": "darkgray"},
        showlegend=True,
        xaxis={
            "zeroline": False,
            "showgrid": False,
            "title": "Batch Number",
            "showline": False,
            "domain": [0, 0.8],
            "titlefont": {"color": "darkgray"},
        },
        yaxis={
            "title": col,
            "showgrid": False,
            "showline": False,
            "zeroline": False,
            "autorange": True,
            "titlefont": {"color": "darkgray"},
        },
        annotations=[
            {
                "x": 0.75,
                "y": lcl,
                "xref": "paper",
                "yref": "y",
                "text": "LCL:" + str(round(lcl, 3)),
                "showarrow": False,
                "font": {"color": "white"},
            },
            {
                "x": 0.75,
                "y": ucl,
                "xref": "paper",
                "yref": "y",
                "text": "UCL: " + str(round(ucl, 3)),
                "showarrow": False,
                "font": {"color": "white"},
            },
            {
                "x": 0.75,
                "y": usl,
                "xref": "paper",
                "yref": "y",
                "text": "USL: " + str(round(usl, 3)),
                "showarrow": False,
                "font": {"color": "white"},
            },
            {
                "x": 0.75,
                "y": lsl,
                "xref": "paper",
                "yref": "y",
                "text": "LSL: " + str(round(lsl, 3)),
                "showarrow": False,
                "font": {"color": "white"},
            },
            {
                "x": 0.75,
                "y": mean,
                "xref": "paper",
                "yref": "y",
                "text": "Targeted mean: " + str(round(mean, 3)),
                "showarrow": False,
                "font": {"color": "white"},
            },
        ],
        shapes=[
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 1,
                "y0": usl,
                "x1": len_figure + 1,
                "y1": usl,
                "line": {"color": "#91dfd2", "width": 1, "dash": "dot"},
            },
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 1,
                "y0": lsl,
                "x1": len_figure + 1,
                "y1": lsl,
                "line": {"color": "#91dfd2", "width": 1, "dash": "dot"},
            },
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 1,
                "y0": ucl,
                "x1": len_figure + 1,
                "y1": ucl,
                "line": {"color": "rgb(255,127,80)", "width": 1, "dash": "dot"},
            },
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 1,
                "y0": mean,
                "x1": len_figure + 1,
                "y1": mean,
                "line": {"color": "rgb(255,127,80)", "width": 2},
            },
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 1,
                "y0": lcl,
                "x1": len_figure + 1,
                "y1": lcl,
                "line": {"color": "rgb(255,127,80)", "width": 1, "dash": "dot"},
            },
        ],
        xaxis2={
            "title": "Count",
            "domain": [0.8, 1],  # 70 to 100 % of width
            "titlefont": {"color": "darkgray"},
            "showgrid": False,
        },
        yaxis2={
            "anchor": "free",
            "overlaying": "y",
            "side": "right",
            "showticklabels": False,
            "titlefont": {"color": "darkgray"},
        },
    )

    return fig


def update_sparkline(interval, param):
    x_array = state_dict["Batch"]["data"].tolist()
    y_array = state_dict[param]["data"].tolist()

    if interval == 0:
        x_new = y_new = None

    else:
        if interval >= max_length:
            total_count = max_length
        else:
            total_count = interval
        x_new = x_array[:total_count][-1]
        y_new = y_array[:total_count][-1]

    return dict(x=[[x_new]], y=[[y_new]]), [0]


def update_count(interval, col, data):
    if interval == 0:
        return "0", "0.00%", 0.00001, "#92e0d3"

    if interval > 0:

        if interval >= max_length:
            total_count = max_length - 1
        else:
            total_count = interval - 1

        ooc_percentage_f = data[col]["ooc"][total_count] * 100
        ooc_percentage_str = "%.2f" % ooc_percentage_f + "%"

        # Set maximum ooc to 15 for better grad bar display
        if ooc_percentage_f > 15:
            ooc_percentage_f = 15

        if ooc_percentage_f == 0.0:
            ooc_grad_val = 0.00001
        else:
            ooc_grad_val = float(ooc_percentage_f)

        # Set indicator theme according to threshold 5%
        if 0 <= ooc_grad_val <= 5:
            color = "#92e0d3"
        elif 5 < ooc_grad_val < 7:
            color = "#f4d44d"
        else:
            color = "#FF0000"

    return str(total_count + 1), ooc_percentage_str, ooc_grad_val, color


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="value-setter-store", data=query.init_data()),
        dcc.Store(id="n-interval-stage", data=50)
    ],
)


# Get the Coordinates of the chosen months, dates and times
def getLatLonColor(selectedData, month, day):
    listCoords = totalList[month][day]

    # No times selected, output all times for chosen month and date
    if selectedData == None or len(selectedData) == 0:
        return listCoords
    listStr = "listCoords["
    for time in selectedData:
        if selectedData.index(time) != len(selectedData) - 1:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ") | "
        else:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ")]"
    return eval(listStr)

@app.callback(
    [
        Output("app-content", "children"), 
        Output("interval-component", "n_intervals")
    ],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
    suppress_callback_exceptions=True
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval

    if tab_switch == "tab3":
        return build_tab_3(), stopped_interval

    if tab_switch == "tab4":
            return build_tab_4(), stopped_interval

    return (
      
            html.Div(
            id="status-container",
            children=[
               
                build_quick_stats_panel(),
                dbc.Row(
                    children=[

                        html.Div(
                                id="graphs-container",
                                children=[
                                build_top_panel(stopped_interval), 
                                build_severity(),
                                build_chart_panel(),
                                generate_heat_map()
                            ],
                        ),
                    ]
                ),
                
            ],
        ),
        stopped_interval,
           
    )



# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "date"),
        # Input("bar-selector", "value"),
        # Input("location-dropdown", "value"),
    ]
)
def update_graph(datePicked):
    zoom = 5.0
    latInitial = 55.09621
    lonInitial = -4.0286298
    #  USA lat/ lng value
    # latInitial = 40.7272
    # lonInitial = -73.991251
    bearing = 0
    # datePicked, selectedData, selectedLocation
    # if selectedLocation:
    #     zoom = 12.0
    #     latInitial = list_of_locations[selectedLocation]["lat"]
    #     lonInitial = list_of_locations[selectedLocation]["lon"]

    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month - 4
    dayPicked = date_picked.day - 1
    selectedData = None
    listCoords = getLatLonColor(selectedData, monthPicked, dayPicked)

    return go.Figure(
        data=[
            # Data for all rides based on date and time
            go.Scattermapbox(
                lat=listCoords["Latitude"],
                lon=listCoords["Longitude"],
                mode="markers",
                cluster=dict(enabled=True),

                hoverinfo="lat+lon+text",
                text=listCoords.index.hour,
                marker=dict(
                    showscale=True,
                    color="#d8d8d8",
                    # color=np.append(np.insert(listCoords.index.hour, 0, 0), 23),
                    opacity=0.3,
                    size=5,
                    colorscale=[
                        [0, "#F4EC15"],
                        [0.04167, "#DAF017"],
                        [0.0833, "#BBEC19"],
                        [0.125, "#9DE81B"],
                        [0.1667, "#80E41D"],
                        [0.2083, "#66E01F"],
                        [0.25, "#4CDC20"],
                        [0.292, "#34D822"],
                        [0.333, "#24D249"],
                        [0.375, "#25D042"],
                        [0.4167, "#26CC58"],
                        [0.4583, "#28C86D"],
                        [0.50, "#29C481"],
                        [0.54167, "#2AC093"],
                        [0.5833, "#2BBCA4"],
                        [1.0, "#613099"],
                    ],
                    colorbar=dict(
                        title="Time of<br>Day",
                        x=0.93,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(color="#d8d8d8"),
                        titlefont=dict(color="#d8d8d8"),
                        thicknessmode="pixels",
                    ),
                ),
            ),
            # Plot of important locations on the map
            go.Scattermapbox(
                lat=[list_of_locations[i]["lat"] for i in list_of_locations],
                lon=[list_of_locations[i]["lon"] for i in list_of_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in list_of_locations],
                marker=dict(size=8, color="#29C481",),
            ),
        ],
        layout=go.Layout(
            autosize=True,
            height=630,
            width=1000,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=True,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": zoom,
                                        "mapbox.center.lon": lonInitial,
                                        "mapbox.center.lat": latInitial,
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )



# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)