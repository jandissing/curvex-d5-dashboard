import dash
from dash.dependencies import Input, Output
from dash import dcc, html
from .functions import *
import flask
import pandas as pd
import os
# import urllib.parse
import dash_daq as daq
from domain.eeg_app_aggregate.repository_eeg import EEGRepo
# from domain.profile_aggregate.repository_profile import ProfileRepo
import requests
import json


def create_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get('secret_key', 'secret')

    assets_path = os.getcwd() +'/user_interface/assets/'
    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix, assets_folder=assets_path)
    app._favicon = ("favicon.png")

    app.scripts.config.serve_locally = False

    light_theme = {
        "main-background": "purple",
    }

    dark_theme = {
        "main-background": "black",
    }

    app.layout = html.Div([
        html.Div([
        dcc.Store(id='memory-output'),
        html.H4('Group208-INT', style={'text-align': 'center'}),
        daq.BooleanSwitch(on=False, id="bool-switch-input"),
        html.Div(id="bool-switch-output"),
        # html.H4('User: '),
        # html.H2(id="tabs-example-graph2"),
        dcc.Location(id='url', refresh=False),
        html.A(html.H5('Switch Profile'), href='/newsession/', id="switch-profile-button"),
        html.H1(id='username'),],
        className='top_div'),
        html.Div([
            html.A(id="start_new_session"),
        ], className="new_session_div"),
        
    dcc.Tabs(id="tabs-example-graph2", style={'display': 'None'})],
        className='container',
        id='container',
        style={ "backgroundColor": light_theme["main-background"]})


    @app.callback(
        [Output("container", "style"),],
        Input("bool-switch-input", "on"),
    )
    def update_output(on):
        theme = dark_theme if on else light_theme

        return (
            {"backgroundColor": theme["main-background"]},
        )
    # Update the index startnewsession-button
    @app.callback(dash.dependencies.Output('username', 'children'),
                [dash.dependencies.Input('url', 'pathname')],
                [dash.dependencies.Input('url', 'href')])
    def display_page(pathname, href):
        try:
            base_url = href.split("/")[0] + "//" + href.split("/")[2] + "/"
            profile_id = pathname.split("/")[2]
            profile_name = EEGRepo.fetch_eeg_by_id(profile_id)['profilename']
            return profile_name
        except:
            return " "

    @app.callback(dash.dependencies.Output('switch-profile-button', 'href'),
                [dash.dependencies.Input('url', 'pathname')],
                [dash.dependencies.Input('url', 'href')])
    def display_page(pathname, href):
        try:
            base_url = href.split("/")[0] + "//" + href.split("/")[2] + "/"
            profile_id = pathname.split("/")[2]
            customer_id = EEGRepo.get_customer_id_by_profile_id(profile_id)
            return "http://group208-choose-profile.azurewebsites.net/selectprofile/" + customer_id
        except:
            return "#"

    @app.callback(dash.dependencies.Output('start_new_session', 'children'),
                [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        try:
            profile_id = pathname.split("/")[2]
            print(profile_id)
            url = f"/newsession/{profile_id}"
            print(url)
            content = html.A(html.Button(f"Start new session", id="start_new_session"), href=url)
            print(content)
            return content
        except:
            return "/Error"

    @app.callback(Output('memory-output', 'data'),
                [dash.dependencies.Input('url', 'pathname')],
                [dash.dependencies.Input('url', 'href')])
    def filter_user(pathname, href):
        base_url = href.split("/")[0] + "//" + href.split("/")[2] + "/"
        profile_id = pathname.split("/")[2]
        eeg_data =  EEGRepo.fetch_eeg_by_id(profile_id)['values']
        # eeg_data = json.loads(requests.get(base_url + 'eegdata/' +user_name).text)['values']
        df_all_sessions = pd.DataFrame()
        for i in range(len(eeg_data)):
            print(i)
            df = pd.DataFrame(eeg_data[i]['eeg_data_info']['eeg_data_values'])
            df['Session'] = "Session " + str(i+1)
            df_all_sessions = pd.concat([df_all_sessions, df], axis=0)

        return df_all_sessions.to_dict('records')
    

    @app.callback(Output('memory-tab-output', 'data'),
                Input('memory-output', 'data'),
                Input("tabs-example-graph", 'value')
                )
    def on_data_set_graph_store(data, tab_selected):
        df = pd.DataFrame.from_records(data)
        if tab_selected.split(' ')[0] == 'Task':
            filtered = df.loc[(df['Tasks start and end time'] == tab_selected)]
        else:
            filtered = df.loc[(df['Session'] == tab_selected)]

        return filtered.to_dict('records')

    
    
    @app.callback(Output("tabs-example-graph2", 'children'),
                 Input('memory-output', 'data'))
    def update_graph(data):
        if data is None:
            return html.Div([html.Div([html.H3('There is no data for this profile yet', style={'textAlign': 'center', 'fontSize': '2rem', })])
                ,
                ], className='messagediv')
        else:
            print("Hello_ there is data")
            df = pd.DataFrame.from_records(data)
            sessions = df['Session'].unique()
            children_list = [dcc.Tab(label=session, id=session ,value=session) for session in sessions]
            first_children_value = sessions[0]
            return html.Div([
                    dcc.Store(id='memory-tab-output'),
                    dcc.Tabs(id="tabs-example-graph", value=first_children_value, children=children_list, style={'width': '65vw', 'position':'absolute', 'left':'35vw', 'top':'0px', 'max-height': '50px'}),
                    html.Div(id='tabs-content-example-graph'),
                    html.Div(id='tabs-content-example-graph2'),
                ]) 


    @app.callback(
        Output('tabs-content-example-graph', 'children'),
        Input('memory-tab-output', 'data')
    )
    def on_data_set_graph(data):
        df = pd.DataFrame.from_records(data)
        fig1 = plot_figure(df)

        fig2 = plot_figure2(df)

        try:
            fig3 = plot_figure3(df)
            fig4 = plot_figure4(df)
            fig5 = plot_figure5(df)
            
            recommendation = recommend(df)
            # print("problem here")
            return html.Div([
            html.Div([dcc.Graph(figure=fig1, style={'width': '100%'})]),
            html.Div([dcc.Graph(figure=fig2, style={'width': '100%'})]),
            html.Div([dcc.Graph(figure=fig3, style={'width': '100%'})]),
            html.Div([dcc.Graph(figure=fig4, style={'width': '100%'})]),
            html.Div([dcc.Graph(figure=fig5, style={'width': '100%'})]),
            html.Div([
                html.H5(id='text-output'),
                html.H2(recommendation['phrase1'], style={'width': '100%', 'font-weight': 'normal', 'text-align': 'center'}),
                recommendation['img'],
                html.H3(recommendation['phrase2'], style={'width': '100%', 'font-weight': 'normal', 'text-align': 'center'})
                ],
                style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center', 'margin': 'auto', 'width': '100%', 'padding-left': '14%', 'padding-right': '14%'})
            ], style={'display': 'grid', 'justify-content': 'center', 'align-items':'center', 'grid-template-columns': '1fr 1fr', 'width': '96%', 'margin-left': 'auto', 'margin-right': 'auto', 'column-height': '450px'})
        except:
            return html.Div([
            dcc.Graph(figure=fig1, style={'grid-column': '1/3', 'width': '100%'}),
            dcc.Graph(figure=fig2, style={'grid-column': '1/3', 'width': '100%'}),
            # html.H2(str(data), style={'color': 'white'})
            ], style={'display': 'grid', 'justify-content': 'center', 'grid-template-columns': '1fr 1fr', 'width': '96%', 'margin-left': 'auto', 'margin-right': 'auto'})

    return app