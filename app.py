import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import json
from bisect import bisect_left, bisect_right
from math import floor, ceil
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from ds.visuals.VisualsBySubjects import score_dist
from ds.visuals.VisualsByYears import sankey
import base64
from dash.dependencies import Input, Output, State

sample1000 = pd.read_csv("ds/data/Dash Board/Subject/sample1000.csv", index_col=0)
science1000 = pd.read_csv("ds/data/Dash Board/Subject/science1000.csv", index_col=0)
social1000 = pd.read_csv("ds/data/Dash Board/Subject/social1000.csv", index_col=0)

score = {}
score[2018] = pd.read_csv('ds/data/diemthi2018.csv')
score[2019] = pd.read_csv('ds/data/diemthi2019.csv')
score[2020] = pd.read_csv('ds/data/diemthi2020.csv')
score[2021] = pd.read_csv('ds/data/diemthi2021.csv')

app = dash.Dash(__name__)


def build_banner():
    test_png = 'cover4.jpeg'
    test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.Img(src='data:image/png;base64,{}'.format(test_base64),
                             style={'max-height': '1500px', 'max-width': '1500px'}

                             ),
                    html.H1(children="National High School Exam Scores EDA Project",
                            style={
                                "color": "#000000",
                                'text-align': 'center',
                                'font': '40px/42px sans-serif',
                                'padding-bottom': '20px',
                                'padding-top': '20px',
                                'borderTop': '0px solid #000000',
                                'fontWeight': 'bold'
                            }),
                    html.H2(children="A web application designed to have an insight about the National High School Graduation examination results",
                            style={
                                "color": "#000000",
                                'text-align': 'center',
                                'font': '18px/24px sans-serif',
                                'padding-bottom': '0px',
                                'fontWeight': 'bold'
                            }),
                ],
            ),
        ],
    )


def build_tabs():
    tab_style = {
        'borderTop': '0px solid #45a39b',
        'borderLeft': '0px solid #d6d6d6',
        'borderRight': '0px solid #d6d6d6',
        'borderBottom': '0px solid #d6d6d6',
        'padding': '20px',
        'font': '14px/16px sans-serif',
        'backgroundColor': '#eef3f3',
        'fontWeight': 'bold',
        'border-radius': '20px',
        'margin': '20px',
        'align': 'center'

    }
    tab_selected_style = {
        'borderTop': '0px solid #000000',
        'borderLeft': '0px solid #d6d6d6',
        'borderRight': '0px solid #d6d6d6',
        'borderBottom': '0px solid #d6d6d6',
        'backgroundColor': '#cb4b7c',
        'padding': '20px',
        'font': '14px/16px sans-serif',
        'fontWeight': 'bold',
        'color': 'white',
        'border-radius': '20px',
        'margin': '20px',
        'align': 'center'
    }
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="overview-tab",
                        label="Overview",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        id="subject-tab",
                        label="Subjects",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        id="visual-tab",
                        label="Provinces",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        id="year-tab",
                        label="Years",
                        value="tab4",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, selected_style=tab_selected_style
                    ),
                ],
                style={'margin': '20px', 'border-radius': '20px'}
            )
        ],
    )

########################################################################################################################
"""
TAB 1
"""
participant_each_year = pd.read_csv('ds/data/Dash Board/Overview/participant_each_year.csv')
fig2 = px.bar(participant_each_year, x='year', y='Count', labels={'Count':'Participant number'})

economic_feature_df = pd.read_csv('ds/data/Dash Board/Overview/economic_feature_2021.csv')

def Choropleth_VN_2020(ProvinceInfo, feature, title_text):

    #Vietnam map
    vietnam_geo = json.load(open("ds/data/Dash Board/Overview/vietnam_state.geojson","r"))

    # Plotting
    fig = px.choropleth_mapbox(
        data_frame = ProvinceInfo,
        locations = 'CityCode',
        featureidkey="properties.Code",
        geojson = vietnam_geo,
        color = feature,
        color_continuous_scale = 'turbo',
        hover_name = "Province",
        mapbox_style = "carto-positron",
        center = {"lat": 16,"lon": 106},
        zoom = 4.5,
        title = title_text,
    )
    fig.update_geos(fitbounds = "locations", visible=False)
    return fig

def build_tab_1():
    return [html.Div(children=[
        html.Div(children=[
            html.H3("Total number of participants each year", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
            dcc.Graph("participant_each_year", figure=fig2)
            ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'}),
        html.Div(children=[
            html.H3("Number of participants in each province", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
            dcc.Slider(id='year_slider',min=2018, max=2021, step=None, marks={2018: '2018', 2019: '2019', 2020: '2020', 2021: '2021'}, value=2018),
            dcc.Graph("participant_province")
            ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'}),
        html.Div(children=[
            html.Div(children=[
                html.H3("Map number of participants each province", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
                dcc.Graph('map-participant-province')
                ], style={'width': '48%', 'display': 'inline-block', 'margin-left': '20px'}),
            html.Div(children=[
                html.H3("Map economic feature 2021", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
                dcc.Graph('map-econimic-feature')
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'margin-right': '20px'})
            ]),
        html.Div(children=[
            html.H3("Economic feature 2021", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
            dcc.RadioItems(
                id='economic-feature',
                options=[{'label': 'Monthly Income', 'value': 'Monthly Income'},
                         {'label': 'Urban Ratio', 'value': 'Urban Ratio'},
                         {'label': 'Poverty Rate', 'value': 'Poverty Rate'}],
                value='Monthly Income', labelStyle={'display': 'block'},
                style={'padding': 10, 'flex': 1}),
            dcc.Graph("economic-feature-2021")
            ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'})                                                                                                                                                                                                                                      

        ])]


@app.callback(
    Output('participant_province', 'figure'),
    Output('map-participant-province', 'figure'),
    Input('year_slider', 'value')
)
def update_histogram(year):
    df = pd.read_csv(f'ds/data/Dash Board/Overview/participant_province_{year}.csv')
    fig1 = px.bar(df, x="Province", y="Count",barmode='group',color='Area')
    fig1.update_traces(width = 1)

    title = f"Vietnamese participants in {year}"
    fig2 = Choropleth_VN_2020(df, 'Count', title)

    return fig1, fig2

@app.callback(
    Output('economic-feature-2021', 'figure'),
    Output('map-econimic-feature', 'figure'),
    Input('economic-feature', 'value')
)

def sketch_economic_feature(feature):
    df = economic_feature_df[['CityCode', 'Province', 'AreaCode', 'Area', feature]]
    fig1 = px.bar(df, x="Province", y=feature,barmode='group',color='Area')
    fig1.update_traces(width = 1)

    title = "Vietnam Economy and Social map"
    fig2 = Choropleth_VN_2020(economic_feature_df, feature, title)

    return fig1, fig2

########################################################################################################################
"""
TAB 2
"""


def combi_tabs():
    tab_style = {
        'borderTop': '0px solid #45a39b',
        'borderLeft': '0px solid #d6d6d6',
        'borderRight': '0px solid #d6d6d6',
        'borderBottom': '0px solid #d6d6d6',
        'padding': '20px',
        'font': '14px/16px sans-serif',
        'backgroundColor': '#FFFFFF',
        'fontWeight': 'bold'
    }
    tab_selected_style = {
        'borderTop': '0px solid #000000',
        'borderLeft': '0px solid #d6d6d6',
        'borderRight': '0px solid #d6d6d6',
        'borderBottom': '3px solid #cb4b7c',
        'backgroundColor': '#FFFFFF',
        'padding': '20px',
        'font': '14px/16px sans-serif',
        'fontWeight': 'bold',
        'fontColor': '#45a39b',
    }
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="combi-tabs",
                value="science",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="science-tab",
                        label="Science",
                        value="science",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        id="subject-tab",
                        label="Social",
                        value="social",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, selected_style=tab_selected_style
                    ),
                ],
            )
        ],
    )


#
#
@app.callback(
    [Output("combi-checklist", "children")],
    [Input("combi-tabs", "value")],
)
def combi_option(tab_switch):
    checkbox_style = {
        'padding-left': '20px',
        'padding-top': '20px',
        'font': '14px/16px sans-serif',
        'fontWeight': 'bold',
        'padding-bottom': '20px',
        'text-align': 'center',
    }
    main_options = [
        {"label": "Math", "value": "Math"},
        {"label": "Literature", "value": "Literature"},
        {"label": "English", "value": "English"}
    ]
    science_options = [
        {"label": "Physics", "value": "Physics"},
        {"label": "Chemistry", "value": "Chemistry"},
        {"label": "Biology", "value": "Biology"}
    ]
    social_options = [
        {"label": "Geography", "value": "Geography"},
        {"label": "History", "value": "History"},
        {"label": "Civic Education", "value": "Civic Education"}
    ]
    if tab_switch == "science":
        return [
            dcc.Checklist(
                id="subject-checklist",
                options=main_options + science_options,
                value=["Math", "Literature", "English"],
                style=checkbox_style,
                labelStyle={'display': 'block', 'text-align': 'center', 'padding': '2px'}

            ),
        ]
    else:
        return [
            dcc.Checklist(
                id="subject-checklist",
                options=main_options + social_options,
                value=["Math", "Literature", "English"],
                style=checkbox_style,
                labelStyle={'display': 'block', 'align': 'center', 'padding': '2px'}
            ),
        ]


def setting_2():
    checkbox_style = {
        'padding-left': '10px',
        'font': '14px/16px sans-serif',
        'fontWeight': 'bold'
    }

    return html.Div([
        combi_tabs(),
        html.Div(id='combi-checklist')
    ])


@app.callback(
    [Output("correlogram", "figure"), Output("distribution", "figure")],
    [Input("subject-checklist", "value"), Input("combi-tabs", "value")],
)
def get_collelogram(subjects, tab):
    if tab == "science":
        return score_dist(science1000, subjects, "line", view="correlogram", shade=True, smooth=True), score_dist(
            sample1000, subjects, "line", view="together", shade=True, smooth=True)
    else:
        return score_dist(social1000, subjects, "line", view="correlogram", shade=True, smooth=True), score_dist(
            sample1000, subjects, "line", view="together", shade=True, smooth=True)


def build_tab_2():
    return [html.Div([
        # row1
        html.Div(children=[
            html.Div(children=[html.H3("Correlogram between subjects in 2021", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
                               dcc.Graph(id="correlogram", style={'padding-bottom': '20px'})
                               ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'}),
            html.Div([html.Div(children=[
                html.H3("Settings", style={
                    "color": "#000000",
                    'text-align': 'center',
                    'font': '14px/16px sans-serif',
                    'padding-bottom': '20px',
                    'padding-top': '20px',
                    'fontWeight': 'bold', 'color': 'white',
                    'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                    'margin': '0px'}),
                setting_2()], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                     'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'}),
                html.Div([
                    html.H3("Distribution of subjects in 2021", style={
                        "color": "#000000",
                        'text-align': 'center',
                        'font': '14px/16px sans-serif',
                        'padding-bottom': '20px',
                        'padding-top': '20px',
                        'fontWeight': 'bold', 'color': 'white',
                        'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px',
                        'border-top-right-radius': '20px', 'margin': '0px'}, ),
                    dcc.Graph(id="distribution", style={'padding-bottom': '20px'})
                ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                          'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'})
            ], style={'padding-left': '20px'})
        ], style={'display': 'flex', 'flex-direction': 'row', }),
        # html.Div([
        #     html.H3("Distribution of subjects", style={
        #                         "color": "#000000",
        #                         'text-align': 'center',
        #                         'font': '14px/16px sans-serif',
        #                         'padding-bottom': '10px',
        #                         'padding-top': '50px',
        #                         'fontWeight': 'bold'}),
        #     dcc.Graph(figure=score_dist(sample1000, ["Math", "English"], "line", view="together", shade = True, smooth=True))
        # ])
    ])]


########################################################################################################################
"""
TAB 3
"""
subject_option = [{"label": "Math", "value": 'Math'},
                     {"label": "Literature", "value": 'Literature'},
                     {"label": "English", "value": 'English'},
                     {"label": "Physics", "value": 'Physics'},
                     {"label": "Chemistry", "value": 'Chemistry'},
                     {"label": "Biology", "value": 'Biology'},
                     {"label": "Geography", "value": 'Geography'},
                     {"label": "History", "value": 'History'},
                     {"label": "Civic Education", "value": 'Civic Education'}]

province_option = [{'label': 'Hanoi', 'value': 1}, {'label': 'Ho Chi Minh City', 'value': 2}, 
                   {'label': 'Hai Phong', 'value': 3}, {'label': 'Da Nang', 'value': 4}, 
                   {'label': 'Ha Giang', 'value': 5}, {'label': 'Cao Bang', 'value': 6}, 
                   {'label': 'Lai Chau', 'value': 7}, {'label': 'Lao Cai', 'value': 8}, 
                   {'label': 'Tuyen Quang', 'value': 9}, {'label': 'Lang Son', 'value': 10}, 
                   {'label': 'Bac Kan', 'value': 11}, {'label': 'Thai Nguyen', 'value': 12}, 
                   {'label': 'Yen Bai', 'value': 13}, {'label': 'Son La', 'value': 14}, 
                   {'label': 'Phu Tho', 'value': 15}, {'label': 'Vinh Phuc', 'value': 16}, 
                   {'label': 'Quang Ninh', 'value': 17}, {'label': 'Bac Giang', 'value': 18}, 
                   {'label': 'Bac Ninh', 'value': 19}, {'label': 'Hai Duong', 'value': 21}, 
                   {'label': 'Hung Yen', 'value': 22}, {'label': 'Hoa Binh', 'value': 23}, 
                   {'label': 'Ha Nam', 'value': 24}, {'label': 'Nam Dinh', 'value': 25}, 
                   {'label': 'Thai Binh', 'value': 26}, {'label': 'Ninh Binh', 'value': 27}, 
                   {'label': 'Thanh Hoa', 'value': 28}, {'label': 'Nghe An', 'value': 29}, 
                   {'label': 'Ha Tinh', 'value': 30}, {'label': 'Quang Binh', 'value': 31}, 
                   {'label': 'Quang Tri', 'value': 32}, {'label': 'Thua Thien - Hue', 'value': 33}, 
                   {'label': 'Quang Nam', 'value': 34}, {'label': 'Quang Ngai', 'value': 35}, 
                   {'label': 'Kon Tum', 'value': 36}, {'label': 'Binh Dinh', 'value': 37}, 
                   {'label': 'Gia Lai', 'value': 38}, {'label': 'Phu Yen', 'value': 39}, 
                   {'label': 'Dak Lak', 'value': 40}, {'label': 'Khanh Hoa', 'value': 41}, 
                   {'label': 'Lam Dong', 'value': 42}, {'label': 'Binh Phuoc', 'value': 43}, 
                   {'label': 'Binh Duong', 'value': 44}, {'label': 'Ninh Thuan', 'value': 45}, 
                   {'label': 'Tay Ninh', 'value': 46}, {'label': 'Binh Thuan', 'value': 47}, 
                   {'label': 'Dong Nai', 'value': 48}, {'label': 'Long An', 'value': 49}, 
                   {'label': 'Dong Thap', 'value': 50}, {'label': 'An Giang', 'value': 51}, 
                   {'label': 'Ba Ria - Vung Tau', 'value': 52}, {'label': 'Tien Giang', 'value': 53}, 
                   {'label': 'Kien Giang', 'value': 54}, {'label': 'Can Tho', 'value': 55}, 
                   {'label': 'Ben Tre', 'value': 56}, {'label': 'Vinh Long', 'value': 57}, 
                   {'label': 'Tra Vinh', 'value': 58}, {'label': 'Soc Trang', 'value': 59}, 
                   {'label': 'Bac Lieu', 'value': 60}, {'label': 'Ca Mau', 'value': 61}, 
                   {'label': 'Dien Bien', 'value': 62}, {'label': 'Dak Nong', 'value': 63}, 
                   {'label': 'Hau Giang', 'value': 64}]

def plot_radar(data, range_x):
    categories = list(data.columns)
    fig = go.Figure()
    for i in range(data.shape[0]):
        fig.add_trace(go.Scatterpolar(
            r=list(data.loc[i].values),
            theta=categories,
            fill='toself',
            name=f'Label {i}'
        ))
    fig.update_layout(
        polar=dict(
        radialaxis=dict(
        visible=True,
        range=range_x,
      )),
         showlegend=False
    )
    return fig

def score_spectrum_province(df,subject,CityCode):

    data_province = df[df.CityCode == CityCode]
    subject_name = ''
    if (len(subject)<3 or ('-' in subject)):
        bins = [i/2 for i in range(0,61)]
        data_show = data_province[subject].value_counts(bins = bins).sort_index()
        subject_name = 'Combination: '+subject
    else:
        data_show = data_province[subject].value_counts().sort_index()
        subject_name = subject
        
    count_score = {'Score': pd.Series((data_show.index).astype('str')),
               'Count': pd.Series(data_show.values)}
    
    df = pd.DataFrame(count_score)
    fig = px.bar(df, x='Score', y='Count',title=City[CityCode]+': '+subject_name)
    return fig

#radar1
radar_data_1 = pd.read_csv('ds/data/Dash Board/Province/province_feature_radar.csv')
radar1 = radar_data_1.drop(['Label'], axis=1)
radar1 = plot_radar(radar1, [0,1])

#radar2
radar_data_2 = pd.read_csv('ds/data/Dash Board/Province/province_grade_radar.csv')
radar2 = radar_data_2.drop(['Label'],axis=1)
radar2 = plot_radar(radar2, [0,9])

#Map K-means
k_means_province  = pd.read_csv('ds/data/Dash Board/Province/k-means-province.csv')
title = "Vietnam clustering using economic features"
map_k_means = Choropleth_VN_2020(k_means_province, 'Label', title)

def build_tab_3():
    return [html.Div(children=[
        #parallel plot
        html.Div(children=[
            html.H3("Provinces grades proportion distribution",style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
            dcc.Dropdown(id="subject-dropdown1",
                 options=subject_option,
                 multi=False,
                 value='Math',
                 style={'width': "40%"}),
            dcc.Graph("province-parallel")
            ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'}),
        #Map K-means
        html.Div(children=[
            html.H3("Province clustering map",style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
            dcc.Graph('map-k-means', figure=map_k_means)
            ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'}),
        #radar chart
        html.Div(children=[
            #radar1
            html.Div(children=[
                html.H3("Province-clustering economic features radar",style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
                dcc.Graph('province-feature-radar', figure=radar1)
                ], style={'width': '48%', 'display': 'inline-block', 'margin-left': '20px'}),
            #radar2
            html.Div(children=[
                html.H3("Procinve-clustering grade radar",style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
                dcc.Graph('province-grade-radar', figure=radar2)
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'margin-right': '20px'})
            ])
        ])]

@app.callback(
    Output('province-parallel', 'figure'),
    Input('subject-dropdown1', 'value')
    )
def update_parallel_plot(subject):
    df = pd.read_csv(f'ds/data/Dash Board/Province/grade_each_province_{subject}.csv')
    fig = px.parallel_coordinates(
      df,
      color = "Area",
      labels = {'p02': 'Grade02', 'p24': 'Grade24', 'p46': 'Grade46', 'p68': 'Grade68', 'p810': 'Grade810'},
      color_continuous_scale=px.colors.diverging.Tealrose,
      color_continuous_midpoint=3)

    return fig

@app.callback(
    Output('histogram-province-grade', 'figure'),
    Input('province_dropdown', 'value'), 
    Input('subject-dropdown2', 'value')
    )
def histogram_province_grade(province_select, subject_select):
    fig = score_spectrum_province(score[2021], 'Math', 1)

    return radar1

########################################################################################################################
"""
TAB 4
"""
year_optionS = [{'label': '2018', 'value': 2018},
               {'label': '2019', 'value': 2019},
               {'label': '2020', 'value': 2020},]

year_optionT = [{'label': '2019', 'value': 2019},
               {'label': '2020', 'value': 2020},
               {'label': '2021', 'value': 2021}]

#Stack
def count_range(data,subject,mini,maxi):
    df1 = data[data[subject] >= mini]
    df2 = df1[df1[subject] <= maxi]
    return len(df2)

def AreaStack(subject):
    BigData = {2018: score[2018],
               2019: score[2019],
               2020: score[2020],
               2021: score[2021]}

    r1 = [count_range(BigData[2018+i],subject,0,5.1) for i in range(4)]
    r2 = [count_range(BigData[2018+i],subject,5.2,7.1) for i in range(4)]
    r3 = [count_range(BigData[2018+i],subject,7.2,8.0) for i in range(4)]
    r4 = [count_range(BigData[2018+i],subject,8.1,10) for i in range(4)]

    x=[2018,2019,2020,2021]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=r1,
        mode='lines',
        line=dict(width=0.5, color='rgb(190, 87, 12)'),
        stackgroup='one',
        name = '0 - 5.1',
        groupnorm='percent' # sets the normalization for the sum of the stackgroup
    ))
    fig.add_trace(go.Scatter(
        x=x, y=r2,
        mode='lines',
        line=dict(width=0.5, color='rgb(225, 105, 180)'),
        name = '5.2 - 7.1',
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=r3,
        mode='lines',
        line=dict(width=0.5, color='rgb(255, 220, 70)'),
        name = '7.2 - 8.0',
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=r4,
        mode='lines',
        line=dict(width=0.5, color='rgb(255, 10, 40)'),
        name = '8.1 - 10',
        stackgroup='one'
    ))

    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'),
        title = subject)
        # legend_title = "Score range")

    return fig

#Sankey
def add_label(data_path, ranges, colors, subject):
  province_avg = pd.read_csv(data_path)
  criteria = [province_avg[subject].between(r[0], r[1]) for r in ranges]
  province_avg['Level'] = np.select(criteria, [i for i in range(len(ranges))], 0)
  province_avg['Color'] = np.select(criteria, colors, 0)

  return province_avg[['CityCode', subject, 'Level', 'Color']]


def sankey(ranges, nodes, node_colors, path_colors, subject, weight=False):
  # plt.clf()
  # sns.set(style="darkgrid")
  # plt.rcParams['figure.figsize'] = (15, 10)
  province_avg2021 = add_label("ds/data/Province_Avg2021.csv", ranges, path_colors, subject)
  province_avg2020 = add_label("ds/data/Province_Avg2020.csv", ranges, path_colors, subject)
  province_avg2019 = add_label("ds/data/Province_Avg2019.csv", ranges, path_colors, subject)
  province_avg2018 = add_label("ds/data/Province_Avg2018.csv", ranges, path_colors, subject)

  if weight == False:
    value = [5] * 189
  else:
    value = list(province_avg2019[subject] - province_avg2018[subject]) + list(
      province_avg2020[subject] - province_avg2019[subject]) + list(
      province_avg2021[subject] - province_avg2020[subject])

  fig = go.Figure(data=[go.Sankey(
    node=dict(
      pad=15,
      thickness=15,
      line=dict(color="rgba(255, 0, 0, 0)", width=0.5),
      label=nodes * 4,
      color=node_colors * 4
    ),
    link=dict(
      source=list(province_avg2018['Level']) + list(province_avg2019['Level'] + len(ranges)) + list(
        province_avg2020['Level'] + 2 * len(ranges)),  # indices correspond to labels, eg A1, A2, A1, B1, ...
      target=list(province_avg2019['Level'] + len(ranges)) + list(province_avg2020['Level'] + 2 * len(ranges)) + list(
        province_avg2021['Level'] + 3 * len(ranges)),
      value=value,
      color=list(province_avg2018['Color']) + list(province_avg2019['Color']) + list(province_avg2020['Color'])
    ))])

  fig.update_layout(title_text=subject, font_size=10)
  
  return fig


#Exchange benchmark
grades = score
# Declare subjects combination
sbs = {}
sbs['A00'] = ["Math", "Physics", "Chemistry"]
sbs['A01'] = ["Math", "Physics", "English"]
sbs['A02'] = ["Math", "Physics", "Biology"]
sbs['A03'] = ["Math", "Physics", "History"]
sbs['A04'] = ["Math", "Physics", "Geography"]
sbs['A05'] = ["Math", "Chemistry", "History"]
sbs['A06'] = ["Math", "Chemistry", "Geography"]
sbs['A07'] = ["Math", "History", "Geography"]
sbs['A08'] = ["Math", "History", "Civic Education"]
sbs['A09'] = ["Math", "Geography", "Civic Education"]
sbs['A10'] = ["Math", "Physics", "Civic Education"]
sbs['A11'] = ["Math", "Chemistry", "Civic Education"]
sbs['B00'] = ["Math", "Chemistry", "Biology"]
sbs['B01'] = ["Math", "Biology", "History"]
sbs['B02'] = ["Math", "Biology", "Geography"]
sbs['B03'] = ["Math", "Biology", "Literature"]
sbs['B04'] = ["Math", "Biology", "Civic Education"]
sbs['B08'] = ["Math", "Biology", "English"]
sbs['C00'] = ["Literature", "History", "Geography"]
sbs['C01'] = ["Literature", "Math", "Physics"]
sbs['C02'] = ["Literature", "Math", "Chemistry"]
sbs['C03'] = ["Literature", "Math", "History"]
sbs['C04'] = ["Literature", "Math", "Geography"]
sbs['C05'] = ["Literature", "Physics", "Chemistry"]
sbs['C06'] = ["Literature", "Physics", "Biology"]
sbs['C07'] = ["Literature", "Physics", "History"]
sbs['C08'] = ["Literature", "Chemistry", "Biology"]
sbs['C09'] = ["Literature", "Physics", "Geography"]
sbs['C10'] = ["Literature", "Chemistry", "History"]
sbs['C12'] = ["Literature", "Biology", "History"]
sbs['C13'] = ["Literature", "Biology", "Geography"]
sbs['C14'] = ["Literature", "Math", "Civic Education"]
sbs['C16'] = ["Literature", "Physics", "Civic Education"]
sbs['C17'] = ["Literature", "Chemistry", "Civic Education"]
sbs['C19'] = ["Literature", "History", "Civic Education"]
sbs['C20'] = ["Literature", "Geography", "Civic Education"]
sbs['D01'] = ["Literature", "Math", "English"]
sbs['D07'] = ["Math", "Chemistry", "English"]
sbs['D08'] = ["Math", "Biology", "English"]
sbs['D09'] = ["Math", "History", "English"]
sbs['D10'] = ["Math", "Geography", "English"]
sbs['D11'] = ["Literature", "Physics", "English"]
sbs['D12'] = ["Literature", "Chemistry", "English"]
sbs['D13'] = ["Literature", "Biology", "English"]
sbs['D14'] = ["Literature", "History", "English"]
sbs['D15'] = ["Literature", "Geography", "English"]
sbs['D66'] = ["Literature", "Civic Education", "English"]
sbs['D84'] = ["Math", "Civic Education", "English"]
sbs['A00-Math'] = ["Math", "Physics", "Chemistry", "Math"]
sbs['A01-Math'] = ["Math", "Physics", "English", "Math"]
sbs['A02-Math'] = ["Math", "Physics", "Biology", "Math"]
sbs['A03-Math'] = ["Math", "Physics", "History", "Math"]
sbs['A04-Math'] = ["Math", "Physics", "Geography", "Math"]
sbs['A05-Math'] = ["Math", "Chemistry", "History", "Math"]
sbs['A06-Math'] = ["Math", "Chemistry", "Geography", "Math"]
sbs['A07-Math'] = ["Math", "History", "Geography", "Math"]
sbs['A08-Math'] = ["Math", "History", "Civic Education", "Math"]
sbs['A09-Math'] = ["Math", "Geography", "Civic Education", "Math"]
sbs['A10-Math'] = ["Math", "Physics", "Civic Education", "Math"]
sbs['A11-Math'] = ["Math", "Chemistry", "Civic Education", "Math"]
sbs['B00-Math'] = ["Math", "Chemistry", "Biology", "Math"]
sbs['B01-Math'] = ["Math", "Biology", "History", "Math"]
sbs['B02-Math'] = ["Math", "Biology", "Geography", "Math"]
sbs['B03-Math'] = ["Math", "Biology", "Literature", "Math"]
sbs['B04-Math'] = ["Math", "Biology", "Civic Education", "Math"]
sbs['B08-Math'] = ["Math", "Biology", "English", "Math"]
sbs['C00-Math'] = ["Literature", "History", "Geography", "Math"]
sbs['C01-Math'] = ["Literature", "Math", "Physics", "Math"]
sbs['C02-Math'] = ["Literature", "Math", "Chemistry", "Math"]
sbs['C03-Math'] = ["Literature", "Math", "History", "Math"]
sbs['C04-Math'] = ["Literature", "Math", "Geography", "Math"]
sbs['C05-Math'] = ["Literature", "Physics", "Chemistry", "Math"]
sbs['C06-Math'] = ["Literature", "Physics", "Biology", "Math"]
sbs['C07-Math'] = ["Literature", "Physics", "History", "Math"]
sbs['C08-Math'] = ["Literature", "Chemistry", "Biology", "Math"]
sbs['C09-Math'] = ["Literature", "Physics", "Geography", "Math"]
sbs['C10-Math'] = ["Literature", "Chemistry", "History", "Math"]
sbs['C12-Math'] = ["Literature", "Biology", "History", "Math"]
sbs['C13-Math'] = ["Literature", "Biology", "Geography", "Math"]
sbs['C14-Math'] = ["Literature", "Math", "Civic Education", "Math"]
sbs['C16-Math'] = ["Literature", "Physics", "Civic Education", "Math"]
sbs['C17-Math'] = ["Literature", "Chemistry", "Civic Education", "Math"]
sbs['C19-Math'] = ["Literature", "History", "Civic Education", "Math"]
sbs['C20-Math'] = ["Literature", "Geography", "Civic Education", "Math"]
sbs['D01-Math'] = ["Literature", "Math", "English", "Math"]
sbs['D07-Math'] = ["Math", "Chemistry", "English", "Math"]
sbs['D08-Math'] = ["Math", "Biology", "English", "Math"]
sbs['D09-Math'] = ["Math", "History", "English", "Math"]
sbs['D10-Math'] = ["Math", "Geography", "English", "Math"]
sbs['D11-Math'] = ["Literature", "Physics", "English", "Math"]
sbs['D12-Math'] = ["Literature", "Chemistry", "English", "Math"]
sbs['D13-Math'] = ["Literature", "Biology", "English", "Math"]
sbs['D14-Math'] = ["Literature", "History", "English", "Math"]
sbs['D15-Math'] = ["Literature", "Geography", "English", "Math"]
sbs['D66-Math'] = ["Literature", "Civic Education", "English", "Math"]
sbs['D84-Math'] = ["Math", "Civic Education", "English", "Math"]
sbs['A00-English'] = ["Math", "Physics", "Chemistry", "English"]
sbs['A01-English'] = ["Math", "Physics", "English", "English"]
sbs['A02-English'] = ["Math", "Physics", "Biology", "English"]
sbs['A03-English'] = ["Math", "Physics", "History", "English"]
sbs['A04-English'] = ["Math", "Physics", "Geography", "English"]
sbs['A05-English'] = ["Math", "Chemistry", "History", "English"]
sbs['A06-English'] = ["Math", "Chemistry", "Geography", "English"]
sbs['A07-English'] = ["Math", "History", "Geography", "English"]
sbs['A08-English'] = ["Math", "History", "Civic Education", "English"]
sbs['A09-English'] = ["Math", "Geography", "Civic Education", "English"]
sbs['A10-English'] = ["Math", "Physics", "Civic Education", "English"]
sbs['A11-English'] = ["Math", "Chemistry", "Civic Education", "English"]
sbs['B00-English'] = ["Math", "Chemistry", "Biology", "English"]
sbs['B01-English'] = ["Math", "Biology", "History", "English"]
sbs['B02-English'] = ["Math", "Biology", "Geography", "English"]
sbs['B03-English'] = ["Math", "Biology", "Literature", "English"]
sbs['B04-English'] = ["Math", "Biology", "Civic Education", "English"]
sbs['B08-English'] = ["Math", "Biology", "English", "English"]
sbs['C00-English'] = ["Literature", "History", "Geography", "English"]
sbs['C01-English'] = ["Literature", "Math", "Physics", "English"]
sbs['C02-English'] = ["Literature", "Math", "Chemistry", "English"]
sbs['C03-English'] = ["Literature", "Math", "History", "English"]
sbs['C04-English'] = ["Literature", "Math", "Geography", "English"]
sbs['C05-English'] = ["Literature", "Physics", "Chemistry", "English"]
sbs['C06-English'] = ["Literature", "Physics", "Biology", "English"]
sbs['C07-English'] = ["Literature", "Physics", "History", "English"]
sbs['C08-English'] = ["Literature", "Chemistry", "Biology", "English"]
sbs['C09-English'] = ["Literature", "Physics", "Geography", "English"]
sbs['C10-English'] = ["Literature", "Chemistry", "History", "English"]
sbs['C12-English'] = ["Literature", "Biology", "History", "English"]
sbs['C13-English'] = ["Literature", "Biology", "Geography", "English"]
sbs['C14-English'] = ["Literature", "Math", "Civic Education", "English"]
sbs['C16-English'] = ["Literature", "Physics", "Civic Education", "English"]
sbs['C17-English'] = ["Literature", "Chemistry", "Civic Education", "English"]
sbs['C19-English'] = ["Literature", "History", "Civic Education", "English"]
sbs['C20-English'] = ["Literature", "Geography", "Civic Education", "English"]
sbs['D01-English'] = ["Literature", "Math", "English", "English"]
sbs['D07-English'] = ["Math", "Chemistry", "English", "English"]
sbs['D08-English'] = ["Math", "Biology", "English", "English"]
sbs['D09-English'] = ["Math", "History", "English", "English"]
sbs['D10-English'] = ["Math", "Geography", "English", "English"]
sbs['D11-English'] = ["Literature", "Physics", "English", "English"]
sbs['D12-English'] = ["Literature", "Chemistry", "English", "English"]
sbs['D13-English'] = ["Literature", "Biology", "English", "English"]
sbs['D14-English'] = ["Literature", "History", "English", "English"]
sbs['D15-English'] = ["Literature", "Geography", "English", "English"]
sbs['D66-English'] = ["Literature", "Civic Education", "English", "English"]
sbs['D84-English'] = ["Math", "Civic Education", "English", "English"]

# Compute grades for each subjects combination
for year in grades:
  for sb in sbs:
    grades[year][sb] = 0
    for x in sbs[sb]:
      grades[year][sb] = grades[year][sb] + grades[year][x]
    grades[year][sb] *= 3/len(sbs[sb]) # Normalizing



# Return maximum grade of lowest p% candidates in given subjects combination list
def get_point(percentage, year, subjects_combination):
    data = grades[year][subjects_combination].max(1)
    data = [round(x,2) for x in data if not np.isnan(x)]
    data = sorted(data)
    if len(data) == 0: # Return 0 if not valid any candidates
        return 0
    return data[min(len(data)-1, floor(len(data)*percentage/100))]

# Return percentage range of given point
eps = 0.3 # (point-eps -> point+eps)
def get_percentage(point, year, subjects_combination):
    subjects_combination = [x for x in subjects_combination if x in list(grades[year].head())]
    data = grades[year][subjects_combination].max(1)
    data = [round(x,2) for x in data if not np.isnan(x)]
    data = sorted(data)
    if len(data) == 0: # Return (0, 0) if not valid any candidates
        return 0, 0
    return bisect_left(data, point-eps)/len(data)*100, bisect_right(data, point+eps)/len(data)*100

# Exchange point between source year and target year in given subjects combination list
def exchange(point, yearS, yearT, subjects_combination):
    subjects_combination = [x for x in subjects_combination if x in list(grades[year].head())]
    percentage = get_percentage(point, yearS, subjects_combination)
    return get_point(percentage[0], yearT, subjects_combination), get_point(percentage[1], yearT, subjects_combination)

def build_tab_4():
    return [html.Div(children=[
        #Sankey and stack
        html.Div(children=[
            #Sankey
            html.Div(children=[
                html.H3("Sankey", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
                dcc.Dropdown(id='sankey-subject',
                            options=[{"label": "Math", "value": 'Math'},
                                     {"label": "Literature", "value": 'Literature'},
                                     {"label": "English", "value": 'English'},
                                     {"label": "Physics", "value": 'Physic'},
                                     {"label": "Chemistry", "value": 'Chemistry'},
                                     {"label": "Biology", "value": 'Biology'},
                                     {"label": "Geography", "value": 'Geography'},
                                     {"label": "History", "value": 'History'},
                                     {"label": "Civic Education", "value": 'Civic Education'}],
                            multi=False,
                            value='Math',
                            style={'text-align': 'center', 'font': '14px/16px sans-serif'}
                            ),
                dcc.Graph('sankey-grade-year')
                ], style={'width': '48%', 'display': 'inline-block', 'margin-left': '20px'}),
            #Stack
            html.Div(children=[
                html.H3("Stack", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
                dcc.Dropdown(id='stack-subject',
                            options=subject_option,
                            multi=False,
                            value='Math',
                            style={'text-align': 'center', 'font': '14px/16px sans-serif'}
                            ),
                dcc.Graph('stack-grade-year')
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'margin-right': '20px'})
            ]),
        #Exchange benchmark
        html.Div(children=[
            html.H3("Exchange benchmark HUST", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
            html.Div(children=[
                html.Div(children=[
                    html.Label('Previous year'),
                    dcc.Dropdown(id='pre-year-drop',options=year_optionS,
                        multi=False,
                        value=2018,
                        style={'width': '40%'}),
                    html.Br(),
                    html.Label('Grade'),
                    dcc.Input(id='grade-input-state', type='number', placeholder='eg. 20.25', debounce=True, 
                        style={'width': '20%', 'margin-left': '20px'}),
                    html.Br(),
                    html.Br(),
                    html.Button(id='exchange-submit', n_clicks=0, children='Exchange')
                    ], style={'padding': 10, 'flex': 1}),
                html.Div(children=[
                    html.Label("Following year"),
                    dcc.Dropdown(id='fol-year-drop',options=year_optionT,
                        multi=False,
                        value=2019,
                        style={'width': '40%'}),
                    html.Br(),
                    html.Label("Subject combination"),
                    dcc.Input(id='subject-input-state', type='text', placeholder='eg. A00 or A00-Math (Math is the main subject)', debounce=True,
                        style={'width': '50%', 'margin-left': '20px'})
                    ], style={'padding': 10, 'flex': 1})
                ], style={'display': 'flex', 'flex-direction': 'row'}),
            html.Div(id="output-container", style={'padding': 10, 'flex': 1}),
            html.Br()
            ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'}),
        #Exchange benchmark graph
        html.Div(children=[
            html.H3("Exchange benchmark graph", style={
                "color": "white",
                'text-align': 'center',
                'font': '14px/16px sans-serif',
                'padding-bottom': '20px',
                'padding-top': '20px',
                'fontWeight': 'bold',
                'backgroundColor': '#cb4b7c', 'border-top-left-radius': '20px', 'border-top-right-radius': '20px',
                'margin': '0px'}),
            dcc.Checklist(id='year-checklist', options=year_optionT, value=[], style={'padding': 10, 'flex': 1}),
            dcc.Graph('exchange-grade-graph')
            ], style={'background-color': 'white', 'border-radius': '20px', 'margin-top': '20px',
                                         'margin-bottom': '20px', 'margin-left': '20px', 'margin-right': '20px'})
        ])]

@app.callback(
    Output('stack-grade-year', 'figure'),
    Input('stack-subject', 'value'))
def update_stack(subject):
    stack_diagram = AreaStack(subject)

    return stack_diagram

@app.callback(
    Output('sankey-grade-year', 'figure'),
    Input('sankey-subject', 'value')
    )
def update_sankey(subject_sankey):
    sankey_chart = sankey(ranges=[(0, 4.5), (4.5, 5.5), (5.5, 6.5), (6.5, 7), (7, 10)],
       nodes = ["0 - 4.5", "4.5 - 5.5", "5.5 - 6.5", "6.5 - 7",  "7 - 10"],
       node_colors = ["rgba(215, 47, 47, 1)", "rgba(215, 136, 47, 1)", "rgba(215, 209, 47, 1)", "rgba(150, 215, 47, 1)", "rgba(47, 215, 84, 1)"],
       path_colors = ["rgba(215, 47, 47, 0.5)", "rgba(215, 136, 47, 0.5)", "rgba(215, 209, 47, 0.5)", "rgba(150, 215, 47, 0.5)", "rgba(47, 215, 84, 0.5)"],
       subject=subject_sankey)

    return sankey_chart

@app.callback(
    Output('output-container', 'children'),
    Input('exchange-submit', 'n_clicks'),
    State('grade-input-state', 'value'),
    State('pre-year-drop', 'value'),
    State('fol-year-drop', 'value'),
    State('subject-input-state', 'value'))

def exchange_grade(n_clicks, grade, pre_year, fol_year, subject_combination):
    sub_com = [f'{subject_combination}']

    exchange_grade = exchange(grade, pre_year, fol_year, sub_com)

    return u'Your grade is equavalent to the grade in rang {} in {}'.format(exchange_grade,fol_year)

@app.callback(
    Output('exchange-grade-graph', 'figure'),
    Input('year-checklist', 'value'))
def update_line(year_list):
    df = pd.read_csv(f'ds/data/Dash Board/Year/exchange-grade-{min(year_list)}-{max(year_list)}.csv')
    fig = px.line(df, x='Major ID', y='Grade', color='Type', title="Hanoi University of Science & Technology (HUST) - Standard Passing Grades".upper())

    return fig

########################################################################################################################
app.layout = html.Div(children=[
    html.Div(
        id="big-app-container",
        children=[
            build_banner(),
            html.Div(
                id="app-container",
                children=[
                    build_tabs(),
                    # Main app
                    html.Div(id="app-content"),
                ],
            ),

        ], style={'background-color': '#eef3f3'})
])


@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_tab_1()
    elif tab_switch == "tab2":
        return build_tab_2()
    elif tab_switch == "tab3":
        return build_tab_3()
    else:
        return build_tab_4()


if __name__ == '__main__':
    app.run_server(debug=True)
