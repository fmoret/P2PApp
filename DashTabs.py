# -*- coding: utf-8 -*-
"""
    File managing Dash tabs layout
"""

#import datetime
import dash_core_components as dcc
import dash_html_components as html
from MGraph import MGraph
from SimulatorApp import Simulator

class TabApp:
    def __init__(self,Market=None,Optimizer=None):
        # Default parameters
        self.ShareWidth()
        self.init_GraphOfMarketGraph()
        # Granting access to Market's graph 
        if Market is None:
            self.MGraph = MGraph(directed=True)
        else:
            self.MGraph = Market
        if Optimizer is None:
            self.Optimizer = Simulator()
        else:
            self.Optimizer = Optimizer
#        # Granting access to information on simulation activity
##        self.Optimizer.simulation_on = simulation_on
##        self.Optimizer.simulation_on_tab = False
#        self.Optimizer.simulation_on = True
#        self.Optimizer.simulation_on_tab = True
        self.n_clicks_tab = 0
    
    def ShareWidth(self,menu=None,graph=None):
        if menu is None:
            menu='40%'
        if graph is None:
            graph='60%'
        self.share_width_menu = menu
        self.share_width_graph = graph
        self.defaultTable = html.Div([
                html.Div([], style={'display':'table-cell','width':'30%'}),
                html.Div([], style={'display':'table-cell','width':'50%'}),
                html.Div([], style={'display':'table-cell','width':'3%'}),
                html.Div([], style={'display':'table-cell','width':'17%'}),
                ], style={'display':'table-row'})

    def MenuTab(self,menu_data=[],graph_data=[],bottom_data=[]):
        if menu_data==[]:
            width_menu = '0%'
            width_graph = '100%'
        elif graph_data==[]:
            width_graph = '0%'
            width_menu = '100%'
        else:
            width_menu = self.share_width_menu
            width_graph = self.share_width_graph
        
        return html.Div([
                html.Div([
                    html.Div(menu_data, style={'width': width_menu, 'display': 'inline-block','vertical-align': 'top'}),
                    html.Div(graph_data, style= {'width': width_graph, 'display': 'inline-block'})
                ], style= {'width': '100%', 'display': 'block'}),
                html.Div(bottom_data, style= {'width': '100%', 'display': 'block'})
            ], id='tab-output-simulation')
    
    def ShowTab(self,tab_id):
        menu_data = []
        graph_data = []
        bottom_data = []
        return self.MenuTab(menu_data,graph_data,bottom_data)
    
    #%% Market graph -- management and plot
    def ListAgentsName(self,out_list=[]):
        ag_list = []
        for i in self.ListAgentsIndex(out_list):
            ag_list.append(self.MGraph.vs[i]['name'])
        return ag_list
    
    def ListAgentsIndex(self,out_list=[]):
        show_list = []
        for i in range(len(self.MGraph.vs)):
            if self.MGraph.vs[i].index not in out_list:
                show_list.append(self.MGraph.vs[i].index)
        return show_list
    
    def ListAgentsType(self):
        ag_list = []
        for i in range(len(self.MGraph.vs)):
            ag_list.append(self.MGraph.vs[i]['Type'])
        return ag_list
    
    def ListAgentsNumberAssets(self):
        ag_list = []
        for i in range(len(self.MGraph.vs)):
            ag_list.append(self.MGraph.vs[i]['AssetsNum'])
        return ag_list
    
    def init_GraphOfMarketGraph(self):
        self.GraphInterval = 3 # in secondes
        
    
    def ShowMarketGraph(self,interval=True,update=False):
        cells = [
                html.Div([],id='market-graph-top'),
                html.Div([self.MGraph.BuildGraphOfMarketGraph(update)],id='market-graph-graph'),
                html.Div([],id='market-graph-down'),
                html.Div([],id='market-graph-hidden',style={'display':'none'})
                ]
        if interval:
            cells.extend([dcc.Interval(id='market-graph-interval',interval=self.GraphInterval*1000)])  
        return html.Div(cells, id='market-graph-refresh')  
    
    
    #%% Running Simulation -- Progress display
    def Simulation_on_Tab(self,n_clicks=None):
        if self.Optimizer.simulation_on_tab or (n_clicks is not None and self.n_clicks_tab!=n_clicks):
            return self.Optimizer.ShowProgress()
        else:
            self.Optimizer.simulation_on_tab = True
            return html.Div([html.Button(children='Show progress', id = 'simulation-trigger', type='submit', n_clicks=self.n_clicks_tab)])
    
    
    
    
    
    