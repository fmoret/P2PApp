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
@app.callback(Output('market-topmenu-second', 'children'),[Input('market-topmenu-insert','value')])
def voidfct_Insert(insert_value):
    return MarketTab.TopMenu_Insert(insert_value)

# Action's options - number
@app.callback(Output('market-topmenu-third', 'children'),[Input('market-topmenu-second-drop','value')],[
        State('market-topmenu-insert', 'value')])
def voidfct_Number(example_value,add_value):
    return MarketTab.TopMenu_Number(example_value,add_value)

# Detect click on button 'Add'/'Select'
@app.callback(Output('market-menu', 'children'),[Input('add-button', 'n_clicks')],
              [State('market-topmenu-insert', 'value'),
               State('market-topmenu-second-drop', 'value'),
               State('market-topmenu-third-number', 'value')])
def voidfct_AddButton(n_clicks,add_value,example_value,size_value):
    return MarketTab.Menu(n_clicks,add_value,example_value,size_value)

# Detect click on buttons Refresh
@app.callback(Output('market-menu-agent-refresh', 'children'),[Input('agent-refresh-button', 'n_clicks')])
def voidfct_AgentRefreshButton(n_clicks):
    return MarketTab.Menu_AgentRefresh()

# Change in agent type
@app.callback(Output('market-menu-agent-data', 'children'),[Input('market-menu-agent-type', 'value'),])
def voidfct_AgentType(agent_type):
    return MarketTab.AgentType(agent_type)

# Change in agent data (name, number of assets)
@app.callback(Output('market-menu-assets', 'children'),[
        Input('market-menu-agent-name', 'value'),
        Input('market-menu-agent-number-assets', 'value')
        ])
def voidfct_AgentData(agent_name,agent_n_assets):
    return MarketTab.AgentChange(agent_name,agent_n_assets)

# Change in agent data (community goal, importation fee)
@app.callback(Output('market-menu-agent-impfee-show', 'style'),[
        Input('market-menu-agent-commgoal', 'value'),
        Input('market-menu-agent-impfee', 'value')
        ])
def voidfct_AgentChangeCommGoal(comm_goal,impfee):
    return MarketTab.AgentChangeCommGoal(comm_goal,impfee)

# Change in agent partnerships
@app.callback(Output('market-menu-agent-preferences', 'value'),[Input('market-menu-agent-partners', 'value')],[
        State('market-menu-agent-preferences', 'value')])
def voidfct_AgentPartners(agent_partners,agent_preferences):
    return MarketTab.AgentPartners(agent_partners,agent_preferences)

# Change in agent preferences
@app.callback(Output('market-menu-agent-preferences-void', 'value'),[Input('market-menu-agent-preferences', 'value')])
def voidfct_AgentPreferences(agent_preferences):
    return MarketTab.AgentPreferences(agent_preferences)

# Change in agent community
@app.callback(Output('market-menu-agent-commpref', 'value'),[Input('market-menu-agent-community', 'value')],[
        State('market-menu-agent-commpref', 'value')])
def voidfct_AgentCommunity(agent_community,agent_commpref):
    return MarketTab.AgentCommunity(agent_community,agent_commpref)

# Change in agent community preference
@app.callback(Output('market-menu-agent-commpref-void', 'value'),[Input('market-menu-agent-commpref', 'value')])
def voidfct_AgentCommPref(agent_commpref):
    return MarketTab.AgentCommPref(agent_commpref)

# Assets Tabs
@app.callback(Output('tab-assets-output', 'children'), [Input('tab-assets', 'value')])
def voidfct_AssetsTabs(asset_tab_id):
    return MarketTab.ShowAssetMenu(asset_tab_id)

# Change in asset data (name, type, costfct, costfct_coeff, p_bounds_up, p_bounds_low, ...)
@app.callback(Output('market-menu-asset-void', 'value'),[
        Input('market-menu-asset-name', 'value'),
        Input('market-menu-asset-type', 'value'),
        Input('market-menu-asset-costfct', 'value'),
        Input('market-menu-asset-costfct_coeff', 'value'),
        Input('market-menu-asset-p_bounds_up', 'value'),
        Input('market-menu-asset-p_bounds_low', 'value'),
        ])
def voidfct_AssetData(asset_name,asset_type,asset_costfct,asset_costfct_coeff,asset_p_bounds_up,asset_p_bounds_low):
    return MarketTab.AssetChange(asset_name,asset_type,asset_costfct,asset_costfct_coeff,asset_p_bounds_up,asset_p_bounds_low)

# Detect click on buttons Refresh
@app.callback(Output('market-menu-community-refresh', 'children'),[Input('community-refresh-button', 'n_clicks')])
def voidfct_CommunityRefreshButton(n_clicks):
    return MarketTab.Menu_CommunityRefresh()

# Change in community data 
@app.callback(Output('market-menu-community-members-void', 'value'),[
        Input('market-menu-community-name', 'value'),
        Input('market-menu-community-commgoal', 'value'),
        Input('market-menu-community-members', 'value')
        ])
def voidfct_CommunityData(comm_name,comm_goal,comm_members):
    return MarketTab.CommunityChange(comm_name,comm_goal,comm_members)

# Change in community partnerships
@app.callback(Output('market-menu-community-preferences', 'value'),[Input('market-menu-community-partners', 'value')],[
        State('market-menu-community-preferences', 'value')])
def voidfct_CommunityPartners(comm_partners,comm_preferences):
    return MarketTab.AgentPartners(comm_partners,comm_preferences)

# Change in community preferences
@app.callback(Output('market-menu-community-preferences-void', 'value'),[Input('market-menu-community-preferences', 'value')])
def voidfct_CommunityPreferences(comm_preferences):
    return MarketTab.AgentPreferences(comm_preferences)

# Show the possible types of suppression
@app.callback(Output('market-menu-delete-type', 'children'),[Input('market-menu-delete-select', 'value')])
def voidfct_DeleteType(Selected_Index):
    return MarketTab.Menu_DeleteType(Selected_Index)

# Last warning before suppression of agent, community manager or entire community
@app.callback(Output('market-menu-delete-assets', 'children'),[Input('market-menu-delete-select-type', 'value')])
def voidfct_DeleteAssets(Selected_Type):
    return MarketTab.Menu_DeleteAssets(Selected_Type)

# Last warning before suppression of assets
@app.callback(Output('market-menu-delete-message', 'children'),[Input('market-menu-delete-select-asset', 'value')],[
        State('market-menu-delete-select-type', 'value')])
def voidfct_DeleteWarningWarning(Selected_Assets,Selected_Type):
    return MarketTab.Menu_DeleteWarning(Selected_Assets,Selected_Type)

# Suppression after confirmation
@app.callback(Output('market-menu-delete-refresh','children'),[
        Input('market-menu-delete-cancel-button', 'n_clicks'),
        Input('market-menu-delete-confirm-button', 'n_clicks')
        ],[
        State('market-menu-delete-select-type', 'value'),
        State('market-menu-delete-select-asset', 'value')
        ])
def voidfct_DeleteConfirmed(n_cancel,n_confirm,delete_type,delete_asset):
    return MarketTab.Menu_DeleteConfirmed(n_cancel,n_confirm,delete_type,delete_asset)

# Show confirm buttons
@app.callback(Output('market-menu-delete-confirm-buttons', 'style'),[Input('market-menu-delete-show-confirm-button', 'n_clicks')],[
        State('market-menu-delete-show-confirm-button', 'children')])
def voidfct_DeleteShowConfirmed(n_clicks,show_disp):
    return MarketTab.Menu_DeleteShowConfirmed(show_disp)

# Save button
@app.callback(Output('market-menu-save-message', 'children'),[Input('market-menu-save-button', 'n_clicks')],[
        State('market-menu-saveas-filename', 'value')])
def voidfct_SaveGraph(n_clicks,filename):
    return MarketTab.Menu_SaveGraph(n_clicks,filename)

# Save button message
@app.callback(Output('market-menu-save-refresh', 'children'),[Input('market-menu-save-button-message', 'n_clicks')],[
        State('market-menu-save-button-message', 'children')])
def voidfct_SaveGraphMessage(n_clicks,message):
    return [message]

# Add file save button
@app.callback(Output('market-menu-addfile-select', 'children'),[Input('market-menu-addfile-extension', 'value')],[
        State('market-topmenu-insert', 'value'),
        State('market-topmenu-second-drop', 'value')])
def voidfct_AddFileSelect(extension,actiontype,filetype):
    return MarketTab.Menu_AddFileSelect(extension,actiontype,filetype)

# Add file connectivity type
@app.callback(Output('market-menu-addfile-prefs', 'children'),[Input('market-menu-addfile-connect-matrix', 'value')])
def voidfct_AddFilePrefs(connectivity):
    return MarketTab.Menu_AddFilePrefs(connectivity)

# Add file save button
@app.callback(Output('market-menu-addfile-message', 'children'),[Input('market-menu-addfile-button', 'n_clicks')],[
        State('market-menu-addfile-filename', 'value'),
        State('market-menu-addfile-extension', 'value'),
        State('market-menu-addfile-type', 'value'),
        State('market-menu-addfile-connect-matrix', 'value'),
        State('market-menu-addfile-pref-filename', 'value'),
        State('market-menu-addfile-pref-ceil', 'value')])
def voidfct_AddFileMessage(n_clicks,filename,extension,actiontype,connectivity,pref_file,pref_ceil):
    return MarketTab.Menu_AddFileMessage(n_clicks,filename,extension,actiontype,connectivity,pref_file,pref_ceil)

# Add file save button message
@app.callback(Output('market-menu-addfile-refresh', 'children'),[Input('market-menu-addfile-button-message', 'n_clicks')],[
        State('market-menu-addfile-button-message', 'children')])
def voidfct_AddFileMessageOut(n_clicks,message):
    return [message]

# Link menu -- who
@app.callback(Output('market-menu-link', 'children'),[Input('market-menu-link-type', 'value')])
def voidfct_LinkWho(link_type):
    return MarketTab.Menu_LinkWho(link_type)

# Link menu -- with
@app.callback(Output('market-menu-link2', 'children'),[Input('market-menu-link-who', 'value')],[
        State('market-menu-link-type', 'value'),
        State('market-menu-link-type', 'className')])
def voidfct_LinkWith(who,link_type,add_value):
    return MarketTab.Menu_LinkWith(who,link_type,add_value)

# Link menu -- prefs
@app.callback(Output('market-menu-link-prefs', 'children'),[Input('market-menu-link-with', 'value')],[
        State('market-menu-link-who', 'value'),
        State('market-menu-link-type', 'value'),
        State('market-menu-link-type', 'className')])
def voidfct_LinkPrefs(who2,who1,link_type,add_value):
    return MarketTab.Menu_LinkPrefs(who1,who2,link_type,add_value)

# Link menu -- update
@app.callback(Output('market-menu-link-refresh-trigger', 'children'),[Input('market-menu-link-confirm-button', 'n_clicks')],[
        State('market-menu-link-who', 'value'),
        State('market-menu-link-with', 'value'),
        State('market-menu-link-pref1', 'value'),
        State('market-menu-link-pref2', 'value'),
        State('market-menu-link-type', 'value'),
        State('market-menu-link-type', 'className')])
def voidfct_LinkConfirmed(n_clicks,who1,who2,pref1,pref2,link_type,add_value):
    return MarketTab.Menu_LinkConfirmed(n_clicks,who1,who2,pref1,pref2,link_type,add_value)

# Link menu -- refresh
@app.callback(Output('market-menu-link-refresh', 'children'),[Input('market-menu-link-refresh-button', 'n_clicks')])
def voidfct_LinkRefresh(n_clicks):
    return MarketTab.Menu_LinkRefresh()


#%% Simulation tab

# External menu
@app.callback(Output('simulation-menu-external', 'children'),[Input('simulation-menu-location', 'value'),Input('simulation-menu-target', 'value')])
def voidfct_MenuExternal(location,target):
    return SimTab.MenuComputation_External(location,target)

# External menu -- token account
@app.callback(Output('simulation-menu-token-input', 'children'),[Input('simulation-menu-account', 'value')])
def voidfct_MenuToken(account):
    return SimTab.MenuComputation_Token(account)

# External menu -- token account update
@app.callback(Output('simulation-menu-token-hidden', 'children'),[Input('simulation-menu-token', 'value')])
def voidfct_MenuTokenUpdate(token):
    return SimTab.MenuComputation_TokenUpdate(token)

# Parameters menu
@app.callback(Output('simulation-menu-parameters', 'children'),[Input('simulation-menu-algo-type', 'value')])
def voidfct_MenuAlgoParameters(algo):
    return SimTab.MenuAlgorithm_Parameters(algo)

# Parameters menu -- Update
@app.callback(Output('simulation-menu-parameters-hidden', 'children'),[
        Input('simulation-menu-maxit', 'value'),
        Input('simulation-menu-penalty-factor', 'value'),
        Input('simulation-menu-residual-primal', 'value'),
        Input('simulation-menu-residual-dual', 'value')])
def voidfct_MenuAlgoParametersUpdate(maxit,penalty,primal,dual):
    return SimTab.MenuAlgorithm_ParametersUpdate(maxit,penalty,primal,dual)

# Visual menu
@app.callback(Output('simulation-menu-show-progress', 'children'),[Input('simulation-menu-show', 'value')])
def voidfct_MenuProgress(show):
    return SimTab.MenuVisual_Progress(show)

# Visual menu - update
@app.callback(Output('simulation-menu-progress-hidden', 'children'),[Input('simulation-menu-progress', 'value')])
def voidfct_MenuProgressUpdate(progress):
    return SimTab.MenuVisual_ProgressUpdate(progress)

# Visual menu - message
@app.callback(Output('simulation-menu-launch-message', 'children'),[
        Input('simulation-save-button', 'n_clicks'),
        Input('simulation-launch-button', 'n_clicks')])
def voidfct_MenuLaunchMessage(save,launch):
    return SimTab.MenuLaunch_Message(save,launch)

# Confirm menu
@app.callback(Output('simulation-menu-confirm-message', 'children'),[
        Input('simulation-launch-cancel', 'n_clicks'),
        Input('simulation-launch-confirm', 'n_clicks')])
def voidfct_MenuLaunchMessageConfirm(cancel,confirm):
    return SimTab.MenuLaunch_MessageConfirm(cancel,confirm)

# Confirm menu -- refresh
@app.callback(Output('simulation-menu-refresh', 'children'),[Input('simulation-menu-refresh-trigger', 'n_clicks')])
def voidfct_MenuRefresh(n_clicks):
    return SimTab.MenuRefresh(n_clicks)

# Fees menu - update
@app.callback(Output('simulation-menu-fees-comm', 'children'),[Input('simulation-menu-fees-addcomm', 'value')])
def voidfct_MenuFees_Commisions(add):
    return SimTab.MenuFees_Commisions(add)

# Fees menu - update
@app.callback(Output('simulation-menu-fees-comm-ans', 'children'),[
        Input('simulation-menu-fees-p2p', 'value'),
        Input('simulation-menu-fees-community', 'value')])
def voidfct_MenuFees_CommisionsUpdate(p2p,comm):
    return SimTab.MenuFees_CommisionsUpdate(p2p,comm)


#%% Simulation -- Running in progress
# Simulator -- launch menu
@app.callback(Output('tabs', 'style'),[Input('tabs-show-trigger', 'n_clicks')],[State('tabs-show-trigger', 'children')])
def voidfct_Tabs_Style(n_clicks,show):
    if show:
        return {'display':'block'}
    else:
        return {'display':'none'}

# Simulator -- launch menu
@app.callback(Output('tab-output-simulation', 'children'),[Input('simulation-trigger', 'n_clicks')])
def voidfct_Simulation_on_Tab(n_clicks):
    return SimTab.Simulation_on_Tab(n_clicks)

# Simulator -- init
@app.callback(Output('simulator-init', 'children'),[Input('simulator-init-trigger', 'n_clicks')])
def voidfct_Progress_Start(n_clicks):
    return SimTab.Optimizer.Progress_Start(n_clicks)

# Simulator -- model
@app.callback(Output('simulator-model', 'children'),[Input('simulator-model-trigger', 'n_clicks')])
def voidfct_Progress_Model(n_clicks):
    return SimTab.Optimizer.Progress_Model(n_clicks)

# Simulator -- optimize
@app.callback(Output('simulator-optimize', 'children'),[Input('simulator-optimize-trigger', 'n_clicks')])
def voidfct_Progress_Optimize(n_clicks):
    return SimTab.Optimizer.Progress_Optimize(n_clicks)

# Simulator -- optimizer launched
@app.callback(Output('simulator-sim-mess', 'children'),[Input('simulator-sim-trigger', 'n_clicks')])
def voidfct_Opti_Start(n_clicks):
    return SimTab.Optimizer.Opti_LocDec_Start(n_clicks)

# Simulator -- update graph
@app.callback(Output('simulator-graph-caps', 'children'),events=[Event('simulator-graph-interval', 'interval')])
def voidfct_Graph_Progress():
    return SimTab.Optimizer.ShowMarketGraph(True)

# Simulator -- stop simulation
@app.callback(Output('simulator-refresh', 'children'),[Input('simulator-stop-trigger', 'n_clicks')])
def voidfct_ShowResults(n_clicks):
    return SimTab.Optimizer.ShowResults(n_clicks)

# Simulator -- results option
@app.callback(Output('results-options-choice', 'children'),[
        Input('results-option-save-button', 'n_clicks'),
        Input('results-option-report-button', 'n_clicks'),
        Input('results-option-new-button', 'n_clicks')])
def voidfct_ShowResults(n_save,n_report,n_new):
    return SimTab.Optimizer.ShowResults_OptionsConfirm(n_save,n_report,n_new)

# Simulator -- confirm exit simulation
@app.callback(Output('results-options-choice-confirm', 'children'),[
        Input('results-option-cancel-button', 'n_clicks'),
        Input('results-option-confirm-button', 'n_clicks')])
def voidfct_Exit_Simulator(n_cancel,n_confirm):
    return SimTab.Optimizer.ShowResults_OptionsConfirmed(n_cancel,n_confirm)

# Simulator -- cancel exit simulation
@app.callback(Output('results-options-choice-refresh', 'children'),[Input('results-option-cancel-trigger', 'n_clicks')])
def voidfct_Exit_Simulator(n_clicks):
    return ''

# Simulator -- exit simulation
@app.callback(Output('MainApp-container', 'children'),[Input('simulator-exit-trigger', 'n_clicks')])
def voidfct_Exit_Simulator(n_clicks):
    return MainApp_Show('Simulation')

# Simulator -- exit simulation
@app.callback(Output('simulator-stop-button-hide', 'children'),[Input('simulator-stop-button', 'n_clicks')])
def voidfct_Button_Stop(n_clicks):
    return SimTab.Optimizer.Button_Stop(n_clicks)

