# -*- coding: utf-8 -*-
"""
    Class managing simulation tab layout
"""

import dash_core_components as dcc
import dash_html_components as html
from .DashTabs import DashTabs
import numpy as np


class SimulationTab(DashTabs):
    def __init__(self, *args, **kwds):
        DashTabs.__init__(self, *args, **kwds)
        self.message_sim = []
        self.table_padding = '10px'
        self.save_clicks = 0
        self.launch_clicks = 0
        self.cancel_clicks = 0
        self.confirm_clicks = 0
    
    #%% Simulation tab -- Display management
    def ShowTab(self):
        if self.Optimizer.simulation_on:
            return self.Simulation_on_Tab()
        elif self.Optimizer.simulation_message:
            return self.Optimizer.ShowResults()
        else:
            graph_data = html.Div([
                    self.ShowMarketGraph(False),
                    ])
            bottom_data = ''#'oho'
            menu_data = self.Menu()
            return self.MenuTab(menu_data,graph_data,bottom_data)
    
    #%% Simulation tab -- Main  menu   
    def Menu(self):
        return html.Div(self.MenuRefresh(), id='simulation-menu-refresh')
    
    def MenuRefresh(self,refresh=None):
        return [html.Div(self.MenuFees(), id='simulation-menu-fees'),
                html.Div(self.MenuAlgorithm(), id='simulation-menu-algorithm'),
                html.Div(self.MenuComputation(), id='simulation-menu-computation'),
                html.Div(self.MenuVisual(), id='simulation-menu-visual'),
                html.Div(self.MenuLaunch(), id='simulation-menu-launch')]
    
    
    #%% Simulation tab -- Fees menu
    def MenuFees(self):
        return [html.Div([
                html.H4('General fees', title='In addition to preferences.'),
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Commission fees:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.RadioItems( id='simulation-menu-fees-addcomm', labelStyle={'display': 'block'}, 
                                                   value=self.Optimizer.Add_Commission_Fees,
                                                 options=[
                                                    {'label': 'Yes', 'value': 'Yes'},
                                                    {'label': 'No', 'value': 'No'},
                                                ])
                                    ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                            ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                html.Div(id='simulation-menu-fees-comm'),
                ])]
    
    def MenuFees_Commisions(self,add='No'):
        if add=='Yes':
            return [html.Div([
                        self.defaultTable,
                        html.Div([
                                html.Div(['P2P:'], style={'display':'table-cell'}, title='Common to all bilateral trades.'),
                                html.Div([
                                        dcc.Input( id='simulation-menu-fees-p2p', type='number', min=0, step=0.1,
                                                       value=self.Optimizer.Commission_Fees_P2P),
                                        ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                html.Div(['c$/kWh'], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        html.Div([
                                html.Div(['Community:'], style={'display':'table-cell'}, title='Common to all communities.'),
                                html.Div([
                                        dcc.Input( id='simulation-menu-fees-community', type='number', min=0, step=0.1,
                                                       value=self.Optimizer.Commission_Fees_Community),
                                        ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                html.Div(['c$/kWh'], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        ], style={'display':'table','width':'100%'}),
                    html.Div(id='simulation-menu-fees-comm-ans'),
                    ]
        else:
            return []
    
    def MenuFees_CommisionsUpdate(self,p2p=None,comm=None):
        if p2p is not None:
            self.Optimizer.Commission_Fees_P2P = max(p2p,0)
        if comm is not None:
            self.Optimizer.Commission_Fees_Community = max(comm,0)
        return
    
    
    #%% Simulation tab -- Algorithm  menu   
    def MenuAlgorithm(self):
        return [html.Div([
                html.H4('Algorithm'),
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Algorithm type:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.RadioItems( id='simulation-menu-algo-type',
                                                 labelStyle={'display': 'block'}, value=self.Optimizer.algorithm,
                                                 options=[
                                                    #{'label': 'Centralized', 'value': 'Centralized'},
                                                    {'label': 'Decentralized', 'value': 'Decentralized'},
                                                ])
                                    ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                            html.Div([], id='simulation-menu-algo-hidden', style={'display':'none'}),
                            ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='simulation-menu-parameters')
                ])]
    
    def MenuAlgorithm_Parameters(self,algo='Centralized'):
        self.Optimizer.algorithm = algo
        cells = [
                self.defaultTable,
                html.Div([
                        html.Div(['Maximum number of iterations:'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input( id='simulation-menu-maxit',
                                             type='number', step=250, min=1,
                                             value=self.Optimizer.maximum_iteration)
                                ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                        html.Div([], id='simulation-menu-parameters-hidden', style={'display':'none'}),
                        ], style={'display':'table-row'})
                ]
        
        if algo=='Decentralized':
            cells.extend([
                        html.Div([
                                html.Div(['Penalty factor:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='simulation-menu-penalty-factor',
                                                     type='number', min=0,
                                                     value=self.Optimizer.penaltyfactor)
                                        ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                    ], style={'display':'table-row'}),
                        html.Div([
                                html.Div(['Primal residual:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='simulation-menu-residual-primal',
                                                     type='number', min=0,
                                                     value=self.Optimizer.residual_primal)
                                        ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                    ], style={'display':'table-row'}),
                        html.Div([
                                html.Div(['Dual residual:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='simulation-menu-residual-dual',
                                                     type='number', min=0,
                                                     value=self.Optimizer.residual_dual)
                                        ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                    ], style={'display':'table-row'})
                    ])
        else:
            cells.extend([
                        html.Div([
                                html.Div(['Residual:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='simulation-menu-residual-primal',
                                                     type='number', min=0,
                                                     value=self.Optimizer.residual_primal)
                                        ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                    ], style={'display':'table-row'}),
                        html.Div([ dcc.Input( id='simulation-menu-penalty-factor', value=self.Optimizer.penaltyfactor) ], style={'display':'none'}),
                        html.Div([ dcc.Input( id='simulation-menu-residual-dual', value=self.Optimizer.residual_dual) ], style={'display':'none'})
                    ])
            
        return [html.Div([
                html.Div(cells, style={'display':'table','width':'100%'}),
                ])]
    
    def MenuAlgorithm_ParametersUpdate(self,maxit,penalty,primal,dual):
        self.Optimizer.maximum_iteration = int(maxit)
        self.Optimizer.penaltyfactor = float(penalty)
        self.Optimizer.residual_primal = float(primal)
        self.Optimizer.residual_dual = float(dual)
        return []
    
    
    #%% Simulation tab -- Computation  menu   
    def MenuComputation(self):
        return [html.Div([
                html.H4('Computation'),
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Target:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.RadioItems( id='simulation-menu-target', 
                                                 labelStyle={'display': 'block'}, value=self.Optimizer.target,
                                                 options=[
                                                    {'label': 'CPU', 'value': 'CPU'},
                                                    #{'label': 'GPU', 'value': 'GPU'},
                                                ])
                                    ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['Location:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.RadioItems( id='simulation-menu-location',
                                                 labelStyle={'display': 'block'}, value=self.Optimizer.location,
                                                 options=[
                                                    {'label': 'local', 'value': 'local'},
                                                    #{'label': 'external', 'value': 'external'},
                                                ])
                                    ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                            html.Div([], id='simulation-menu-computation-hidden', style={'display':'none'}),
                            ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='simulation-menu-external'),
                ])]
    
    def MenuComputation_External(self,location='local',target='CPU'):
        self.Optimizer.location = location
        self.Optimizer.target = target
        if location=='external':
            return [html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Account:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='simulation-menu-account', 
                                                 clearable=False, value=self.Optimizer.account,
                                                 options=[
                                                    {'label': 'Amazon Web Services', 'value': 'AWS'},
                                                    {'label': 'Microsoft Azure', 'value': 'Azure'},
                                                    {'label': 'Google Cloud', 'value': 'GCloud'},
                                                ])
                                    ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='simulation-menu-token-input')
                    ]
        else:
            return [html.Div([
                    dcc.Dropdown( id='simulation-menu-account', value=self.Optimizer.account),
                    dcc.Dropdown( id='simulation-menu-token', value=self.Optimizer.account_token)
                    ], style={'display':'none'})]
    
    def MenuComputation_Token(self,account='AWS'):
        self.Optimizer.account = account
        self.Optimizer.Registered_Token(account)
        return [html.Div([
                self.defaultTable,
                    html.Div([
                            html.Div(['Token account:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='simulation-menu-token', type='text', value=self.Optimizer.account_token)
                                    ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                            html.Div([], id='simulation-menu-token-hidden', style={'display':'none'}),
                            ], style={'display':'table-row'}),
                ], style={'display':'table','width':'100%'})]
    
    def MenuComputation_TokenUpdate(self,token=''):
        self.Optimizer.account_token = token
        return []
    
    
    #%% Simulation tab -- Visualization  menu   
    def MenuVisual(self):
        return [html.Div([
                html.H4('Visualization'),
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Display Progress:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.RadioItems( id='simulation-menu-show', labelStyle={'display': 'block'}, value=self.Optimizer.show,
                                                 options=[{'label':'Yes','value':True},
                                                          #{'label':'No','value':False}
                                                          ])
                                    ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='simulation-menu-show-progress')
                ])]
    
    def MenuVisual_Progress(self,show=True):
        self.Optimizer.show = show
        if show:
            return [html.Div([
                    self.defaultTable,
                        html.Div([
                                html.Div(['Level of detail:'], style={'display':'table-cell'}),
                                html.Div([
                                    dcc.RadioItems( id='simulation-menu-progress',
                                                 labelStyle={'display': 'block'}, value=self.Optimizer.progress,
                                                 options=[
                                                    {'label': 'Partial (iteration, time, ...)', 'value': 'Partial'},
                                                    {'label': 'Full (with graph plot)', 'value': 'Full'},
                                                ])
                                        ], style={'display':'table-cell','padding-bottom':self.table_padding}),
                                html.Div([], id='simulation-menu-progress-hidden', style={'display':'none'}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'})]
    
    def MenuVisual_ProgressUpdate(self,progress='Partial'):
        self.Optimizer.progress = progress
        return []
    
    
    #%% Simulation tab -- Launch  menu   
    def MenuLaunch(self):
        return [html.Div([
                html.Div([
                    html.Div([
                        html.Div([], style={'display':'table-cell','width':'30%','padding-top':'20px'}),
                        html.Div([], style={'display':'table-cell','width':'40%'}),
                        html.Div([], style={'display':'table-cell','width':'30%'}),
                    ], style={'display':'table-row'}),
                    html.Div([
                            html.Div([ html.Button(children='Save parameters', id = 'simulation-save-button', type='submit', n_clicks=self.save_clicks)
                                    ], style={'display':'table-cell'}),
                            html.Div([]),
                            html.Div([ html.Button(children='Run simulation', id = 'simulation-launch-button', type='submit', n_clicks=self.launch_clicks)
                                    ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='simulation-menu-launch-message')
                ])]
    
    def MenuLaunch_Message(self,save=None,launch=None):
        message = []
        if save is not None and save!=self.save_clicks:
            self.save_clicks = save
            out = self.Optimizer.Parameters_Save()
            message = [html.Div([], style={'padding-top':'10px'}), html.Hr() ]
            message.extend(out)
        elif launch is not None and launch!=self.launch_clicks:
            self.launch_clicks = launch
            self.Optimizer.LoadMGraph(self.MGraph)
            test, out = self.Optimizer.Parameters_Test()
            if test:
                message = [
                        html.Div([], style={'padding-top':'10px'}),
                        html.Hr(),
                        html.Div([dcc.Markdown('**Do you confirm the simulation?**')]),
                        html.Div([dcc.Markdown('*Note: This action will block control on the rest of the application.*')]),
                        html.Div([
                            html.Div([
                                html.Div([], style={'display':'table-cell','width':'20%','padding-top':'5px'}),
                                html.Div([], style={'display':'table-cell','width':'30%'}),
                                html.Div([], style={'display':'table-cell','width':'20%'}),
                                html.Div([], style={'display':'table-cell','width':'30%'}),
                            ], style={'display':'table-row'}),
                            html.Div([
                                    html.Div([], style={'display':'table-cell'}),
                                    html.Div([ 
                                            html.Button(children='Cancel', id = 'simulation-launch-cancel', type='submit', n_clicks=self.cancel_clicks)
                                            ], style={'display':'table-cell'}),
                                    html.Div([], style={'display':'table-cell'}),
                                    html.Div([ 
                                            html.Button(children='Confirm', id = 'simulation-launch-confirm', type='submit', n_clicks=self.confirm_clicks)
                                            ], style={'display':'table-cell'})
                                    ], style={'display':'table-row'}),
                        ], style={'display':'table','width':'100%'}),
                        html.Div([],id='simulation-menu-confirm-message')
                        ]
            else:
                message = [html.Div([], style={'padding-top':'10px'}), html.Hr() ]
                message.extend(out)
        return message
    
    def MenuLaunch_MessageConfirm(self,cancel=None,confirm=None):
        if confirm is not None and confirm!=self.confirm_clicks:
            self.confirm_clicks = confirm
            self.Optimizer.simulation_on = True
            return self.Simulation_on_Tab()
        elif cancel is not None and cancel!=self.cancel_clicks:
            self.cancel_clicks = cancel
            self.Optimizer.simulation_on = False
            return html.Div([html.Button(children='', id = 'simulation-menu-refresh-trigger', type='submit', n_clicks=self.cancel_clicks)],style={'display':'none'})
        else:
            return []

