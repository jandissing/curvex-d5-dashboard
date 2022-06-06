import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dash import dcc, html

def plot_figure(df):
    fig = go.Figure()
    delta = go.Scatter(x=df.index, y=df['Delta'], name='Delta', line_shape='spline')
    fig.add_trace(delta)
    theta = go.Scatter(x=df.index, y=df['Theta'], name='Theta', line_shape='spline')
    fig.add_trace(theta)
    low_alpha = go.Scatter(x=df.index, y=df['Low Alpha'], name='Low Alpha', line_shape='spline')
    fig.add_trace(low_alpha)
    high_alpha = go.Scatter(x=df.index, y=df['High Alpha'], name='High Alpha', line_shape='spline')
    fig.add_trace(high_alpha)
    low_beta = go.Scatter(x=df.index, y=df['Low Beta'], name='Low Beta', line_shape='spline')
    fig.add_trace(low_beta)
    high_beta = go.Scatter(x=df.index, y=df['High Beta'], name='High Beta', line_shape='spline')
    fig.add_trace(high_beta)
    low_gamma = go.Scatter(x=df.index, y=df['Low Gamma'], name='Low Gamma', line_shape='spline')
    fig.add_trace(low_gamma)
    middle_gamma = go.Scatter(x=df.index, y=df['Middle Gamma'], name='Middle Gamma', line_shape='spline')
    fig.add_trace(middle_gamma)

    fig.update_layout(
        xaxis=dict(
            title='Time in Seconds',
            autorange=False,
            range=[0, 20],
            rangeslider=dict(
                autorange=True,
                range=[0, 20],
                visible=True,
            ),
            type="-",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        legend=dict(
            
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    
    return fig

def plot_figure2(df1):
    df = df1[['Delta', 'Theta', 'Low Alpha', 'High Alpha', 'Low Beta', 'High Beta',
       'Low Gamma', 'Middle Gamma']].mean().reset_index()
    df.columns = ['index', 'Average']
    fig = px.histogram(df, y='Average', x='index', color='index', labels={"index": "Wave", "Average": "Average"})
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        yaxis_title='',
        xaxis_title=None,
        legend_title=None,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of ", "")))
    fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of ", "")))
    return fig

def plot_figure3(df1):
    df = df1[['Cognitive Load', 'Flow', 'Focus', 'Stress']].mean().reset_index()
    df.columns = ['index', 'Average']
    fig = px.histogram(df, y='Average', x='index', color='index', labels={"index": "Metric", "Average": "Average"})
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        yaxis_title='',
        xaxis_title=None,
        legend_title=None,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of ", "")))
    fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of ", "")))
    return fig

def plot_figure4(df):
    fig = go.Figure()
    cogload = go.Scatter(x=df.index, y=df['Cognitive Load'], name='Cognitive Load', line_shape='spline')
    fig.add_trace(cogload)
    flow = go.Scatter(x=df.index, y=df['Flow'], name='Flow', line_shape='spline')
    fig.add_trace(flow)
    focus = go.Scatter(x=df.index, y=df['Focus'], name='Focus', line_shape='spline')
    fig.add_trace(focus)
    stress = go.Scatter(x=df.index, y=df['Stress'], name='Stress', line_shape='spline')
    fig.add_trace(stress)
    fig.update_layout(
        xaxis=dict(
            title='Time in Seconds',
            autorange=False,
            range=[0, 20],
            rangeslider=dict(
                autorange=True,
                range=[0, 20],
                visible=True,
            ),
            type="-",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        legend=dict(
            
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    
    return fig

def plot_figure5(df1):
    df = df1[['Cognitive Load', 'Flow', 'Focus', 'Stress']].mean().reset_index()
    df.columns = ['index', 'Average']
    fig = px.pie(df, values='Average', names='index', color='index', labels={"index": "Metric", "Average": "Average"})
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        yaxis_title='',
        xaxis_title=None,
        legend_title=None,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of ", "")))
    fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of ", "")))
    return fig

def recommend(df1):
    df = df1[['Cognitive Load', 'Flow', 'Focus', 'Stress']].mean().reset_index()
    df.columns = ['Metric', 'Average']
    df['Percentage'] = df['Average']/df['Average'].sum()
    best_metric = df.loc[(df['Percentage'] == df.Percentage.max())].reset_index()['Metric'][0]
    best_metric_value = round((df.Percentage.max())*100, 2)
    phrase1 = f"Your {best_metric} levels represented {best_metric_value}% of the metrics of your Task. "
    if df.loc[(df['Metric'] == 'Stress')].reset_index()['Percentage'][0] > 0.1:
        phrase2 = f"Based on your data, the stress level was a bit high for this Task... This may be a good time to take a break."
        img = html.Img(src='../user_interface/assets/break.png', style={'width': '35%', 'height': '35%'})
    else: 
        phrase2 = f" \nBased on your data, we recommend you to keep up the good work!!!"
        img = html.Img(src='../user_interface/assets/break.png', style={'width': '35%', 'height': '35%'})
        
    return {'phrase1': phrase1,  'phrase2': phrase2, 'img': img}




list_of_keys = ['Delta','Theta','Low Alpha','High Alpha','Low Beta','High Beta','Low Gamma','Middle Gamma']
list_of_keys_2 = ['Cognitive Load', 'Flow', 'Focus', 'Stress']

def plot_figure11(eeg_data):
    print("OBA")
    fig = go.Figure()
    for key in list_of_keys:
        fig.add_trace(go.Scatter(x=np.arange(len(eeg_data)), y=[item[key] for item in eeg_data], name=key, line_shape='spline'))
    fig.update_layout(
        xaxis=dict(
            title='Time in Seconds',
            autorange=False,
            range=[0, 20],
            rangeslider=dict(
                autorange=True,
                range=[0, 20],
                visible=True,
            ),
            type="-",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        legend=dict(
            
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    
    return fig.to_json()

def plot_figure44(eeg_data):
    fig = go.Figure()
    for key in list_of_keys_2:
        fig.add_trace(go.Scatter(x=np.arange(len(eeg_data)), y=[item[key] for item in eeg_data], name=key, line_shape='spline'))
    fig.update_layout(
        xaxis=dict(
            title='Time in Seconds',
            autorange=False,
            range=[0, 20],
            rangeslider=dict(
                autorange=True,
                range=[0, 20],
                visible=True,
            ),
            type="-",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        legend=dict(
            
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    
    return fig.to_json()

def plot_figure22(eeg_data):
    meandict = {key: sum(row[key] for row in eeg_data) / len(eeg_data) for key in list_of_keys}
    fig = px.histogram(y=meandict.values(), x=meandict.keys(), color=meandict.keys())
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        yaxis_title='',
        xaxis_title=None,
        legend_title=None,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    fig.update_traces(hovertemplate="Wave: %{x}<br>Average: %{y}<extra></extra>")
    fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of ", "")))
    fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of ", "")))
    return fig.to_json()


def plot_figure33(eeg_data):
    meandict = {key: sum(row[key] for row in eeg_data) / len(eeg_data) for key in list_of_keys_2}
    fig = px.histogram(y=meandict.values(), x=meandict.keys(), color=meandict.keys())
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(color = "white", size=17),
        yaxis_title='',
        xaxis_title=None,
        legend_title=None,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="center",
        x=0.5,
    ))
    fig.update_traces(hovertemplate="Metric: %{x}<br>Average: %{y}<extra></extra>")
    fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of ", "")))
    fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of ", "")))
    return fig.to_json()