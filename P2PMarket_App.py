# -*- coding: utf-8 -*-
"""
    Main file of P2PMarket_App application for consumer-centric markets
"""

import dash 
from dash.dependencies import Event, Output, Input, State
import dash_core_components as dcc
import dash_html_components as html

from igraph import *
Market = Graph(directed=True)

#from DashTabs import TabApp
#SimTab = TabApp(Market)
from SimulationTab import SimulationTabApp
from MarketTab import MarketTabApp
SimTab = SimulationTabApp(Market)
MarketTab = MarketTabApp(Market)

#import datetime
#import json
#import pandas_datareader.data as web
#import plotly
#import random
#import time
#import plotly.graph_objs as go
#from collections import deque
#from loremipsum import get_sentences


app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    #html.Div(['Project: Delta']),
    dcc.Tabs(
        tabs=[
            {'label': 'Market network', 'value': 1},
            {'label': 'Simulation', 'value': 2}
        ],
        value=1,
        id='tabs'
    ),
    html.Div(id='tab-output')
], style={
    'width': '98%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})


#%% Callbacks
#%% General Tab layout
@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def voidfct_GeneralTab(tab_id):
    if tab_id==1:
        return MarketTab.ShowTab(tab_id)
    else:
        return SimTab.ShowTab(tab_id)

#%% Market tab
# Action's options
@app.callback(Output('market-topmenu-second', 'children'),[Input('market-topmenu-insert','value')])
def voidfct_Insert(insert_value):
    return MarketTab.ShowTabMarketTopMenu_Insert(insert_value)

# Action's options - number
@app.callback(Output('market-topmenu-third', 'children'),[Input('market-topmenu-second-drop','value')],[State('market-topmenu-insert', 'value')])
def voidfct_Number(example_value,add_value):
    return MarketTab.ShowTabMarketTopMenu_Number(example_value,add_value)

# Detect click on button 'Add'/'Select'
@app.callback(Output('market-menu', 'children'),[Input('add-button', 'n_clicks')],
              [State('market-topmenu-insert', 'value'),State('market-topmenu-second-drop', 'value'),State('market-topmenu-third-number', 'value')])
def voidfct_AddButton(n_clicks,add_value,example_value,size_value):
    return MarketTab.ShowTabMarketMenu(n_clicks,add_value,example_value,size_value)

# Detect click on buttons Refresh
@app.callback(Output('market-menu-agent-refresh', 'children'),[Input('agent-refresh-button', 'n_clicks')])
def voidfct_AgentRefreshButton(n_clicks):
    return MarketTab.ShowTabMarketMenu_AgentRefresh()

# Change in agent type
@app.callback(Output('market-menu-agent-data', 'children'),[Input('market-menu-agent-type', 'value'),])
def voidfct_AgentType(agent_type):
    return MarketTab.AgentType(agent_type)

# Change in agent data (name, type, number of assets)
@app.callback(Output('market-menu-assets', 'children'),[
        Input('market-menu-agent-name', 'value'),
        Input('market-menu-agent-commgoal', 'value'),
        Input('market-menu-agent-number-assets', 'value')
        ])
def voidfct_AgentData(agent_name,comm_goal,agent_n_assets):
    return MarketTab.AgentChange(agent_name,comm_goal,agent_n_assets)

# Change in agent partnerships
@app.callback(Output('market-menu-agent-preferences', 'value'),[Input('market-menu-agent-partners', 'value')],[State('market-menu-agent-preferences', 'value')])
def voidfct_AgentPartners(agent_partners,agent_preferences):
    return MarketTab.AgentPartners(agent_partners,agent_preferences)

# Change in agent preferences
@app.callback(Output('market-menu-agent-preferences-void', 'value'),[Input('market-menu-agent-preferences', 'value')])
def voidfct_AgentPreferences(agent_preferences):
    return MarketTab.AgentPreferences(agent_preferences)

# Change in agent community
@app.callback(Output('market-menu-agent-commpref', 'value'),[Input('market-menu-agent-community', 'value')],[State('market-menu-agent-commpref', 'value')])
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

@app.callback(Output('market-graph-graph', 'children'),events=[Event('market-graph-interval', 'interval')])
def voidfct_IntervalGraphUpdate():
    return MarketTab.BuildGraphOfMarketGraph()

# Detect click on buttons Refresh
@app.callback(Output('market-menu-community-refresh', 'children'),[Input('community-refresh-button', 'n_clicks')])
def voidfct_CommunityRefreshButton(n_clicks):
    return MarketTab.ShowTabMarketMenu_CommunityRefresh()

# Change in community data 
@app.callback(Output('market-menu-community-members-void', 'value'),[
        Input('market-menu-community-name', 'value'),
        Input('market-menu-community-commgoal', 'value'),
        Input('market-menu-community-members', 'value')
        ])
def voidfct_CommunityData(comm_name,comm_goal,comm_members):
    return MarketTab.CommunityChange(comm_name,comm_goal,comm_members)

# Change in community partnerships
@app.callback(Output('market-menu-community-preferences', 'value'),[Input('market-menu-community-partners', 'value')],[State('market-menu-community-preferences', 'value')])
def voidfct_CommunityPartners(comm_partners,comm_preferences):
    return MarketTab.AgentPartners(comm_partners,comm_preferences)

# Change in community preferences
@app.callback(Output('market-menu-community-preferences-void', 'value'),[Input('market-menu-community-preferences', 'value')])
def voidfct_CommunityPreferences(comm_preferences):
    return MarketTab.AgentPreferences(comm_preferences)

# Show the possible types of suppression
@app.callback(Output('market-menu-delete-type', 'children'),[Input('market-menu-delete-select', 'value')])
def voidfct_DeleteType(Selected_Index):
    return MarketTab.ShowTabMarketMenu_DeleteType(Selected_Index)

# Last warning before suppression of agent, community manager or entire community
@app.callback(Output('market-menu-delete-assets', 'children'),[Input('market-menu-delete-select-type', 'value')])
def voidfct_DeleteAssets(Selected_Type):
    return MarketTab.ShowTabMarketMenu_DeleteAssets(Selected_Type)

# Last warning before suppression of assets
@app.callback(Output('market-menu-delete-message', 'children'),[Input('market-menu-delete-select-asset', 'value')],[State('market-menu-delete-select-type', 'value')])
def voidfct_DeleteWarningWarning(Selected_Assets,Selected_Type):
    return MarketTab.ShowTabMarketMenu_DeleteWarning(Selected_Assets,Selected_Type)

# Suppression after confirmation
@app.callback(Output('market-menu-delete-refresh','children'),[
        Input('market-menu-delete-cancel-button', 'n_clicks'),
        Input('market-menu-delete-confirm-button', 'n_clicks')
        ],[
        State('market-menu-delete-select-type', 'value'),
        State('market-menu-delete-select-asset', 'value')
        ])
def voidfct_DeleteConfirmed(n_cancel,n_confirm,delete_type,delete_asset):
    return MarketTab.ShowTabMarketMenu_DeleteConfirmed(n_cancel,n_confirm,delete_type,delete_asset)

# Show confirm buttons
@app.callback(Output('market-menu-delete-confirm-buttons', 'style'),[Input('market-menu-delete-show-confirm-button', 'n_clicks')],[State('market-menu-delete-show-confirm-button', 'children')])
def voidfct_DeleteShowConfirmed(n_clicks,show_disp):
    return MarketTab.ShowTabMarketMenu_DeleteShowConfirmed(show_disp)

# Save button
@app.callback(Output('market-menu-save-message', 'children'),[Input('market-menu-save-button', 'n_clicks')],[State('market-menu-saveas-filename', 'value')])
def voidfct_SaveGraph(n_clicks,filename):
    return MarketTab.ShowTabMarketMenu_SaveGraph(n_clicks,filename)

# Save button message
@app.callback(Output('market-menu-save-refresh', 'children'),[Input('market-menu-save-button-message', 'n_clicks')],[State('market-menu-save-button-message', 'children')])
def voidfct_SaveGraphMessage(n_clicks,message):
    return [message]

# Save button
@app.callback(Output('market-menu-addfile-message', 'children'),[Input('market-menu-addfile-button', 'n_clicks')],[State('market-menu-addfile-filename', 'value'),State('market-menu-addfile-type', 'value')])
def voidfct_AddFile(n_clicks,filename,actiontype):
    return MarketTab.ShowTabMarketMenu_AddFileMessage(n_clicks,filename,actiontype)

# Save button message
@app.callback(Output('market-menu-addfile-refresh', 'children'),[Input('market-menu-addfile-button-message', 'n_clicks')],[State('market-menu-addfile-button-message', 'children')])
def voidfct_AddFileMessage(n_clicks,message):
    return [message]





if __name__ == '__main__':
    app.run_server(debug=True)
