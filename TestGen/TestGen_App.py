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
layout = html.Div(TestGen.ShowApp(), 
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
app.callback(Output('gen-tab-output', 'children'), [Input('gen-tabs', 'value')])(TestGen.ShowTab)

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
                    app.callback(Output(f'gen-general-{tag["var"]}-click-sel','children'), [Input(f'gen-general-{tag["var"]}-click', 'n_clicks')
                            ])(TestGen.GenericMenuSolar(tag["var"]))
            app.callback(Output(f'gen-general-{tag["var"]}-sel','children'), [Input(f'gen-general-{tag["var"]}', 'value')
                    ])(TestGen.GenericFct(tag["var"]))
    else:
        for tag in tags:
            app.callback(Output(f'gen-general-{tag}-sel','children'), [Input(f'gen-general-{tag}', 'value')])(getattr(TestGen,tag))


generate_callbacks(TestGen.Tags)
generate_callbacks(TestGen.ItemTags,True)


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

# Generate -- file system
app.callback(Output('gen-generator-file-system-sel','children'), [Input('gen-generator-file-system', 'value')])(TestGen.FileSystem)
# Generate -- file name
app.callback(Output('gen-generator-file-name-sel','children'), [Input('gen-generator-file-name', 'value')])(TestGen.FileName)

