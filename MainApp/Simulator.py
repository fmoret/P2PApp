# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 15:56:13 2018

@author: Thomas
"""

import time
import dash_core_components as dcc
import dash_html_components as html
#import plotly.plotly as py
#import plotly.graph_objs as go
#from igraph import *
#import os
#import pandas as pd
import numpy as np
from .MGraph import MGraph
from .Prosumer import Prosumer

class Simulator:
    def __init__(self): 
        self.simulation_on = False
        self.simulation_on_tab = False
        self.optimizer_on = False
        self.simulation_message = False
        self.init_test()
        self.n_clicks_tab = 0
        self.verbose = True
        self.timeout = 3600 # in s
        self.Interval = 3 # in s
        self.ShareWidth()
        self.full_progress = []
        # Default optimization parameters
        self.algorithm = 'Decentralized'
        self.target = 'CPU'
        self.location = 'local'
        self.account = 'AWS'
        self.account_token = ''
        self.Registered_Token()
        self.maximum_iteration = 5000
        self.penaltyfactor = 1
        self.residual_primal = 1e-4
        self.residual_dual = 1e-4
        self.communications = 'Synchronous'
        self.show = True
        self.progress = 'Partial'
        # Optimization model
        self.players = {}
        self.Trades = 0
        return
    
    def init_test(self):
        if self.simulation_on and self.simulation_on_tab:
#            self.MGraph = MGraph.Load('graphs/examples/PCM_multi_Community.pyp2p', format='picklez')
            self.MGraph = MGraph.Load('graphs/examples/PCM_single_P2P.pyp2p', format='picklez')
            self.MGraph.BuildGraphOfMarketGraph(True)
            self.SGraph = self.MGraph
        return
    
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
        self.ProgressTable = html.Div([
                html.Div([], style={'display':'table-cell','width':'15%'}),
                html.Div([], style={'display':'table-cell','width':'22%'}),
                html.Div([], style={'display':'table-cell','width':'22%'}),
                html.Div([], style={'display':'table-cell','width':'22%'}),
                html.Div([], style={'display':'table-cell','width':'19%'}),
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
            ], id='simulator-main')
    
    #%% Parameters management
    def Parameters_Save(self):
        message = [html.Div([dcc.Markdown('*Simulation parameters have been saved.*')])]
        return message
    
    def Parameters_Test(self):
        message = []
        if self.location=='local':
            test_loc = True
        else:
            test_loc = False
            message.extend([html.Div([dcc.Markdown('**Simulation on an external server is not possible yet.**')])])
        if self.algorithm=='Decentralized':
            test_algo = True
        else:
            test_algo = False
            message.extend([html.Div([dcc.Markdown('**Centralized simulation is not possible yet.**')])])
        if self.target=='CPU':
            test_target = True
        else:
            test_target = False
            message.extend([html.Div([dcc.Markdown('**Simulation on GPU is not possible yet.**')])])
            
        test = test_loc and test_algo and test_target
        return test, message
    
    def Registered_Token(self,account='AWS'):
        # Look into pre-registered tokens
        if self.account_token == '':
            self.account_token = ''
        return
    
    
    #%% Graph management
    def LoadMGraph(self,MGraph):
        self.MGraph = MGraph
        #self.MGraph.save('temp/graph_presim.pyp2p', format='picklez')
        self.MGraph.Save(self.MGraph,'temp/graph_presim.pyp2p', format='picklez')
        self.SGraph = self.MGraph
        return
    
    #%% Progress management
    def ShowProgress(self,In=True):
        test, out = self.Parameters_Test()
        if test:
            bottom_data = []
            if self.progress=='Full':
                graph_data = self.Graph_Progress(In)
            else:
                graph_data = self.ShowMarketGraph(In)
            menu_data = self.Progress_Main()
            return html.Div([
                    html.Div([html.Button(children=False, id = 'tabs-show-trigger', type='submit', n_clicks=0)],style={'display':'none'}),
                    self.MenuTab(menu_data,graph_data,bottom_data)
                    ],id='simulator-refresh')
        else:
            return out
    
    #%% Progress display -- Terminal
    def Progress_Main(self):
        self.full_progress = []
        return html.Div(self.Progress_Start())
    
    def ProgressMessage(self,next_message='',message=[]):
        self.full_progress.extend(message)
        return html.Div([
                html.Div(message),
                html.Div([
                        html.Button(children='', id = 'simulator-'+next_message+'-trigger', type='submit', n_clicks=self.n_clicks_tab)
                        ],style={'display':'none'}),
                html.Div([],id='simulator-'+next_message),
                ])
    
    def Progress_Start(self,click=None):
        if click is not None:
            self.n_clicks_tab = click
            if not self.optimizer_on:
                self.Opti_LocDec_Init()
            return self.Progress_Model()
        else:
            message = [
                    html.Br(),
                    html.Div([html.B(['Optimizer feedbacks:'],style={'text-decoration':'underline'})]),
                    html.Div([html.B('Init ...')]),
                    html.Div(['Initializing parameters ...']),
                    ]
            return self.ProgressMessage('init',message)
    
    def Progress_Model(self,click=None):
        if click is not None:
            self.n_clicks_tab = click
            if not self.optimizer_on:
                self.Opti_LocDec_InitModel()
#            return
            return self.Progress_Optimize()
        else:
            message = [html.Div(['Constructing model ...'])]
            return self.ProgressMessage('model',message)
    
    def Progress_Optimize(self,click=None):
        if click is not None:
            self.n_clicks_tab = click
            self.start_sim = time.clock()
            return self.Opti_LocDec_State()
        else:
            message = [
                    html.Div([html.B('Optimize ...')]),
                    html.Div([
                        self.ProgressTable,
                        html.Div([
                                html.Div(['it'], style={'display':'table-cell'}),
                                html.Div(['SW'], style={'display':'table-cell'}),
                                html.Div(['Primal'], style={'display':'table-cell'}),
                                html.Div(['Dual'], style={'display':'table-cell'}),
                                html.Div(['Avg Price'], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        ], style={'display':'table','width':'100%'}),
                    ]
            return self.ProgressMessage('optimize',message)
    
    
    #%% Progress display -- Graph
    def ShowMarketGraph(self,update=False,In=True):
        if In:
            return html.Div([self.SGraph.UpdateGraphEdges(update,self.Trades)],id='simulator-graph-graph')  
        else:
            return html.Div([self.SGraph.BuildGraphOfMarketGraph(update)],id='simulator-graph-graph')  
    
    def Graph_Progress(self,In=True,click=None):
        return html.Div(self.Graph_Refresh(click,In),id='simulator-graph-refresh')
    
    def Graph_Refresh(self,n_clicks=None,In=True):
        if n_clicks is None:
            return [
                    html.Div([self.ShowMarketGraph(True,In)],id='simulator-graph-caps'),
                    html.Div([dcc.Interval(id='simulator-graph-interval',interval=self.Interval*1000)],style={'display':'none'})
                    ]
        else:
            return [html.Div([self.ShowMarketGraph(True,In)],id='simulator-graph-caps')]
    
    
    #%% Optimization
    def Opti_LocDec_Init(self):
        nag = len(self.MGraph.vs)
        self.nag = nag
        self.Trades = np.zeros([nag,nag])
        self.Prices = np.zeros([nag,nag])
        self.iteration = 0
        self.iteration_last = -1
        self.SW = 0
        self.prim = float("inf")
        self.dual = float("inf")
        self.Price_avg = 0
        self.simulation_time = 0
        self.opti_progress = [self.ProgressTable]
        return
    
    def Opti_LocDec_InitModel(self):
        part = np.zeros(self.Trades.shape)
        pref = np.zeros(self.Trades.shape)
        for es in self.MGraph.es:
            part[es.source][es.target] = 1
            pref[es.source][es.target] = es['weight']
        for x in self.MGraph.vs:
            self.players[x.index] = Prosumer(agent=x, partners=part[x.index], preferences=pref[x.index], rho=self.penaltyfactor)
        self.part = part
        return
    
    def Opti_LocDec_State(self,out=False):
        if self.iteration_last < self.iteration:
            self.iteration_last = self.iteration
            self.opti_progress.extend([
                            html.Div([
                                    html.Div([f'{self.iteration}'], style={'display':'table-cell'}),
                                    html.Div([f'{self.SW:.3g}'], style={'display':'table-cell'}),
                                    html.Div([f'{self.prim:.3g}'], style={'display':'table-cell'}),
                                    html.Div([f'{self.dual:.3g}'], style={'display':'table-cell'}),
                                    html.Div([f'{self.Price_avg:.2f}'], style={'display':'table-cell'}),
                                    ], style={'display':'table-row'})
                            ])
        if out:
            self.full_progress.extend([
                        html.Div(self.opti_progress, style={'display':'table','width':'100%'}),
                        html.Div([f'Total simulation time: {self.simulation_time:.1f} s']),
                        html.Div([html.Button(children='', id = 'simulator-graph-end', type='submit', n_clicks=self.n_clicks_tab)],style={'display':'none'}),
                        html.Div(['Optimization stopped.']),
                        html.Br(),
                        self.ErrorMessages()
                    ])
            return html.Div([html.Button(children='', id = 'simulator-stop-trigger', type='submit', n_clicks=self.n_clicks_tab)],style={'display':'none'})
        else:
            return html.Div([
                    html.Div(self.opti_progress, style={'display':'table','width':'100%'}),
                    html.Div(['...']),
                    html.Div([f'Running time: {self.simulation_time:.1f} s']),
                    html.Div([
                            html.Button(children='', id = 'simulator-sim-trigger', type='submit', n_clicks=self.n_clicks_tab)
                            ],style={'display':'none'})
                    ], id='simulator-sim-mess')
    
    def Opti_LocDec_Start(self,click=None):
        if click is not None:
            if not self.optimizer_on:
                self.optimizer_on = True
                self.start_sim = time.clock()
                self.simulation_time = 0
            lapsed = 0
            start_time = time.clock()
            while (self.prim>self.residual_primal or self.dual>self.residual_dual) and self.iteration<self.maximum_iteration and lapsed<=self.Interval:
                self.iteration += 1
                temp = np.copy(self.Trades)
                for i in range(self.nag):
                    temp[:,i] = self.players[i].optimize(self.Trades[i,:])
                    self.Prices[:,i][self.part[i,:].nonzero()] = self.players[i].y
                self.Trades = np.copy(temp)
                self.prim = sum([self.players[i].Res_primal for i in range(self.nag)])
                self.dual = sum([self.players[i].Res_dual for i in range(self.nag)])
                lapsed = time.clock()-start_time
            
            # Displayed data
            self.simulation_time += lapsed
            self.Price_avg = self.Prices[self.Prices!=0].mean()
            self.SW = sum([self.players[i].SW for i in range(self.nag)])
            
            if self.Opti_End_Test():
                self.Opti_LocDec_Stop()
                return self.Opti_LocDec_State(True)
            else:
                return self.Opti_LocDec_State(False)
    
    def Opti_LocDec_Stop(self):
        self.optimizer_on = False
        self.simulation_on_tab = False
        self.simulation_on = False
        return
    
    def Opti_End_Test(self):
        if self.prim<=self.residual_primal and self.dual<=self.residual_dual:
            self.simulation_message = 1
        elif self.iteration>=self.maximum_iteration:
            self.simulation_message = -1
        elif self.simulation_time>=self.timeout:
            self.simulation_message = -2
        else:
            self.simulation_message = 0
        return self.simulation_message
    
    #%% Results display
    def ErrorMessages(self):
        errors=[]
        if self.simulation_message==1:
            errors.extend([
                    html.Div([f'Simulation converged after {self.iteration} iterations']),
                    html.Div([f'in {self.simulation_time:.1f} seconds.']),
                    html.Div([f'The total social welfare is of {self.SW:.0f} $']),
                    html.Div([f'The total amount of power traded is {abs(self.Trades).sum()/2:.0f} W']),
                    html.Div([f'with an average trading price of {self.Price_avg:.2f} $/Wh']),
                    ])
        else:
            errors.append( html.Div([html.B("Simulation did not converge.")]) )
            if self.simulation_message==-1:
                errors.append( html.Div(["Maximum number of iterations has been reached."]) )
            elif self.simulation_message==-2:
                errors.append( html.Div(["Simulation time exceeded timeout."]) )
            else:
                errors.append( html.Div(["Something went wrong."]) )
        return html.Div([
                html.Div([html.B(['Optimizer messages:'],style={'text-decoration':'underline'})]),
                html.Div(errors)
                ])
    
    def ShowResults(self,click=None):
        bottom_data = []
        graph_data = self.ShowMarketGraph(True)
        menu_data = html.Div([
                        html.Div(self.full_progress),
                        html.Hr(),html.Br(),
                        html.Div(self.ShowResults_Options(),id='simulator-stopped-decision')
                    ],id='simulator-refresh-sub')
        return self.MenuTab(menu_data,graph_data,bottom_data)
    
    def ShowResults_Options(self):
        return ['What do you want to do now?']
    
    
    