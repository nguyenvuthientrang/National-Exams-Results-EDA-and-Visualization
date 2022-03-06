import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from plotly.subplots import make_subplots



########################################################################################################################

def score_dist(df, subjects, graph, view="seperate", shade=False, smooth=True, sample_size=1000):
    assert view == "together" or view == "seperate" or view == "correlogram"

    colors = {"Math": "#45a39b", "Literature": "#a0a345", "English": "#77a345", "Physics": "#4577a3",
              "Chemistry": "#5145a3", "Biology": "#8845a3", "Geography": "#a34845", "History": "#a36a45",
              "Civic Education": "#a3456a"}
    assert graph == "line" or graph == "bar" or graph == "line-bar"
    if graph == "line":
        kde = True
        hist = False
    elif graph == "bar":
        kde = False
        hist = True
    else:
        kde = True
        hist = True

    all_subjects = {"Math", "Literature", "English", "Physics", "Chemistry", "Biology", "Geography", "History",
                    "Civic Education"}
    assert set(subjects) <= all_subjects

    bandwidth = {"Math": 0.2, "Literature": 0.25, "English": 0.2, "Physics": 0.25, "Chemistry": 0.25, "Biology": 0.25,
                 "Geography": 0.25, "History": 0.25, "Civic Education": 0.25}

    if smooth == True:
        bw = 2
    else:
        bw = 1

    labels = []
    if view == "together":
        fig = ff.create_distplot([list(df[sub]) for sub in subjects], subjects,
                                 colors=[colors[sub] for sub in subjects],
                                 bin_size=[bandwidth[sub] for sub in subjects], show_curve=kde, show_hist=hist)
        fig.update_layout(width=500)
        fig.update_layout(height=400)
    elif view == "seperate":
        fig = make_subplots(
            rows=3, cols=3)
        i = 0
        for subject in subjects:
            f = ff.create_distplot([df[subject]], [subject], colors=[colors[subject]], bin_size=[bandwidth[subject]],
                                   show_curve=kde, show_hist=hist)
            fig.add_trace(go.Histogram(f['data'][0]), row=i // 3 + 1, col=i % 3 + 1)
            fig.add_trace(go.Scatter(f['data'][1]), row=i // 3 + 1, col=i % 3 + 1)
            i += 1
        fig.update_layout(width=600)
        fig.update_layout(height=400)

    else:
        fig = make_subplots(
            rows=len(subjects), cols=len(subjects))
        for i in range(1, len(subjects) + 1):
            f = ff.create_distplot([df[subjects[i - 1]]], [subjects[i - 1]], colors=[colors[subjects[i - 1]]],
                                   bin_size=[bandwidth[subjects[i - 1]]], show_curve=True, show_hist=True)
            fig.add_trace(go.Histogram(f['data'][0]), row=i, col=i)
            fig.add_trace(go.Scatter(f['data'][1]), row=i, col=i)
        if len(subjects) > 1:
            for i in range(2, len(subjects) + 1):
                fig.update_yaxes(title_text="<b>"+subjects[i - 1], row=i, col=1)
                fig.update_xaxes(title_text="<b>"+subjects[i - 1], row=len(subjects), col=i)
                for j in range(1, i):
                    fig.add_trace(go.Histogram2dContour(
                        x=df[subjects[j - 1]],
                        y=df[subjects[i - 1]],
                        colorscale=[(0, "#ffffff"), (1, colors[subjects[j - 1]])],
                        line_width=0,
                        showscale=False,
                        histnorm='probability density'),
                        row=i, col=j)
        fig.update_layout(width=700)
        fig.update_layout(height=700)
        fig.update_yaxes(title_text="<b>"+subjects[0], row=1, col=1)
        fig.update_xaxes(title_text="<b>"+subjects[0], row=len(subjects), col=1)
    fig.update_layout(plot_bgcolor='#ffffff', )
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(showticklabels=False)
    return fig

########################################################################################################################