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
        for element in tags:
            app.callback(Output(f'gen-general-{element}-sel','children'), [Input(f'gen-general-{element}', 'value')])(TestGen.GenericFct(element))
    else:
        for element in tags:
            app.callback(Output(f'gen-general-{element}-sel','children'), [Input(f'gen-general-{element}', 'value')])(getattr(TestGen,element))

generate_callbacks(TestGen.Tags)
generate_callbacks(TestGen.GenericTags,True)








## Number of cases
##app.callback(Output('gen-general-Ngen-sel', 'children'), [Input('gen-general-Ngen', 'value')])(getattr(TestGen,'Ngen'))
#
## Composition of test cases identical?
#@app.callback(Output('gen-general-Same-sel', 'children'), [Input('gen-general-Same', 'value')])
#def voidfct_GeneralMenu_Same(same):
#    return TestGen.Same(same)
#
## Production coverage
#@app.callback(Output('gen-general-Coverage-sel', 'children'), [Input('gen-general-Coverage', 'value')])
#def voidfct_Coverage(coverage):
#    return TestGen.Coverage(coverage)
#
## Wind share
#@app.callback(Output('gen-general-Wind-sel', 'children'), [Input('gen-general-Wind', 'value')])
#def voidfct_Wind(wind):
#    return TestGen.Wind(wind)
#
## Number of houses
#@app.callback(Output('gen-general-Nhouses-sel', 'children'), [Input('gen-general-Nhouses', 'value')])
#def voidfct_Nhouses(Nhouses):
#    return TestGen.Nhouses(Nhouses)
#
#
#TestGen_tags = ['Ngen','Same','Coverage','Wind','Nhouses']
#for element in tags:
#    app.callback(Output('gen-general-'+element+'-sel','children'), [Input(f'gen-general-'+element, 'value')])(getattr(TestGen,element))