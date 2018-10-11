# -*- coding: utf-8 -*-
"""
    Main file of P2PMarket_App application for consumer-centric markets
"""

#import dash 
from app import app

from dash.dependencies import Event, Output, Input, State
import dash_core_components as dcc
import dash_html_components as html

from .SimulationTab import SimulationTab
from .MarketTab import MarketTab
SimTab = SimulationTab()
MarketTab = MarketTab()

#import datetime
#import json
#import pandas_datareader.data as web
#import plotly
#import random
#import time
#import plotly.graph_objs as go
#from collections import deque
#from loremipsum import get_sentences

def MainApp_Show(tab_id='Market'):
    return [html.Div([
                html.Div([
                        html.Div(['Prosumer Centric Market Simulation'],
                                 style={'display':'table-cell','width':'70%','font-size':'2em'}),
                        html.Div([html.A('Go to test case generator', href='/generator', style={'color':'#003366','font-style':'italic'})],
                                  style={'display':'table-cell','width':'30%','text-align':'right','vertical-align':'top'})
                        ],style={'display':'table-row'})
            ],id='main-title',style={'display':'table','width':'100%'}),
            html.Div([
                #html.Hr()
                ],style={'width':'95%','padding-bottom':'1em','margin':'auto'}),
            dcc.Tabs(id="tabs", value=tab_id, style={'display':'block'},
                     children=[
                             dcc.Tab(label='Market', value='Market'),
                             dcc.Tab(label='Simulation', value='Simulation'),
                             ]
                     ),
            html.Div(id='tab-output'),
            ]

layout = html.Div(MainApp_Show(), 
        id='MainApp-container',
        style={
            'width': '98%',
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
            'margin-right': 'auto'
        }
    )


#%% Callbacks
#%% General Tab layout
@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def voidfct_Tabs(tab_id):
    if tab_id=='Market':
#        MarketTab.MGraph = SimTab.MGraph
        MarketTab.Optimizer = SimTab.Optimizer
        return MarketTab.ShowTab()
    elif tab_id=='Simulation':
        SimTab.MGraph = MarketTab.MGraph
        SimTab.Optimizer = MarketTab.Optimizer
        return SimTab.ShowTab()
    else:
        return []

@app.callback(Output('market-graph-graph', 'children'),events=[Event('market-graph-interval', 'interval')])
def voidfct_IntervalGraphUpdate():
    return MarketTab.MGraph.BuildGraphOfMarketGraph()


#%% Market tab
# Action's options
app.callback(Output('market-topmenu-second', 'children'),[Input('market-topmenu-insert','value')
            ])(MarketTab.TopMenu_Insert)

# Action's options - number
app.callback(Output('market-topmenu-third', 'children'),[Input('market-topmenu-second-drop','value')],[
        State('market-topmenu-insert', 'value')
            ])(MarketTab.TopMenu_Number)

# Detect click on button 'Add'/'Select'
app.callback(Output('market-menu', 'children'),[Input('add-button', 'n_clicks')],
              [State('market-topmenu-insert', 'value'),
               State('market-topmenu-second-drop', 'value'),
               State('market-topmenu-third-number', 'value')
               ])(MarketTab.Menu)

# Detect click on buttons Refresh
app.callback(Output('market-menu-agent-refresh', 'children'),[Input('agent-refresh-button', 'n_clicks')
            ])(MarketTab.Menu_AgentRefresh)

# Change in agent type
app.callback(Output('market-menu-agent-data', 'children'),[Input('market-menu-agent-type', 'value')
            ])(MarketTab.AgentType)

# Change in agent data (name, number of assets)
app.callback(Output('market-menu-assets', 'children'),[
            Input('market-menu-agent-name', 'value'),
            Input('market-menu-agent-number-assets', 'value')
            ])(MarketTab.AgentChange)

# Change in agent data (community goal, importation fee)
app.callback(Output('market-menu-agent-impfee-show', 'style'),[
            Input('market-menu-agent-commgoal', 'value'),
            Input('market-menu-agent-impfee', 'value')
            ])(MarketTab.AgentChangeCommGoal)

# Change in agent partnerships
app.callback(Output('market-menu-agent-preferences', 'value'),[Input('market-menu-agent-partners', 'value')],[
            State('market-menu-agent-preferences', 'value')
            ])(MarketTab.AgentPartners)

# Change in agent preferences
app.callback(Output('market-menu-agent-preferences-void', 'value'),[Input('market-menu-agent-preferences', 'value')
            ])(MarketTab.AgentPreferences)

# Change in agent community
app.callback(Output('market-menu-agent-commpref', 'value'),[Input('market-menu-agent-community', 'value')],[
            State('market-menu-agent-commpref', 'value')
            ])(MarketTab.AgentCommunity)

# Change in agent community preference
app.callback(Output('market-menu-agent-commpref-void', 'value'),[Input('market-menu-agent-commpref', 'value')
            ])(MarketTab.AgentCommPref)

# Assets Tabs
app.callback(Output('tab-assets-output', 'children'), [Input('tab-assets', 'value')
            ])(MarketTab.ShowAssetMenu)

# Change in asset data (name, type, costfct, costfct_coeff, p_bounds_up, p_bounds_low, ...)
app.callback(Output('market-menu-asset-void', 'value'),[
            Input('market-menu-asset-name', 'value'),
            Input('market-menu-asset-type', 'value'),
            Input('market-menu-asset-costfct', 'value'),
            Input('market-menu-asset-costfct_coeff', 'value'),
            Input('market-menu-asset-p_bounds_up', 'value'),
            Input('market-menu-asset-p_bounds_low', 'value'),
            ])(MarketTab.AssetChange)

# Detect click on buttons Refresh
app.callback(Output('market-menu-community-refresh', 'children'),[Input('community-refresh-button', 'n_clicks')
            ])(MarketTab.Menu_CommunityRefresh)

# Change in community data 
app.callback(Output('market-menu-community-members-void', 'value'),[
            Input('market-menu-community-name', 'value'),
            Input('market-menu-community-commgoal', 'value'),
            Input('market-menu-community-members', 'value')
            ])(MarketTab.CommunityChange)

# Change in community partnerships
app.callback(Output('market-menu-community-preferences', 'value'),[Input('market-menu-community-partners', 'value')],[
            State('market-menu-community-preferences', 'value')
            ])(MarketTab.AgentPartners)

# Change in community preferences
app.callback(Output('market-menu-community-preferences-void', 'value'),[Input('market-menu-community-preferences', 'value')
            ])(MarketTab.AgentPreferences)

# Show the possible types of suppression
app.callback(Output('market-menu-delete-type', 'children'),[Input('market-menu-delete-select', 'value')
            ])(MarketTab.Menu_DeleteType)

# Last warning before suppression of agent, community manager or entire community
app.callback(Output('market-menu-delete-assets', 'children'),[Input('market-menu-delete-select-type', 'value')
            ])(MarketTab.Menu_DeleteAssets)

# Last warning before suppression of assets
app.callback(Output('market-menu-delete-message', 'children'),[Input('market-menu-delete-select-asset', 'value')],[
            State('market-menu-delete-select-type', 'value')
            ])(MarketTab.Menu_DeleteWarning)

# Suppression after confirmation
app.callback(Output('market-menu-delete-refresh','children'),[
            Input('market-menu-delete-cancel-button', 'n_clicks'),
            Input('market-menu-delete-confirm-button', 'n_clicks')
            ],[
            State('market-menu-delete-select-type', 'value'),
            State('market-menu-delete-select-asset', 'value')
            ])(MarketTab.Menu_DeleteConfirmed)

# Show confirm buttons
@app.callback(Output('market-menu-delete-confirm-buttons', 'style'),[Input('market-menu-delete-show-confirm-button', 'n_clicks')],[
        State('market-menu-delete-show-confirm-button', 'children')])
def voidfct_DeleteShowConfirmed(n_clicks,show_disp):
    return MarketTab.Menu_DeleteShowConfirmed(show_disp)

# Save button
app.callback(Output('market-menu-save-message', 'children'),[Input('market-menu-save-button', 'n_clicks')],[
            State('market-menu-saveas-filename', 'value')
            ])(MarketTab.Menu_SaveGraph)

# Save button message
@app.callback(Output('market-menu-save-refresh', 'children'),[Input('market-menu-save-button-message', 'n_clicks')],[
        State('market-menu-save-button-message', 'children')])
def voidfct_SaveGraphMessage(n_clicks,message):
    return [message]

# Add file save button
app.callback(Output('market-menu-addfile-select', 'children'),[Input('market-menu-addfile-extension', 'value')],[
            State('market-topmenu-insert', 'value'),
            State('market-topmenu-second-drop', 'value')
            ])(MarketTab.Menu_AddFileSelect)

# Add file connectivity type
app.callback(Output('market-menu-addfile-prefs', 'children'),[Input('market-menu-addfile-connect-matrix', 'value')
            ])(MarketTab.Menu_AddFilePrefs)

# Add file save button
app.callback(Output('market-menu-addfile-message', 'children'),[Input('market-menu-addfile-button', 'n_clicks')],[
            State('market-menu-addfile-filename', 'value'),
            State('market-menu-addfile-extension', 'value'),
            State('market-menu-addfile-type', 'value'),
            State('market-menu-addfile-connect-matrix', 'value'),
            State('market-menu-addfile-pref-filename', 'value'),
            State('market-menu-addfile-pref-ceil', 'value')
            ])(MarketTab.Menu_AddFileMessage)

# Add file save button message
@app.callback(Output('market-menu-addfile-refresh', 'children'),[Input('market-menu-addfile-button-message', 'n_clicks')],[
        State('market-menu-addfile-button-message', 'children')])
def voidfct_AddFileMessageOut(n_clicks,message):
    return [message]

# Link menu -- who
app.callback(Output('market-menu-link', 'children'),[Input('market-menu-link-type', 'value')
            ])(MarketTab.Menu_LinkWho)

# Link menu -- with
app.callback(Output('market-menu-link2', 'children'),[Input('market-menu-link-who', 'value')],[
            State('market-menu-link-type', 'value'),
            State('market-menu-link-type', 'className')
            ])(MarketTab.Menu_LinkWith)

# Link menu -- prefs
@app.callback(Output('market-menu-link-prefs', 'children'),[Input('market-menu-link-with', 'value')],[
        State('market-menu-link-who', 'value'),
        State('market-menu-link-type', 'value'),
        State('market-menu-link-type', 'className')])
def voidfct_LinkPrefs(who2,who1,link_type,add_value):
    return MarketTab.Menu_LinkPrefs(who1,who2,link_type,add_value)

# Link menu -- update
app.callback(Output('market-menu-link-refresh-trigger', 'children'),[Input('market-menu-link-confirm-button', 'n_clicks')],[
            State('market-menu-link-who', 'value'),
            State('market-menu-link-with', 'value'),
            State('market-menu-link-pref1', 'value'),
            State('market-menu-link-pref2', 'value'),
            State('market-menu-link-type', 'value'),
            State('market-menu-link-type', 'className')
            ])(MarketTab.Menu_LinkConfirmed)

# Link menu -- refresh
@app.callback(Output('market-menu-link-refresh', 'children'),[Input('market-menu-link-refresh-button', 'n_clicks')])
def voidfct_LinkRefresh(n_clicks):
    return MarketTab.Menu_LinkRefresh()


#%% Simulation tab

# External menu
app.callback(Output('simulation-menu-external', 'children'),[Input('simulation-menu-location', 'value'),
            Input('simulation-menu-target', 'value')
            ])(SimTab.MenuComputation_External)

# External menu -- token account
app.callback(Output('simulation-menu-token-input', 'children'),[Input('simulation-menu-account', 'value')
            ])(SimTab.MenuComputation_Token)

# External menu -- token account update
app.callback(Output('simulation-menu-token-hidden', 'children'),[Input('simulation-menu-token', 'value')
            ])(SimTab.MenuComputation_TokenUpdate)

# Parameters menu
app.callback(Output('simulation-menu-parameters', 'children'),[Input('simulation-menu-algo-type', 'value')
            ])(SimTab.MenuAlgorithm_Parameters)

# Parameters menu -- Update
app.callback(Output('simulation-menu-parameters-hidden', 'children'),[
            Input('simulation-menu-maxit', 'value'),
            Input('simulation-menu-penalty-factor', 'value'),
            Input('simulation-menu-residual-primal', 'value'),
            Input('simulation-menu-residual-dual', 'value')
            ])(SimTab.MenuAlgorithm_ParametersUpdate)

# Visual menu
app.callback(Output('simulation-menu-show-progress', 'children'),[Input('simulation-menu-show', 'value')
            ])(SimTab.MenuVisual_Progress)

# Visual menu - update
app.callback(Output('simulation-menu-progress-hidden', 'children'),[Input('simulation-menu-progress', 'value')
            ])(SimTab.MenuVisual_ProgressUpdate)

# Visual menu - message
app.callback(Output('simulation-menu-launch-message', 'children'),[
            Input('simulation-save-button', 'n_clicks'),
            Input('simulation-launch-button', 'n_clicks')
            ])(SimTab.MenuLaunch_Message)

# Confirm menu
app.callback(Output('simulation-menu-confirm-message', 'children'),[
            Input('simulation-launch-cancel', 'n_clicks'),
            Input('simulation-launch-confirm', 'n_clicks')
            ])(SimTab.MenuLaunch_MessageConfirm)

# Confirm menu -- refresh
app.callback(Output('simulation-menu-refresh', 'children'),[Input('simulation-menu-refresh-trigger', 'n_clicks')
            ])(SimTab.MenuRefresh)

# Fees menu - update
app.callback(Output('simulation-menu-fees-comm', 'children'),[Input('simulation-menu-fees-addcomm', 'value')
            ])(SimTab.MenuFees_Commisions)

# Fees menu - update
app.callback(Output('simulation-menu-fees-comm-ans', 'children'),[
            Input('simulation-menu-fees-p2p', 'value'),
            Input('simulation-menu-fees-community', 'value')
            ])(SimTab.MenuFees_CommisionsUpdate)


#%% Simulation -- Running in progress
# Simulator -- launch menu
@app.callback(Output('tabs', 'style'),[Input('tabs-show-trigger', 'n_clicks')],[State('tabs-show-trigger', 'children')])
def voidfct_Tabs_Style(n_clicks,show):
    if show:
        return {'display':'block'}
    else:
        return {'display':'none'}

# Simulator -- launch menu
app.callback(Output('tab-output-simulation', 'children'),[Input('simulation-trigger', 'n_clicks')
            ])(SimTab.Simulation_on_Tab)

# Simulator -- init
app.callback(Output('simulator-init', 'children'),[Input('simulator-init-trigger', 'n_clicks')
            ])(SimTab.Optimizer.Progress_Start)

# Simulator -- model
app.callback(Output('simulator-model', 'children'),[Input('simulator-model-trigger', 'n_clicks')
            ])(SimTab.Optimizer.Progress_Model)

# Simulator -- optimize
app.callback(Output('simulator-optimize', 'children'),[Input('simulator-optimize-trigger', 'n_clicks')
            ])(SimTab.Optimizer.Progress_Optimize)

# Simulator -- optimizer launched
app.callback(Output('simulator-sim-mess', 'children'),[Input('simulator-sim-trigger', 'n_clicks')
            ])(SimTab.Optimizer.Opti_LocDec_Start)

# Simulator -- update graph
@app.callback(Output('simulator-graph-caps', 'children'),events=[Event('simulator-graph-interval', 'interval')])
def voidfct_Graph_Progress():
    return SimTab.Optimizer.ShowMarketGraph(True)

# Simulator -- stop simulation
app.callback(Output('simulator-refresh', 'children'),[Input('simulator-stop-trigger', 'n_clicks')
            ])(SimTab.Optimizer.ShowResults)

# Simulator -- results option
app.callback(Output('results-options-choice', 'children'),[
            Input('results-option-save-button', 'n_clicks'),
            Input('results-option-report-button', 'n_clicks'),
            Input('results-option-new-button', 'n_clicks')
            ])(SimTab.Optimizer.ShowResults_OptionsConfirm)

# Simulator -- confirm exit simulation
app.callback(Output('results-options-choice-confirm', 'children'),[
            Input('results-option-cancel-button', 'n_clicks'),
            Input('results-option-confirm-button', 'n_clicks')
            ])(SimTab.Optimizer.ShowResults_OptionsConfirmed)

# Simulator -- cancel exit simulation
@app.callback(Output('results-options-choice-refresh', 'children'),[Input('results-option-cancel-trigger', 'n_clicks')])
def voidfct_Exit_Simulator(n_clicks):
    return ''

# Simulator -- exit simulation
@app.callback(Output('MainApp-container', 'children'),[Input('simulator-exit-trigger', 'n_clicks')])
def voidfct_Exit_Simulator(n_clicks):
    return MainApp_Show('Simulation')

# Simulator -- exit simulation
app.callback(Output('simulator-stop-button-hide', 'children'),[Input('simulator-stop-button', 'n_clicks')
            ])(SimTab.Optimizer.Button_Stop)

