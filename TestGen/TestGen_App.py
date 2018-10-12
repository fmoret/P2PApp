# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 11:00:33 2018

@author: Thomas
"""


#import dash 
from app import app

from dash.dependencies import Event, Output, Input, State
import dash_core_components as dcc
import dash_html_components as html

from .TestGenTab import TestGenTab
TestGen = TestGenTab()

#import datetime
#import json
#import pandas_datareader.data as web
#import plotly
#import random
#import time
#import plotly.graph_objs as go
#from collections import deque
#from loremipsum import get_sentences

def TestGenApp_Show(tab_id='Generator'):
    return [html.Div([
                html.Div([
                        html.Div(['Test Case Generator'],
                                 style={'display':'table-cell','width':'70%','font-size':'2em'}),
                        html.Div([html.A('Back to main app', href='/', style={'color':'#003366','font-style':'italic'})],
                                  style={'display':'table-cell','width':'30%','text-align':'right','vertical-align':'top'})
                        ],style={'display':'table-row'}),
            ],id='gen-title',style={'display':'table','width':'100%'}),
            html.Div([
                html.Hr()
                ],style={'width':'95%','padding-bottom':'1em','margin':'auto'}),
            dcc.Tabs(id="gen-tabs", value=tab_id, style={'display':'none'},
                     children=[
                             dcc.Tab(label='Generator', value='Generator'),
                             ]
                     ),
            html.Div(id='gen-tab-output')
            ]

layout = html.Div(TestGenApp_Show(), 
        id='TestGen-container',
        style={
            'width': '98%',
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
            'margin-right': 'auto'
        }
    )

#%% Callbacks
#%% General Tab layout
@app.callback(Output('gen-tab-output', 'children'), [Input('gen-tabs', 'value')])
def voidfct_Tabs(tab_id):
    if tab_id=='Generator':
        return TestGen.ShowTab()
    else:
        return []

#%% General Menu
def generate_callbacks(tags,generic=False):
    if generic:
        for tag in tags:
            if tag['controlable']:
                app.callback(Output(f'gen-params-Price-min-{tag["var"]}-sel','children'), [Input(f'gen-params-Price-min-{tag["var"]}', 'value')
                        ])(TestGen.GenericFctParams('Price_min',tag["var"]))
                app.callback(Output(f'gen-params-Price-max-{tag["var"]}-sel','children'), [Input(f'gen-params-Price-max-{tag["var"]}', 'value')
                        ])(TestGen.GenericFctParams('Price_max',tag["var"]))
                if tag['type']=='consumption':
                    app.callback(Output(f'gen-params-Power-min-{tag["var"]}-sel','children'), [Input(f'gen-params-Power-min-{tag["var"]}', 'value')
                            ])(TestGen.GenericFctParams('Power_min',tag["var"]))
                    app.callback(Output(f'gen-params-Power-max-{tag["var"]}-sel','children'), [Input(f'gen-params-Power-max-{tag["var"]}', 'value')
                            ])(TestGen.GenericFctParams('Power_max',tag["var"]))
                    if tag['solar']:
                        app.callback(Output(f'gen-params-solar-{tag["var"]}-sel','children'), [Input(f'gen-params-solar-{tag["var"]}', 'value')
                                ])(TestGen.GenericFctParams('Solar_Installed',tag["var"]))
                        app.callback(Output(f'gen-general-{tag["var"]}-solar-sel','children'), [Input(f'gen-general-{tag["var"]}-solar', 'value')
                                ])(TestGen.GenericFctSolar(tag["var"]))
            app.callback(Output(f'gen-general-{tag["var"]}-sel','children'), [Input(f'gen-general-{tag["var"]}', 'value')
                    ])(TestGen.GenericFct(tag["var"]))
    else:
        for tag in tags:
            app.callback(Output(f'gen-general-{tag}-sel','children'), [Input(f'gen-general-{tag}', 'value')])(getattr(TestGen,tag))


generate_callbacks(TestGen.Tags)
generate_callbacks(TestGen.GenericTags,True)


# Nsame -- show
app.callback(Output('gen-general-Same-show','children'), [Input('gen-general-Same-refresh', 'n_clicks')])(TestGen.SameShowRefresh)
# Nsame -- refresh
app.callback(Output('gen-general-Same-row','style'), [Input('gen-general-Same-hide', 'n_clicks')])(TestGen.SameShowHide)
# Params -- refresh
app.callback(Output('gen-params-refresh','children'), [Input('gen-params-default', 'n_clicks')])(TestGen.ParamsMenuDefault)
# General -- refresh
app.callback(Output('gen-general-refresh','children'), [Input('gen-general-default', 'n_clicks')])(TestGen.GeneralMenuDefault)

# Generate -- launch
app.callback(Output('gen-launch-button-sel','children'), [Input('gen-launch-button', 'n_clicks')])(TestGen.GenerateLaunch)
# Generate -- trigger
app.callback(Output('gen-generator-output','children'), [Input('gen-generator-trigger', 'n_clicks')])(TestGen.Generate)

