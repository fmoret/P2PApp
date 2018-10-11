# -*- coding: utf-8 -*-
"""
    Class managing market network tab layout
"""

import dash_core_components as dcc
import dash_html_components as html
from .MGraph import MGraph
from .DashTabs import DashTabs
import os
import pandas as pd
import numpy as np
import copy


class MarketTab(DashTabs):
    def __init__(self, *args, **kwds):
        DashTabs.__init__(self, *args, **kwds)
        self.init_DefaultMarketOptions()
        self.init_DefaultFilename()
        self.current_filename = self.default_filename
        # Default menu plot parameters
        self.market_topmenu_add = 'Add'
        self.market_topmenu_second = 'Agent'
        self.market_topmenu_third = ''
        # State variables
        self.update_graph = False
        self.state_market_tab = 0 #Unused
        self.total_clicks = 0
        self.maxID = 0
        self.clicks_delete_confirm = 0
        self.clicks_delete_cancel = 0
        self.clicks_save = 0
        # Info on current working agent
        self.AgentName = 'Agent' + ' ' + str(self.maxID)
        self.CommID = 0
        self.AgentID = 0
        self.AssetID = 0
    
    def init_DefaultMarketOptions(self):
        self.allow_P2P_with_both_communitymanager_and_its_members = True
        self.allow_P2P_within_community = True
        self.default_partnership_preference = 0
        self.default_community_preference = 0
        self.default_community_size = 3
        #self.color_dict_ag = {'Manager':'green','Agent':'blue','Asset':'black'}
        #self.color_dict_conn = {'Alone':'red','Connected':'blue'}
        self.default_asset = {'name':'Asset 1', 'id':0, 'type':'Load',
                              'costfct':'Quadratic', 'costfct_coeff':[0,0,0],
                              'longitude':0, 'latitude':0, 'bus':0,
                              'p_bounds_up':0, 'p_bounds_low':0, 'q_bounds_up':0, 'q_bounds_low':0}
        self.community_goal_options = ['Lowest Price','Lowest Importation']#,'Autonomy','Peak Shaving']
        self.assets_type = ['Appliances','Store','Flats','Stores','Factory','Solar','Wind','Fossil']
        self.assets_type_shortcut = {'App':'Appliances','Fact':'Factory','House':'Appliances'}
        self.default_preference_threshold = 100
    
    def init_DefaultFilename(self):
        n_start = 0
        self.default_dirpath_examples = 'graphs/examples'
        self.default_dirpath = 'graphs/saved'
        self.current_dirpath = self.default_dirpath
        #self.default_dirpath_absolute = os.path.abspath(self.default_dirpath)
        for file in os.listdir(self.default_dirpath):
            if file.endswith(".pyp2p") and len(file)>10:
                if file[0:4]=='P2P_' and file[4:-6].isdigit():
                    n_start = max(int(file[4:-6])+1, n_start)
        self.default_filename = 'P2P_' + str(n_start) + '.pyp2p'
    
    
    #%% Market tab -- Display management
    def ShowTab(self):
        if self.Optimizer.simulation_on:
            return self.Simulation_on_Tab()
        elif self.Optimizer.simulation_message:
            return self.Optimizer.ShowResults()
        else:
            graph_data = html.Div([
                    self.ShowMarketGraph(True,True),
                    ])
            bottom_data = ''#'oho'
            menu_data = html.Div([self.TopMenu(),
                        html.Div([],id='market-menu')])
            return self.MenuTab(menu_data,graph_data,bottom_data)
    
    #%% Market tab -- Top menu   
    def TopMenu(self):
        self.state_market_tab = 1
        return html.Div([
                html.Div(['Actions:']),
                html.Div([
                    html.Div([dcc.Dropdown( id='market-topmenu-insert',
                            options=[
                                    {'label': 'Add', 'value': 'Add'},
                                    {'label': 'Modify', 'value': 'Change'},
                                    {'label': 'Delete', 'value': 'Delete'},
                                    {'label': 'Save', 'value': 'Save'},
                                    {'label': 'Open', 'value': 'Open'}
                                ], value=self.market_topmenu_add, clearable=False)
                            ],style={'display': 'table-cell', 'width': '20%'}
                            ),
                    html.Div([], id='market-topmenu-void1', style={'display': 'table-cell', 'width': '2%'}),
                    html.Div([self.TopMenu_Insert()
                            ], id='market-topmenu-second', style={'display': 'table-cell', 'width': '32%'}),
                    html.Div([], id='market-topmenu-void2', style={'display': 'table-cell', 'width': '2%'}),
                    html.Div([self.TopMenu_Number()], id='market-topmenu-third', style={'display': 'table-cell', 'width': '32%'}),
                    html.Div([], id='market-topmenu-void3', style={'display': 'table-cell', 'width': '2%'}),
                    html.Div([
                            html.Button(children='Select', id = 'add-button', type='submit', n_clicks=self.total_clicks)
                            ], id='test', style={'display': 'table-cell', 'width': '10%'})
                    ], id='market-topmenu', style={'display': 'table', 'width': '100%'}),
                    html.Hr()
                ])
    
    def TopMenu_Insert(self,insert_value=None):
        if insert_value is None:
            insert_value = self.market_topmenu_add
        else:
            self.market_topmenu_add = insert_value
        out_val = self.market_topmenu_second
        out_disp = {'display':'block'}
        if insert_value=='Add':
            out_opt=[
                        {'label': 'Agent', 'value': 'Agent'},
                        {'label': 'Community', 'value': 'Community'},
                        {'label': 'Link (soon)', 'value': 'Link'},
                        {'label': 'From example', 'value': 'Example'},
                        {'label': 'From File', 'value': 'File'},
                    ]
        elif insert_value=='Change' or insert_value=='Delete':
            out_opt=[
                        {'label': 'Agent/Community', 'value': 'Agent/Community'},
                        {'label': 'Link', 'value': 'Link'},
                    ]
        elif insert_value=='Save':
            out_opt=[
                        {'label': 'Save', 'value': 'Save'},
                        {'label': 'Save as', 'value': 'Save as'},
                    ]
            out_val='Save'
        elif insert_value=='Open':
            out_opt=[
                        {'label': 'New', 'value': 'New'},
                        {'label': 'From example', 'value': 'Example'},
                        {'label': 'From File', 'value': 'File'},
                    ]
        else:
            out_opt = []
            out_val = None
            out_disp = {'display':'none'}
        return html.Div([dcc.Dropdown( id='market-topmenu-second-drop', options=out_opt, value=out_val, clearable=False)],style=out_disp)
    
    def TopMenu_Number(self,example_value=None,add_value=None):
        if example_value is None:
            example_value = self.market_topmenu_second
        else:
            self.market_topmenu_second = example_value
        if add_value is None:
            add_value = self.market_topmenu_add
        else:
            self.market_topmenu_add = add_value
        if add_value=='Add' and example_value=='Community':
            return html.Div([dcc.Input( id='market-topmenu-third-number', type='number', step=1, min=1, value=self.default_community_size)])
        elif add_value=='Delete' and example_value=='Agent/Community':
            return html.Div([dcc.Dropdown(id='market-topmenu-third-number')], style={'display':'none'})
        elif add_value=='Change' and example_value=='Agent/Community':
            return html.Div([
                    dcc.Dropdown( id='market-topmenu-third-number',
                                 options=[{'label':x['name'],'value':x.index} for x in self.MGraph.vs], 
                                 value=self.market_topmenu_third,
                                 clearable=False)
                    ])
        else:
            return html.Div([dcc.Input( id='market-topmenu-third-number', type='number', step=1, min=1, value=0)], style={'display':'none'})
    
    #%% Market tab -- Main menu
    def Menu(self,n_clicks,add_value,example_value,size_value):
        self.state_market_tab = 2
        if self.total_clicks != n_clicks:
            self.total_clicks = n_clicks
            self.update_graph = True
        else:
            self.update_graph = False
        
        if add_value=='Save':
            return self.Menu_Save(example_value)
        elif add_value=='Add':
            if example_value=='Agent':
                self.CreateAgent()
                return self.Menu_Agent()
            elif example_value=='Community':
                self.CreateCommunity(size_value)
                return self.Menu_Community()
            elif example_value=='Example':
                return self.Menu_AddFile()
            elif example_value=='File':
                return self.Menu_AddFile()
            elif example_value=='Link':
                return self.Menu_Link(add_value)
            else:
                return 
        elif add_value=='Open':
            if example_value=='Example':
                return self.Menu_AddFile()
            elif example_value=='File':
                return self.Menu_AddFile()
            elif example_value=='New':
                return self.Menu_AddFile()
            else:
                return 
        else:
            if example_value=='Agent/Community':
                if add_value=='Delete':
                    return self.Menu_Delete()
                else:
                    self.AgentID = size_value
                    self.AgentName = self.MGraph.vs[self.AgentID]['name']
                    return self.Menu_Agent()
            elif example_value=='Link':
                return self.Menu_Link(add_value)
            else:
                return 
    
    def Menu_Preferences(self,idx=None):
        if idx is None:
            idx = self.AgentID
        return ','.join(str(x) for x in self.MGraph.vs[idx]['Preferences'])
    
    def Menu_CommPref(self):
        return ','.join(str(x) for x in self.MGraph.vs[self.AgentID]['CommPref'])
    
    #%% Market tab -- Agent menu
    def Menu_Agent(self):
#        if len(self.MGraph.vs)>self.AgentID:
#            val = self.MGraph.vs[self.AgentID]['Type']
#        else:
#            val=None
        return html.Div([
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Agent type:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-type',
                                                 clearable=False,
                                                 options=[
                                                    {'label': 'Agent', 'value': 'Agent'},
                                                    {'label': 'Community Manager', 'value': 'Manager'},
                                                    #{'label': 'Grid', 'value': 'Grid'}
                                                ], value=self.MGraph.vs[self.AgentID]['Type'])
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}),
                            html.Div([
                                    html.Button(children='Refresh', id = 'agent-refresh-button', type='submit')
                                    ], style={'display':'table-cell'}, id='market-menu-agent-type-void'),
                                ], style={'display':'table-row'})
                        ], style={'display':'table','width':'100%'}),
                html.Div(self.Menu_AgentRefresh(), id='market-menu-agent-refresh')
                ])
    
    def Menu_AgentRefresh(self,click=None):
        return html.Div([], style={'display':'table','width':'100%'},id='market-menu-agent-data')
    
    def Menu_AgentData(self):
        if self.MGraph.vs[self.AgentID]['Type']=='Manager':
            Ag_name = 'Community name:'
            Comm_name = 'Community members:'
            min_ass = 0
            max_ass = 0
            self.MGraph.vs[self.AgentID]['AssetsNum'] = 0
            styl_goal = {'display':'table-row'}
            styl_ass = {'display':'none'}
        else:
            Ag_name = 'Agent name:'
            Comm_name = 'Community membership:'
            if self.MGraph.vs[self.AgentID]['AssetsNum'] == 0:
                self.MGraph.vs[self.AgentID]['AssetsNum'] = 1
            min_ass = 1
            max_ass = None
            styl_goal = {'display':'none'}
            styl_ass = {'display':'table-row'}
        styl_impfee = {'display':'none'}
        AllowedPart = self.ListAllowedPartners()
        for x in self.MGraph.vs[self.AgentID]['Partners']:
            for ids in self.MGraph.vs.select(ID=x):
                AllowedPart.append(ids.index)
        AllowedComm = self.ListAllowedCommunities()
        return [
                html.Div([self.defaultTable,
                    html.Div([
                            html.Div([Ag_name], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-name', value=self.MGraph.vs[self.AgentID]['name'], type='text', style={'width':'99%'})
                                    ], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['Community objective:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-commgoal', 
                                                 clearable=False,
                                                 options=[{'label':x,'value':x} for x in self.community_goal_options], 
                                                value=self.MGraph.vs[self.AgentID]['CommGoal'])
                                    ], style={'display':'table-cell'}),
                            ], style=styl_goal),
                    html.Div([
                            html.Div(['Importation fee:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-impfee', type='number', min=0, step=0.01, value=self.MGraph.vs[self.AgentID]['ImpFee'], style={'width':'99%'})
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}),
                            html.Div([' $/kWh'], style={'display':'table-cell'}),
                            ], style=styl_impfee, id='market-menu-agent-impfee-show'),
                    html.Div([
                            html.Div(['Trading partners:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-partners',
                                                 options=[{'label':self.MGraph.vs[i]['name'],'value':self.MGraph.vs[i]['ID']} for i in AllowedPart], 
                                                multi=True,
                                                value=self.MGraph.vs[self.AgentID]['Partners'])
                                    ], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['Preferences:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-preferences', type='text', style={'width':'99%'},
                                              value=self.Menu_Preferences())
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}, id='market-menu-agent-preferences-void'),
                            ], style={'display':'table-row'}, id='market-menu-agent-prefDiv'),
                    html.Div([
                            html.Div([Comm_name], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-community',
                                                 options=[{'label':self.MGraph.vs[i]['name'],'value':self.MGraph.vs[i]['ID']} for i in AllowedComm], 
                                                multi=True,
                                                value=self.MGraph.vs[self.AgentID]['Community'])
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}, id='market-menu-agent-community-void'),
                            ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['Community preference:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-commpref', type='text', style={'width':'99%'},
                                              value=self.Menu_CommPref())
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}, id='market-menu-agent-commpref-void'),
                            ], style={'display':'table-row'}, id='market-menu-agent-commprefDiv'),
                    html.Div([
                            html.Div(['Number of assets:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-number-assets', 
                                              value=self.MGraph.vs[self.AgentID]['AssetsNum'], 
                                              type='number', step=1, min=min_ass, max=max_ass, style={'width':'99%'})
                                    ], style={'display':'table-cell'}),
                            ], style=styl_ass),
                ], style={'display':'table','width':'100%'}),
                html.Div([], id='market-menu-assets'),
                ]
    
    #%% Market tab -- Link menus
    def Menu_Link(self,add_value='Add'):
        return html.Div(self.Menu_LinkRefresh(add_value), id='market-menu-link-refresh')
    
    def Menu_LinkRefresh(self,add_value='Add'):
        return [
                html.Div([self.defaultTable,
                    html.Div([
                            html.Div(['Type of link:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown(id='market-menu-link-type', clearable=False, className=add_value,
                                                 options=[
                                                         {'label':'Partnership','value':'Partnership'},
                                                         {'label':'Community membership','value':'Membership'},
                                                         ])
                                    ], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                ], style={'display':'table','width':'100%'}),
                html.Div([], id='market-menu-link'),
                ]
    
    def Menu_LinkWho(self,link_type):
        if link_type=='Partnership':
            return [
                    html.Div([self.defaultTable,
                        html.Div([
                                html.Div(['Between:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Dropdown(id='market-menu-link-who', clearable=False,
                                                     options=[{'label':x['name'],'value':x.index} for x in self.MGraph.vs])
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='market-menu-link2'),
                    ]
        elif link_type=='Membership':
            return [
                    html.Div([self.defaultTable,
                        html.Div([
                                html.Div(['Agent/Manager:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Dropdown(id='market-menu-link-who', clearable=False,
                                                     options=[{'label':x['name'],'value':x.index} for x in self.MGraph.vs])
                                                     #options=[{'label':x['name'],'value':x.index} for x in self.MGraph.vs.select(Type_ne='Manager')])
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='market-menu-link2'),
                    ]
    
    def Menu_LinkWith(self,who=None,link_type=None,add_value=None):
        if who!=None and link_type!=None and add_value!=None:
            if link_type=='Partnership':
                if add_value=='Add':
                    AllowedPart = self.ListAllowedPartners(who)
                else:
                    AllowedPart = []
                    for ids in self.MGraph.vs[who]['Partners']:
                        for x in self.MGraph.vs.select(ID=ids):
                            AllowedPart.append(x.index)
                return [
                        html.Div([self.defaultTable,
                            html.Div([
                                    html.Div(['And:'], style={'display':'table-cell'}),
                                    html.Div([
                                            dcc.Dropdown(id='market-menu-link-with', clearable=False, value=None,
                                                         options=[{'label':self.MGraph.vs[i]['name'],'value':i} for i in AllowedPart])
                                            ], style={'display':'table-cell'}),
                                    ], style={'display':'table-row'}),
                        ], style={'display':'table','width':'100%'}),
                        html.Div(['electro'], id='market-menu-link-prefs'),
                        ]
            elif link_type=='Membership':
                if add_value=='Add':
                    AllowedComm = self.ListAllowedCommunities(who)
                else:
                    AllowedComm = []
                    for ids in self.MGraph.vs[who]['Community']:
                        for x in self.MGraph.vs.select(ID=ids):
                            AllowedComm.append(x.index)
                    if self.MGraph.vs[who]['Type']=='Manager':
                        txt = 'Member:'
                    elif self.MGraph.vs[who]['Type']=='Agent':
                        txt = 'Community:'
                    else:
                        txt = ''
                return [
                        html.Div([self.defaultTable,
                            html.Div([
                                    html.Div([txt], style={'display':'table-cell'}),
                                    html.Div([
                                            dcc.Dropdown(id='market-menu-link-with', clearable=False, value=None,
                                                         options=[{'label':self.MGraph.vs[i]['name'],'value':i} for i in AllowedComm])
                                            ], style={'display':'table-cell'}),
                                    ], style={'display':'table-row'}),
                        ], style={'display':'table','width':'100%'}),
                        html.Div(['rap'], id='market-menu-link-prefs'),
                        ]
    
    def Menu_LinkPrefs(self,who1,who2,link_type,add_value):
        if who2!=None and who1!=None and link_type!=None and add_value!=None:
            button=[]
            inp1=[]
            inp2=[]
            if add_value=='Delete':
                button = [html.Button(children='Delete', id = 'market-menu-link-confirm-button', type='submit', n_clicks=self.clicks_save)]
                inp1=[html.Div([ dcc.Input(id='market-menu-link-pref1', type='number', value=None) ], style={'display':'none'})]
                inp2=[html.Div([ dcc.Input(id='market-menu-link-pref2', type='number', value=None) ], style={'display':'none'})]
            else:
                on = False
                if link_type=='Partnership':
                    on = True
                    message = 'Preference of '
                    if add_value=='Change':
                        valnum1 = self.MGraph.vs[who1]['Preferences'][ self.MGraph.vs[who1]['Partners'].index(self.MGraph.vs[who2]['ID']) ]
                        valnum2 = self.MGraph.vs[who2]['Preferences'][ self.MGraph.vs[who2]['Partners'].index(self.MGraph.vs[who1]['ID']) ]
                    else:
                        valnum1 = self.default_partnership_preference
                        valnum2 = valnum1
                elif link_type=='Membership':
                    on = True
                    message = 'Community preference of '
                    if add_value=='Change':
                        valnum1 = self.MGraph.vs[who1]['CommPref'][ self.MGraph.vs[who1]['Community'].index(self.MGraph.vs[who2]['ID']) ]
                        valnum2 = self.MGraph.vs[who2]['CommPref'][ self.MGraph.vs[who2]['Community'].index(self.MGraph.vs[who1]['ID']) ]
                    else:
                        valnum1 = self.default_community_preference
                        valnum2 = valnum1
                if on:
                    inp1=[html.Div([ message+self.MGraph.vs[who1]['name'] ], style={'display':'table-cell'}),
                          html.Div([ dcc.Input(id='market-menu-link-pref1', type='number', value=float(valnum1)) ], style={'display':'table-cell'})]
                    inp2=[html.Div([ message+self.MGraph.vs[who2]['name'] ], style={'display':'table-cell'}),
                          html.Div([ dcc.Input(id='market-menu-link-pref2', type='number', value=float(valnum2)) ], style={'display':'table-cell'})]
                    if add_value=='Add':
                        button = [html.Button(children='Add', id = 'market-menu-link-confirm-button', type='submit', n_clicks=self.clicks_save)]
                    elif add_value=='Change':
                        button = [html.Button(children='Change', id = 'market-menu-link-confirm-button', type='submit', n_clicks=self.clicks_save)]
            return [
                    html.Div([self.defaultTable,
                        html.Div(inp1, style={'display':'table-row'}),
                        html.Div(inp2, style={'display':'table-row'}),
                        html.Div([
                                html.Div([], style={'display':'table-cell'}),
                                html.Div([], style={'display':'table-cell'}),
                                html.Div([], style={'display':'table-cell'}),
                                html.Div(button, style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='market-menu-link-refresh-trigger', style={'display':'none'}),
                    ]
            
    def Menu_LinkConfirmed(self,n_confirm,who1,who2,pref1,pref2,link_type,add_value):
        if self.clicks_save != n_confirm:
            self.clicks_save = n_confirm
            if who1!=None and who2!=None and link_type!=None and add_value!=None:
                on = False
                if add_value=='Delete':
                    on = self.LinkDelete(link_type,who1,who2)
                elif add_value=='Change' and pref1!=None and pref2!=None:
                    on = self.LinkChange(link_type,who1,who2,pref1,pref2)
                elif add_value=='Add' and pref1!=None and pref2!=None:
                    on = self.LinkAdd(link_type,who1,who2,pref1,pref2)
                if on:
                    print('Action not implemented yet! ;P')
                    return html.Button(children='', id ='market-menu-link-refresh-button', type='submit', n_clicks=1)
    
    #%% Market tab -- Community menu
    def Menu_Community(self):
        return [html.Div([self.defaultTable,
                html.Div([
                        html.Div(['Community name:'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input( id='market-menu-community-name', value=self.MGraph.vs[self.AgentID]['name'], type='text', style={'width':'99%'})
                                ], style={'display':'table-cell'}),
                        html.Div([html.Button(children='Refresh', id = 'community-refresh-button', type='submit')], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                html.Div(self.Menu_CommunityRefresh(), id='market-menu-community-refresh')]
    
    def Menu_CommunityRefresh(self,click=None):
        AllowedPart = self.ListAllowedPartners()
        return html.Div([self.defaultTable,
                html.Div([
                    html.Div(['Community objective:'], style={'display':'table-cell'}),
                    html.Div([
                            dcc.Dropdown( id='market-menu-community-commgoal', 
                                         clearable=False,
                                         options=[{'label':x,'value':x} for x in self.community_goal_options], 
                                        value=self.MGraph.vs[self.AgentID]['CommGoal'])
                            ], style={'display':'table-cell'}),
                    ], style={'display':'table-row'}),
                html.Div([
                        html.Div(['Trading partners:'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Dropdown( id='market-menu-community-partners',
                                             options=[{'label':self.MGraph.vs[i]['name'],'value':self.MGraph.vs[i]['ID']} for i in AllowedPart], 
                                            multi=True,
                                            value=self.MGraph.vs[self.AgentID]['Partners'])
                                ], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                html.Div([
                        html.Div(['Preferences:'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input( id='market-menu-community-preferences', type='text', style={'width':'99%'},
                                          value=self.Menu_Preferences())
                                ], style={'display':'table-cell'}),
                        html.Div([], style={'display':'table-cell'}, id='market-menu-community-preferences-void'),
                        ], style={'display':'table-row'}, id='market-menu-community-prefDiv'),
                html.Div([
                        html.Div(['Community members'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input( id='market-menu-community-members', style={'width':'99%'},
                                            value=','.join([self.MGraph.vs.select(ID=x)['name'][0] for x in self.MGraph.vs[self.AgentID]['Community']]))
                                ], style={'display':'table-cell'}),
                        html.Div([], style={'display':'table-cell'}, id='market-menu-community-members-void'),
                        ], style={'display':'table-row'}),
            ], style={'display':'table','width':'100%'})
    
    #%% Market tab -- Delete menu
    def Menu_Delete(self):
        return html.Div(self.Menu_DeleteRefresh(), id='market-menu-delete-refresh')
    
    def Menu_DeleteRefresh(self,del_select=None):
        return [
                html.Div([
                    html.Div([
                        html.Div([], style={'display':'table-cell','width':'40%'}),
                        html.Div([], style={'display':'table-cell','width':'40%'}),
                        html.Div([], style={'display':'table-cell','width':'20%'}),
                    ], style={'display':'table-row'}),
                    html.Div([
                        html.Div(['Which agent do you want to delete?'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Dropdown( id='market-menu-delete-select', value=None,
                                             options=[{'label': x['name'] , 'value': x.index} for x in self.MGraph.vs])
                                ], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                    html.Div([], style={'display':'table-row'}, id='market-menu-delete-type'),
                 ], style={'display':'table','width':'100%'}),
                 html.Div([], id='market-menu-delete-assets'),
                 html.Div([], id='market-menu-delete-message'),
                 html.Div([
                         html.Div([
                            html.Div([
                                html.Div([], style={'display':'table-cell','width':'15%'}),
                                html.Div([], style={'display':'table-cell','width':'15%'}),
                                html.Div([], style={'display':'table-cell','width':'70%'}),
                            ], style={'display':'table-row'}),
                            html.Div([
                                html.Div([html.Button(children='Delete', id = 'market-menu-delete-confirm-button', type='submit', n_clicks=self.clicks_delete_confirm)], style={'display':'table-cell'}),
                                html.Div([html.Button(children='Cancel', id = 'market-menu-delete-cancel-button', type='submit', n_clicks=self.clicks_delete_cancel)], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                         ], style={'display':'table','width':'100%'})
                    ], id='market-menu-delete-confirm-buttons',style={'display':'none'}),
                ]
    
    def Menu_DeleteType(self,Selected_Index=None):
        if Selected_Index != None:
            self.AgentID = Selected_Index
            if self.MGraph.vs[self.AgentID]['Type']=='Agent':
                return [html.Div(['What do you want to delete?'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Dropdown( id='market-menu-delete-select-type',
                                             options=[{'label': 'The agent' , 'value': 'Agent'},
                                                     {'label': 'Some of its assets' , 'value': 'Assets'}], 
                                            value=None)
                                ], style={'display':'table-cell'}),
                        ]
            elif self.MGraph.vs[self.AgentID]['Type']=='Manager':
                return [html.Div(['What do you want to delete?'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Dropdown( id='market-menu-delete-select-type',
                                             options=[{'label': 'All community' , 'value': 'Community'},
                                                     {'label': 'Only the manager' , 'value': 'Manager'}], 
                                            value=None)
                                ], style={'display':'table-cell'}),
                        ]
            else:
                return []
        else:
            return []
    
    def Menu_DeleteAssets(self,Selected_Type=None):
        if Selected_Type != None:
            if self.MGraph.vs[self.AgentID]['Type']=='Agent' and Selected_Type=='Assets':
                return [html.Div([
                            html.Div([
                                html.Div([], style={'display':'table-cell','width':'40%'}),
                                html.Div([], style={'display':'table-cell','width':'40%'}),
                                html.Div([], style={'display':'table-cell','width':'20%'}),
                            ], style={'display':'table-row'}),
                            html.Div([
                                html.Div(['Which assets do you want to delete?'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Dropdown( id='market-menu-delete-select-asset',
                                         options=[{'label':self.MGraph.vs[self.AgentID]['Assets'][i]['name'],'value':i} for i in range(int(self.MGraph.vs[self.AgentID]['AssetsNum']))], 
                                         multi=True,value=[])
                                ], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                         ], style={'display':'table','width':'100%'}),
                        ]
            else:
                return [html.Div([
                            dcc.Dropdown(id='market-menu-delete-select-asset',
                                     options=[{'label':Selected_Type,'value':Selected_Type}], value=Selected_Type,clearable=False)
                                ], style={'display':'none'}),
                        ]
        else:
            return []
    
    def Menu_DeleteWarning(self,Selected_Assets=None,Selected_Type=None):
        if Selected_Assets != None:
            message = []
            if isinstance(Selected_Assets,str) and Selected_Type!='Assets':
                if Selected_Type=='Agent':
                    message= [
                            html.Div([dcc.Markdown('**This action will delete the agent and all its assets!**')]),
                            html.Div(["Do you confirm the suppresion of agent '"+self.MGraph.vs[self.AgentID]['name']+"'?"])
                            ]
                elif Selected_Type=='Manager':
                    message= [
                            html.Div([dcc.Markdown('*Note that only the community manager will be deleted, other agents in the community will not be affected.*')]),
                            html.Div(["Do you confirm the suppresion of community manager '"+self.MGraph.vs[self.AgentID]['name']+"'?"])
                            ]
                elif Selected_Type=='Community':
                    message= [
                            html.Div([dcc.Markdown('**This action will delete all direct members of this community!**')]),
                            html.Div(["Do you confirm the suppresion of the community '"+self.MGraph.vs[self.AgentID]['name']+"'?"])
                            ]
            elif isinstance(Selected_Assets,list) and len(Selected_Assets)!=0 and Selected_Type=='Assets':
                length = len(Selected_Assets)-1
                list_assets = ""
                for i in range(length):
                    list_assets += "'"+ self.MGraph.vs[self.AgentID]['Assets'][Selected_Assets[i]]['name'] +"',"
                list_assets += "'"+ self.MGraph.vs[self.AgentID]['Assets'][Selected_Assets[length]]['name'] +"'"
                if length>0:
                    message= [
                            html.Div([dcc.Markdown('*Note that only the selected assets will be deleted, other assets will not be affected.*')]),
                            html.Div(["Do you confirm the suppresion of assets "+list_assets+" of agent "+self.MGraph.vs[self.AgentID]['name']+"?"])
                            ]
                else:
                    message= [
                            html.Div([dcc.Markdown('*Note that only the selected assets will be deleted, other assets will not be affected.*')]),
                            html.Div(["Do you confirm the suppresion of asset "+list_assets+" of agent "+self.MGraph.vs[self.AgentID]['name']+"?"])
                            ]
            if message!=[]:
                message.append(html.Div(html.Button(children='block', id ='market-menu-delete-show-confirm-button', type='submit', n_clicks=1), style={'display':'none'}))
                return html.Div(message)
            else:
                return [html.Div(html.Button(children='none', id ='market-menu-delete-show-confirm-button', type='submit', n_clicks=1), style={'display':'none'})]
        else:
            return [html.Div(html.Button(children='none', id ='market-menu-delete-show-confirm-button', type='submit', n_clicks=1), style={'display':'none'})]
    
    def Menu_DeleteConfirmed(self,n_cancel,n_confirm,delete_type=None,delete_asset=None):
        if self.clicks_delete_confirm != n_confirm:
            self.clicks_delete_confirm = n_confirm
            
            if delete_type=='Assets':
                length = len(delete_asset)-1
                list_assets = ""
                for i in range(length):
                    list_assets += "'"+ self.MGraph.vs[self.AgentID]['Assets'][delete_asset[i]]['name'] +"',"
                list_assets += "'"+ self.MGraph.vs[self.AgentID]['Assets'][delete_asset[length]]['name'] +"'"
                self.DeleteAssets(delete_asset)
                if length>0:
                    return ["Assets "+list_assets+" have been deleted"]
                else:
                    return ["Asset "+list_assets+" has been deleted"]
            elif delete_type=='Agent':
                message = ["Agent '"+self.MGraph.vs[self.AgentID]['name']+"' has been deleted"]
                self.DeleteAgent()
                return message
            elif delete_type=='Manager':
                message = ["Community mannager '"+self.MGraph.vs[self.AgentID]['name']+"' has been deleted"]
                self.DeleteAgent()
                return message
            elif delete_type=='Community':
                message = ["Community '"+self.MGraph.vs[self.AgentID]['name']+"' has been deleted"]
                self.DeleteCommunity()
                return message
            else:
                return []#['Confirm ',str(delete_type),' ',str(delete_asset)]
        elif self.clicks_delete_cancel != n_cancel:
            self.clicks_delete_cancel = n_cancel
            return []
        else:
            return [self.Menu_DeleteRefresh()]
    
    def Menu_DeleteShowConfirmed(self,show_disp):
        return {'display':show_disp}
    
    #%% Market tab -- Assets menu
    def ShowAssetsMenu(self):
        if self.AssetID >= int(self.MGraph.vs[self.AgentID]['AssetsNum']):
            self.AssetID = int(self.MGraph.vs[self.AgentID]['AssetsNum'])-1
        return html.Div([
                html.Div([
                    dcc.Tabs(
                            children=[
                                    dcc.Tab(label='Asset n° {}'.format(i+1), value=i) 
                                        for i in range(int(self.MGraph.vs[self.AgentID]['AssetsNum']))
                                    ],
                            value=self.AssetID,
                            id='tab-assets',
                            vertical=True,
                        )],
                    style={'width': '20%', 'float': 'left'}),
                html.Div(id='tab-assets-output',style={'width': '80%', 'float': 'right'})
                ], style={
                    'width': '100%',
                    'fontFamily': 'Sans-Serif',
                    'margin-left': 'auto',
                    'margin-right': 'auto'
                })
    
    def ShowAssetMenu(self,asset_tab_id):
        if int(self.MGraph.vs[self.AgentID]['AssetsNum'])==0:
            return []
        else:
            if isinstance(asset_tab_id,str):
                if asset_tab_id=='tab-1':
                    asset_tab_id = 0
                else:
                    asset_tab_id = int(asset_tab_id)
            Asset_dict = self.MGraph.vs[self.AgentID]['Assets'][asset_tab_id]
            self.AssetID = asset_tab_id
            return html.Div([
                    html.Div([
                        html.Div([
                                html.Div([], style={'display':'table-cell','width':'3%'}),
                                html.Div([], style={'display':'table-cell','width':'42%'}),
                                html.Div([], style={'display':'table-cell','width':'40%'}),
                                html.Div([], style={'display':'table-cell','width':'15%'}),
                                ], style={'display':'table-row'}),
                        html.Div([
                                html.Div([], style={'display':'table-cell'}),
                                html.Div(['Asset name:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='market-menu-asset-name', value=Asset_dict['name'], type='text', style={'width':'98%'})
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        html.Div([
                                html.Div([], style={'display':'table-cell'}),
                                html.Div(['Asset type:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Dropdown( id='market-menu-asset-type', clearable=False,
                                                     options=[{'label': x, 'value': x} for x in self.assets_type], 
                                                    value=Asset_dict['type'])
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        html.Div([
                                html.Div([], style={'display':'table-cell'}),
                                html.Div(['Cost function type:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Dropdown( id='market-menu-asset-costfct', clearable=False,
                                                     options=[
                                                        {'label': 'Quadratic', 'value': 'Quadratic'},
                                                    ], 
                                                    value=Asset_dict['costfct'])
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        html.Div([
                                html.Div([], style={'display':'table-cell'}),
                                html.Div(['Cost function coefficients:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='market-menu-asset-costfct_coeff', value=','.join(str(x) for x in Asset_dict['costfct_coeff']), type='text', style={'width':'98%'})
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        html.Div([
                                html.Div([], style={'display':'table-cell'}),
                                html.Div(['Upper bound:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='market-menu-asset-p_bounds_up', value=Asset_dict['p_bounds_up'], type='number', step='1', style={'width':'98%'})
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                        html.Div([
                                html.Div([], style={'display':'table-cell'}),
                                html.Div(['Lower bound:'], style={'display':'table-cell'}),
                                html.Div([
                                        dcc.Input( id='market-menu-asset-p_bounds_low', value=Asset_dict['p_bounds_low'], type='number', step='1', style={'width':'98%'})
                                        ], style={'display':'table-cell'}),
                                ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([],id='market-menu-asset-void')
                    ])
    
    #%% Market tab -- Save menu
    def Menu_Save(self,type_save='Save'):
        self.init_DefaultFilename()
        if type_save=='Save as':
            text_read = [dcc.Input( id='market-menu-saveas-filename', value=self.current_filename[0:-6],type='text', style={'width':'99%'})]
        else:
            text_read = [self.current_filename[0:-6],
                         dcc.Input( id='market-menu-saveas-filename', value=self.current_filename[0:-6],type='text', style={'display':'none'})]
        return html.Div([
                html.Div([
                    html.Div([
                            html.Div([], style={'display':'table-cell','width':'20%'}),
                            html.Div([], style={'display':'table-cell','width':'40%'}),
                            html.Div([], style={'display':'table-cell','width':'10%'}),
                            html.Div([], style={'display':'table-cell','width':'10%'}),
                            html.Div([], style={'display':'table-cell','width':'20%'}),
                            ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['File name:'], style={'display':'table-cell'}),
                            html.Div(text_read, style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}),
                            html.Div([html.Button(children='Save', id = 'market-menu-save-button', type='submit', n_clicks=self.clicks_save)], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                        ], style={'display':'table','width':'100%'}),
                html.Div([], id='market-menu-save-message')
                ], id='market-menu-save-refresh')
    
    def Menu_SaveGraph(self,n_save=None,filename=None):
        if n_save is not None and self.clicks_save != n_save:
            self.clicks_save = n_save
            if filename is None:
                filename = self.current_filename
            return html.Div([
                    html.Button(children=self.SaveMarketGraph(filename), id = 'market-menu-save-button-message', type='submit', n_clicks=0)
                    ], style={'display':'none'})
        else:
            return 
    
    #%% Market tab -- Agent menu
    def Menu_AddFile(self,filetype='Example',actiontype='Add'):
        return html.Div([
                    html.Div([self.defaultTable,
                        html.Div([
                            html.Div(['File type:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-addfile-extension', clearable=False, value='pyp2p',
                                                 options=[{'label':'pyp2p','value':'pyp2p'},{'label':'csv','value':'csv'}])
                                    ], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.Div([], id='market-menu-addfile-select'),
                ], id='market-menu-addfile-refresh')
        
    def Menu_AddFileSelect(self,extension='pyp2p',actiontype='Add',filetype='Example'):
        if filetype=='File':
            self.current_dirpath = self.default_dirpath
        else:
            self.current_dirpath = self.default_dirpath_examples
        if actiontype=='Open':
            mark = dcc.Markdown('**Warning: All changes since last saving will be lost.**')
        else:
            mark = ''
        if actiontype=='Open' and filetype=='New':
            button_chil = 'New'
            entry = ''
            #drop = html.Div([dcc.Dropdown( id='market-menu-addfile-filename', value='****NEW****')], style={'display':'none'})
        else:
            if actiontype=='Open':
                button_chil = 'Open'
            else:
                button_chil = 'Add'
        if extension=='csv':
            entry = 'Main file:'
        else:
            entry = 'File:'
        
        cells = [self.defaultTable,
                    html.Div([
                        html.Div([entry], style={'display':'table-cell'}),
                        html.Div([
                            dcc.Dropdown( id='market-menu-addfile-filename', clearable=False,
                                options=[{'label':str(file[0:-(len(extension)+1)]),'value':str(file)} for file in os.listdir(self.current_dirpath) if file.endswith('.'+extension)], 
                                value=self.current_filename )
                                ], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input(id='market-menu-addfile-type', value=actiontype, style={'display':'none'})
                                ], style={'display':'table-cell'}),
                        ], style={'display':'table-row'})
                    ]
        if extension=='csv':
            cells.extend([
                    html.Div([
                        html.Div(['Connectivity matrix'], style={'display':'table-cell'}),
                        html.Div([
                            dcc.Dropdown( id='market-menu-addfile-connect-matrix', clearable=False, value='Full',
                                options=[
                                        {'label':'Full P2P','value':'Full'},
                                        {'label':'Consumer-Producer','value':'Partial'},
                                        {'label':'Community','value':'Community'},
                                        {'label':'From preference file','value':'PrefFile'},
                                        ])
                            ], style={'display':'table-cell'})
                        ], style={'display':'table-row'})
                    ])
        else:
            cells.extend([
                    html.Div([
                        dcc.Dropdown( id='market-menu-addfile-connect-matrix', value=None),
                        dcc.Dropdown( id='market-menu-addfile-pref-filename', value=None),
                        dcc.Input( id='market-menu-addfile-pref-ceil', value=None)
                        ], style={'display':'none'})
                    ])
        return html.Div([
                html.Div(cells, style={'display':'table','width':'100%'}),
                html.Div([], id='market-menu-addfile-prefs'),
                html.Div([self.defaultTable, 
                        html.Div([
                          html.Div([], style={'display':'table-cell'}),
                          html.Div([], style={'display':'table-cell'}),
                          html.Div([html.Button(children=button_chil, id = 'market-menu-addfile-button', type='submit', n_clicks=self.clicks_save)], style={'display':'table-cell'}),
                        ], style={'display':'table-row'})
                    ], style={'display':'table','width':'100%'}),
                html.Div([mark]),
                html.Div([], id='market-menu-addfile-message')
                ], id='market-menu-addfile-refresh')
        
    def Menu_AddFilePrefs(self,connectivity='Full'):
        if connectivity=='PrefFile':
            return html.Div([self.defaultTable,
                    html.Div([
                        html.Div(['Preference file'], style={'display':'table-cell'}),
                        html.Div([
                            dcc.Dropdown( id='market-menu-addfile-pref-filename', clearable=False,
                                options=[{'label':str(file[0:-4]),'value':str(file)} for file in os.listdir(self.current_dirpath) if file.endswith('.csv')], 
                                value=self.current_filename )
                            ], style={'display':'table-cell'})
                        ], style={'display':'table-row'}),
                    html.Div([
                        html.Div(['Preference ceil:'], style={'display':'table-cell'}),
                        html.Div([
                            dcc.Input( id='market-menu-addfile-pref-ceil', value=self.default_preference_threshold)
                            ], style={'display':'table-cell'})
                        ], style={'display':'table-row'})
                    ], style={'display':'table','width':'100%'}),
        else:
            return html.Div([
                    dcc.Dropdown( id='market-menu-addfile-pref-filename', value=None),
                    dcc.Input( id='market-menu-addfile-pref-ceil', value=None)
                    ], style={'display':'none'}),
    
    def Menu_AddFileMessage(self,n_add=None,filename=None,extension='pyp2p',actiontype='Add',connectivity='Full',pref_file=None,pref_ceil=None):
        if n_add is not None and self.clicks_save != n_add and filename is not None and actiontype is not None:
            self.clicks_save = n_add
            if pref_ceil is None:
                pref_ceil = self.default_preference_threshold
            
            message = ''
            if actiontype=='Open' and filename=='****NEW****':
                self.MGraph = Graph(directed=True)
                self.maxID = 0
            elif actiontype=='Open':
                if extension=='csv':
                    self.OpenMarketGraph_csv(filename,connectivity,pref_file,pref_ceil)
                else:
                    self.OpenMarketGraph(filename)
            elif actiontype=='Add':
                if extension=='csv':
                    message = self.UnionMarketGraph_csv(filename,connectivity,pref_file,pref_ceil)
                else:
                    message = self.UnionMarketGraph(filename)
            return html.Div([
                    html.Button(children=message, id = 'market-menu-addfile-button-message', type='submit', n_clicks=0)
                    ], style={'display':'none'})
        else:
            return 
    
    
    #%% Market tab -- graph management -- Lists
    def ListAgentsID(self,show_self=True,show_type=None):
        if show_type is None and show_self:
            show_list = [self.MGraph.vs[i]['ID'] for i in range(len(self.MGraph.vs))]
        elif show_type is None and not show_self:
            show_list = [self.MGraph.vs[i]['ID'] for i in range(len(self.MGraph.vs)) if i!=self.AgentID]
        else:
            if show_self:
                show_list = [self.MGraph.vs[i]['ID'] for i in range(len(self.MGraph.vs)) if self.MGraph.vs[i]['Type']==show_type]
            else:
                show_list = [self.MGraph.vs[i]['ID'] for i in range(len(self.MGraph.vs)) if self.MGraph.vs[i]['Type']==show_type and i!=self.AgentID]
        return show_list 
    
    def ListAllowedPartners(self,whos=None):
        if whos is None:
            who = self.AgentID
        else:
            who = whos
        exclusion_list = [self.MGraph.vs[who].index]
        # Exclude all agents in the same community(ies)
        for x in self.MGraph.vs[who]['Community']:
            exclusion_list.append(x)
            if not self.allow_P2P_within_community:
                exclusion_list.extend([self.MGraph.vs.select(ID=y)[0].index for y in self.MGraph.vs.select(ID=x)[0]['Community']])
        # Exclude trades 
        for x in self.MGraph.vs[who]['Partners']:
            idx = self.MGraph.vs.select(ID=x)[0].index
            if self.MGraph.vs[idx]['Type']=='Manager':
                exclusion_list.extend([self.MGraph.vs.select(ID=y)[0].index for y in self.MGraph.vs[idx]['Community']])
            elif not self.allow_P2P_with_both_communitymanager_and_its_members:
                for y in self.MGraph.vs[idx]['Community']:
                    exclusion_list.append(self.MGraph.vs.select(ID=y)[0].index)
        if whos is None:
            exclusion_list.extend(self.MGraph.vs[who]['Community'])
            exclusion_list.extend(self.MGraph.vs[who]['Partners'])
        return self.ListAgentsIndex(exclusion_list)
    
    def ListAllowedCommunities(self,whos=None):
        if whos is None:
            who = self.AgentID
        else:
            who = whos
        # Exclude itself if is a manager and managers which are trading partners
        if self.MGraph.vs[who]['Type'] == 'Manager':
            exclusion_list = [self.MGraph.vs[who].index]
            if not self.allow_P2P_with_both_communitymanager_and_its_members:
                exclusion_list.extend([self.MGraph.vs.select(ID=x)[0].index for x in self.MGraph.vs[who]['Partners']])
            return self.ListAgentsIndex(exclusion_list)
        else:
            inclusion_list = [x.index for x in self.MGraph.vs.select(Type='Manager') if x['ID'] not in self.MGraph.vs[who]['Partners']]
            return inclusion_list
    
    #%% Market tab -- graph management -- Creation
    def CreateCommunity(self,n_agents,returnID=False):
        if self.update_graph:
            if not isinstance(n_agents,int):
                n_agents = int(n_agents)
            Ag_IDs = [self.CreateAgent(True) for i in range(n_agents+1)]
            self.AgentID = Ag_IDs.pop(0)
            self.MGraph.vs[self.AgentID]['name'] = 'Manager' + ' ' + str(self.AgentID+1)
            self.MGraph.vs[self.AgentID]['Type'] = 'Manager'
            self.MGraph.vs[self.AgentID]['AssetsNum'] = 0
            self.MGraph.vs[self.AgentID]['Assets'] = []
            self.MGraph.vs[self.AgentID]['Community'] = Ag_IDs
            self.MGraph.vs[self.AgentID]['CommPref'] = [self.default_community_preference for i in range(n_agents)]
            self.CreatePartnership()
        if returnID:
            return self.AgentID
    
    def CreateAgent(self,returnID=False):
        if self.update_graph:
            self.AgentName = 'Agent' + ' ' + str(self.maxID+1)
            self.MGraph.add_vertex(name=self.AgentName,ID=self.maxID,Type='Agent',
                                        AssetsNum=1,Assets=[self.default_asset],
                                        Partners=[],Preferences=[],Community=[],CommPref=[],CommGoal=None,ImpFee=0)
            self.AgentID = self.MGraph.vs.find(ID=self.maxID).index
            self.maxID += 1
        if returnID:
            return self.AgentID
    
    def CreateAsset(self):
        for i in range(len(self.MGraph.vs[self.AgentID]['Assets']),int(self.MGraph.vs[self.AgentID]['AssetsNum'])):
            asset_dict = self.default_asset
            asset_dict['id'] = i
            asset_dict['name'] = 'Asset '+ str(i+1)
            self.MGraph.vs[self.AgentID]['Assets'].append(asset_dict)
    
    #%% Market tab -- graph management -- Changes
    def AgentType(self,agent_type):
        self.MGraph.vs[self.AgentID]['Type'] = agent_type
        return self.Menu_AgentData()
    
    def AgentChange(self,agent_name,agent_n_assets):
        self.AgentName = agent_name
        self.MGraph.vs[self.AgentID]['name'] = agent_name
        self.MGraph.vs[self.AgentID]['AssetsNum'] = agent_n_assets
        self.CreateAsset()
        return self.ShowAssetsMenu()
    
    def AgentChangeCommGoal(self,comm_goal,impfee):
        self.MGraph.vs[self.AgentID]['CommGoal'] = comm_goal
        self.MGraph.vs[self.AgentID]['ImpFee'] = impfee
        if comm_goal=='Lowest Importation':
            return {'display':'table-row'}
        else:
            return {'display':'none'}
    
    def AgentPartners(self,agent_partners,agent_preferences):
        self.MGraph.vs[self.AgentID]['Partners'] = agent_partners
        return self.AgentPreferences(agent_preferences)
    
    def AgentCommunity(self,agent_community,agent_commpref):
        self.MGraph.vs[self.AgentID]['Community'] = agent_community
        return self.AgentCommPref(agent_commpref)
    
    def AgentChangeNAssets(self,agent_n_assets):
        if self.MGraph.vs[self.AgentID]['Type'] == 'Manager':
            self.MGraph.vs[self.AgentID]['AssetsNum'] = 0
        else:
            self.MGraph.vs[self.AgentID]['AssetsNum'] = agent_n_assets
        self.CreateAsset()
        return self.ShowAssetsMenu()
    
    def AssetChange(self,asset_name,asset_type,asset_costfct,asset_costfct_coeff,asset_p_bounds_up,asset_p_bounds_low):
        Asset_dict = self.MGraph.vs[self.AgentID]['Assets'][self.AssetID]
        Asset_dict['name'] = asset_name
        Asset_dict['type'] = asset_type
        Asset_dict['costfct'] = asset_costfct
        Asset_dict['costfct_coeff'] = [float(x) for x in asset_costfct_coeff.split(',')]
        Asset_dict['p_bounds_up'] = asset_p_bounds_up
        Asset_dict['p_bounds_low'] = asset_p_bounds_low
        self.MGraph.vs[self.AgentID]['Assets'][self.AssetID] = Asset_dict
        return []
    
    def AgentPreferences(self,Pref=[]):
        if isinstance(Pref, str):
            Pref = [float(x) for x in Pref.split(',') if x!='' and x!=' ']
        if Pref!=[]:
            self.MGraph.vs[self.AgentID]['Preferences'] = Pref
        for i in range( len(self.MGraph.vs[self.AgentID]['Partners']) - len(self.MGraph.vs[self.AgentID]['Preferences']) ):
            self.MGraph.vs[self.AgentID]['Preferences'].append(float(self.default_partnership_preference))
        self.CreatePartnership()
        return self.Menu_Preferences()
    
    def AgentCommPref(self,Pref=[]):
        if isinstance(Pref, str):
            Pref = [float(x) for x in Pref.split(',') if x!='' and x!=' ']
        if Pref!=[]:
            self.MGraph.vs[self.AgentID]['CommPref'] = Pref
        for i in range( len(self.MGraph.vs[self.AgentID]['Community']) - len(self.MGraph.vs[self.AgentID]['CommPref']) ):
            self.MGraph.vs[self.AgentID]['CommPref'].append(float(self.default_partnership_preference))
        self.CreatePartnership()
        return self.Menu_CommPref()
    
    def CreatePartnership(self,idx=None):
        if idx is None:
            idx = self.AgentID
        # Delete some edges if too many
        Edges = self.MGraph.es.select(_source=idx)
        if len(Edges) > (len(self.MGraph.vs[idx]['Partners']) + len(self.MGraph.vs[idx]['Community']) ):
            to_del = []
            for x in Edges:
                if self.MGraph.vs[x.tuple[1]]['ID'] not in self.MGraph.vs[idx]['Partners'] and self.MGraph.vs[x.tuple[1]]['ID'] not in self.MGraph.vs[idx]['Community']:
                    self.DeletePartnership(x.tuple[0],x.tuple[1])
                    to_del.append(x.index)
                        
            for x in self.MGraph.es.select(_target=idx):
                if self.MGraph.vs[x.tuple[0]]['ID'] not in self.MGraph.vs[idx]['Partners'] and self.MGraph.vs[x.tuple[0]]['ID'] not in self.MGraph.vs[idx]['Community']:
                    to_del.append(x.index)
            self.MGraph.delete_edges(to_del)
            
        # Update and/or add edges
        Edges = self.MGraph.es.select(_source=idx)
        c_target = []
        for x in Edges:
            c_target.append(x.tuple[1])
        for i in range(len(self.MGraph.vs[idx]['Partners'])):
            idp = self.MGraph.vs.find(ID=self.MGraph.vs[idx]['Partners'][i]).index
            if idp not in c_target:
                self.MGraph.add_edge(idx,idp,weight=float(self.MGraph.vs[idx]['Preferences'][i]))
                self.MGraph.add_edge(idp,idx,weight=float(self.default_partnership_preference))
                self.MGraph.vs[idp]['Partners'].append(self.MGraph.vs[idx]['ID'])
                self.MGraph.vs[idp]['Preferences'].append(float(self.default_partnership_preference))
            else:
                for x in Edges.select(_target=idp):
                    self.MGraph.es[x.index]['weight']=float(self.MGraph.vs[idx]['Preferences'][i])
        for i in range(len(self.MGraph.vs[idx]['Community'])):
            idc = self.MGraph.vs.find(ID=self.MGraph.vs[idx]['Community'][i]).index
            if idc not in c_target:
                self.MGraph.add_edge(idx,idc,weight=float(self.MGraph.vs[idx]['CommPref'][i]))
                self.MGraph.add_edge(idc,idx,weight=float(self.default_community_preference))
                self.MGraph.vs[idc]['Community'].append(self.MGraph.vs[idx]['ID'])
                self.MGraph.vs[idc]['CommPref'].append(float(self.default_community_preference))
            else:
                for x in Edges.select(_target=idc):
                    self.MGraph.es[x.index]['weight']=float(self.MGraph.vs[idx]['CommPref'][i])
    
    def CommunityChange(self,comm_name,comm_goal,comm_members):
        self.AgentName = comm_name
        self.MGraph.vs[self.AgentID]['name'] = comm_name
        self.MGraph.vs[self.AgentID]['CommGoal'] = comm_goal
        comm_members = comm_members.split(',')
        for i in range( min(len(self.MGraph.vs[self.AgentID]['Community']),len(comm_members)) ):
            self.MGraph.vs.select( ID=self.MGraph.vs[self.AgentID]['Community'][i] )[0]['name'] = comm_members[i]
        return []
    
    def LinkTest(self,link_type=''):
        if link_type=='Partnership':
            lpart = 'Partners'
            lpref = 'Preferences'
            okay = True
        elif link_type=='Membership':
            lpart = 'Community'
            lpref = 'CommPref'
            okay = True
        else:
            lpart = []
            lpref = []
            okay = False
        return [okay,lpart,lpref]
    
    def LinkAdd(self,link_type,who1,who2,pref1,pref2):
        [okay,lpart,lpref] = self.LinkTest(link_type)
        if okay and (self.MGraph.vs[who1]['ID'] in self.MGraph.vs[who2][lpart] or self.MGraph.vs[who2]['ID'] in self.MGraph.vs[who1][lpart]):
            okay = False
        elif okay:
            self.MGraph.vs[who1][lpart].append(self.MGraph.vs[who2]['ID'])
            self.MGraph.vs[who1][lpref].append(pref1)
            self.CreatePartnership(who1)
            okay = self.LinkChange(link_type,who1,who2,pref1,pref2)
        return okay
    
    def LinkDelete(self,link_type,who1,who2):
        [okay,lpart,lpref] = self.LinkTest(link_type)
        if okay:
            if self.MGraph.vs[who1]['ID'] in self.MGraph.vs[who2][lpart] or self.MGraph.vs[who2]['ID'] in self.MGraph.vs[who1][lpart]:
                print('in0')
                if self.MGraph.vs[who1]['ID'] in self.MGraph.vs[who2][lpart]:
                    ids = self.MGraph.vs[who1][lpart].index(self.MGraph.vs[who2]['ID'])
                    del self.MGraph.vs[who1][lpref][ids]
                    del self.MGraph.vs[who1][lpart][ids]
                if self.MGraph.vs[who2]['ID'] in self.MGraph.vs[who1][lpart]:
                    ids = self.MGraph.vs[who2][lpart].index(self.MGraph.vs[who1]['ID'])
                    del self.MGraph.vs[who2][lpref][ids]
                    del self.MGraph.vs[who2][lpart][ids]
                self.CreatePartnership(who1)
            else:
                okay = False
        return okay
    
    def LinkChange(self,link_type,who1,who2,pref1,pref2):
        [okay,lpart,lpref] = self.LinkTest(link_type)
        if okay and (self.MGraph.vs[who1]['ID'] not in self.MGraph.vs[who2][lpart] or self.MGraph.vs[who2]['ID'] not in self.MGraph.vs[who1][lpart]):
            okay = False
        elif okay:
            self.MGraph.vs[who1][lpref][self.MGraph.vs[who1][lpart].index(self.MGraph.vs[who2]['ID'])] = pref1
            self.MGraph.vs[who2][lpref][self.MGraph.vs[who2][lpart].index(self.MGraph.vs[who1]['ID'])] = pref2
            Edges = self.MGraph.es.select(_source=who1)
            Edges = Edges.select(_target=who2)
            for ed in Edges:
                self.MGraph.es[ed.index]['weight'] = pref1
            Edges = self.MGraph.es.select(_source=who2)
            Edges = Edges.select(_target=who1)
            for ed in Edges:
                self.MGraph.es[ed.index]['weight'] = pref2
        return okay
    
    #%% Market tab -- graph management -- Suppresions
    def DeletePartnership(self,id_from,id_to):
        if self.MGraph.vs[id_from]['ID'] in self.MGraph.vs[id_to]['Partners']:
            if self.MGraph.vs[id_from]['ID'] in self.MGraph.vs[id_to]['Partners']:
                id_del = self.MGraph.vs[id_to]['Partners'].index(self.MGraph.vs[id_from]['ID'])
                useless = self.MGraph.vs[id_to]['Partners'].pop(id_del)
                useless = self.MGraph.vs[id_to]['Preferences'].pop(id_del)
            if self.MGraph.vs[id_to]['ID'] in self.MGraph.vs[id_from]['Partners']:
                id_del = self.MGraph.vs[id_from]['Partners'].index(self.MGraph.vs[id_to]['ID'])
                useless = self.MGraph.vs[id_from]['Partners'].pop(id_del)
                useless = self.MGraph.vs[id_from]['Preferences'].pop(id_del)
        elif self.MGraph.vs[id_from]['ID'] in self.MGraph.vs[id_to]['Community']:
            if self.MGraph.vs[id_from]['ID'] in self.MGraph.vs[id_to]['Community']:
                id_del = self.MGraph.vs[id_to]['Community'].index(self.MGraph.vs[id_from]['ID'])
                useless = self.MGraph.vs[id_to]['Community'].pop(id_del)
                useless = self.MGraph.vs[id_to]['CommPref'].pop(id_del)
            if self.MGraph.vs[id_to]['ID'] in self.MGraph.vs[id_from]['Community']:
                id_del = self.MGraph.vs[id_from]['Community'].index(self.MGraph.vs[id_to]['ID'])
                useless = self.MGraph.vs[id_from]['Community'].pop(id_del)
                useless = self.MGraph.vs[id_from]['CommPref'].pop(id_del)
    
    def DeleteAssets(self,delete_asset=[]):
        for i in range(int(self.MGraph.vs[self.AgentID]['AssetsNum']),len(self.MGraph.vs[self.AgentID]['Assets'])):
            useless = self.MGraph.vs[self.AgentID]['Assets'].pop()
        delete_asset.sort(reverse=True)
        for i in delete_asset:
            useless = self.MGraph.vs[self.AgentID]['Assets'].pop(i)
        if delete_asset!=[]:
            self.MGraph.vs[self.AgentID]['AssetsNum'] = str(len(self.MGraph.vs[self.AgentID]['Assets']))
    
    def DeleteAgent(self,del_id=None):
        if del_id is None:
            del_id = self.AgentID
        for x in self.MGraph.vs[del_id]['Partners']:
            for y in self.MGraph.vs.select(ID=x):
                self.DeletePartnership(del_id,y.index)
        for x in self.MGraph.vs[del_id]['Community']:
            for y in self.MGraph.vs.select(ID=x):
                self.DeletePartnership(del_id,y.index)
        self.MGraph.delete_vertices(del_id)
    
    def DeleteCommunity(self,del_id=None):
        if del_id is None:
            del_id = self.AgentID
        if self.MGraph.vs[del_id]['Type']=='Manager':
            list_mem = np.copy(self.MGraph.vs[del_id]['Community'])
            self.DeleteAgent(del_id)
            for mem in list_mem:
                for x in self.MGraph.vs.select(ID=mem):
                    self.DeleteAgent(x.index)
#            for n in self.MGraph.vs:
#                if self.MGraph.vs[del_id]['ID'] in n['Community']:
##                    if n['Type']=='Manager':
##                        self.DeleteCommunity(n.index)
##                    else:
##                        self.DeleteAgent(n.index)
#                    self.DeleteAgent(n.index)
    
    #%% Market tab -- graph management -- Save & Open & Add from file
    def SaveMarketGraph(self,filename=None):
        if filename is None:
            filename = self.current_filename
        if not filename.endswith('.pyp2p'):
            filename += '.pyp2p'
        #self.MGraph.save(self.current_dirpath+'/'+filename, format='picklez')
        self.MGraph.Save(self.MGraph,self.current_dirpath+'/'+filename, format='picklez')
        self.current_filename = filename
        return 'The graph has been saved.'
    
    def LoadMarketGraph(self,filename=None):
        if filename is None:
            filename = self.current_filename
        if not filename.endswith('.pyp2p'):
            filename += '.pyp2p'
        #return load(self.current_dirpath+'/'+filename, format='picklez'), filename
        return self.MGraph.Load(self.current_dirpath+'/'+filename, format='picklez'), filename
    
    def OpenMarketGraph(self,filename=None):
        NewMarket,filename = self.LoadMarketGraph(filename)
        if self.VerifyMarketGraphFormat(NewMarket):
            self.MGraph = NewMarket
            self.current_filename = filename
            self.maxID = 0
            for ns in self.MGraph.vs:
                if self.maxID <= ns['ID']:
                    self.maxID = ns['ID']
            self.maxID += 1
        return
    
    def UnionMarketGraph(self,filename=None):
        NewMarket,useless = self.LoadMarketGraph(filename)
        if self.VerifyMarketGraphFormat(NewMarket):
            Ag_old = [NewMarket.vs[i]['ID'] for i in range(len(NewMarket.vs))]
            Ag_IDs = [self.CreateAgent(True) for i in range(len(NewMarket.vs))]
            Ag_new = [self.MGraph.vs[i]['ID'] for i in Ag_IDs]
            for i in range(len(NewMarket.vs)):
                for att in self.default_vertex_attributes:
                    if att == 'Partners' or att=='Community':
                        self.MGraph.vs[Ag_IDs[i]][att] = [Ag_new[Ag_old.index(idx)] for idx in NewMarket.vs[i][att]]
                    elif att != 'ID':
                        self.MGraph.vs[Ag_IDs[i]][att] = NewMarket.vs[i][att]
            for i in range(len(NewMarket.es)):
                self.MGraph.add_edge(Ag_IDs[NewMarket.es[i].source], Ag_IDs[NewMarket.es[i].target], weight=NewMarket.es[i]['weight'])
            return ''
        else:
            return 'Wrong file format.'
    
    def VerifyMarketGraphFormat(self,NewMarket=None):
        output = False
        if NewMarket is not None:
            self.default_vertex_attributes = ['ID','name','Type','AssetsNum','Assets','Partners','Preferences','Community','CommPref','CommGoal','ImpFee']
            if set(NewMarket.vs.attributes())==set(self.default_vertex_attributes) and 'weight' in NewMarket.es.attributes():
                obj = 0
                cnt = 0
                def_list = set([key for key, data_list in self.default_asset.items()])
                for i in range(len(NewMarket.vs)):
                    obj += len(NewMarket.vs[i]['Assets'])
                    for j in range(len(NewMarket.vs[i]['Assets'])):
                        if set([key for key, data_list in NewMarket.vs[i]['Assets'][j].items()]) == def_list:
                            cnt += 1
                if cnt==obj:
                    output = True
        return output
    
    def LoadMarketGraph_csv(self,filename,connectivity=None,pref_file=None,pref_ceil=None):
        if not filename.endswith('.csv'):
            filename += '.csv'
        info = pd.read_csv(self.current_dirpath+'/'+filename,dtype={'Agent':np.int64,'Pmin':np.float64,'Pmax':np.float64,'a':np.float64,'b':np.float64})
        if min(info['Agent'])>0:
            info['Agent'] -= min(info['Agent'])
        if min(info['Community'])==0:
            info['Community'] += 1
        elif min(info['Community'])<0:
            info['Community'] -= min(info['Community']) + 1
        
        NewGraph = MGraph(directed=True)
        ids = info['Agent'].unique()
        for i in range(len(ids)):
            coeff_a = info['a'][info['Agent']==ids[i]].values
            coeff_b = info['b'][info['Agent']==ids[i]].values
            Pmax = info['Pmax'][info['Agent']==ids[i]].values
            Pmin = info['Pmin'][info['Agent']==ids[i]].values
            energy = info['Energy'][info['Agent']==ids[i]].values
            ag_name = info['Name'][info['Agent']==ids[i]].values[0]
            Ass = []
            for nas in range(len(coeff_a)):
                new = copy.deepcopy(self.default_asset)
                if energy[nas] in self.assets_type_shortcut:
                    energy[nas] = self.assets_type_shortcut[energy[nas]]
                new['name'] = energy[nas]
                new['type'] = energy[nas]
                #print(energy[nas])
                new['costfct_coeff'] = [coeff_a[nas],coeff_b[nas],0]
                new['p_bounds_up'] = Pmax[nas]
                new['p_bounds_low'] = Pmin[nas]
                new['id'] = nas+1
                Ass.append(new)
            NewGraph.add_vertex(name=ag_name,ID=ids[i],Type='Agent',
                                AssetsNum=len(coeff_a),Assets=Ass,
                                Partners=[],Preferences=[],Community=[],CommPref=[],CommGoal=None,ImpFee=0)
        
        if connectivity=='PrefFile':
            if pref_ceil is None:
                pref_ceil = self.default_preference_threshold
            else:
                pref_ceil = int(pref_ceil)
            if not pref_file.endswith('.csv'):
                pref_file += '.csv'
            pref = pd.read_csv(self.current_dirpath+'/'+pref_file,index_col=[0],dtype=np.float64)
            pref.index = pref.index.astype('int64')
            if np.shape(pref)==(len(NewGraph.vs),len(NewGraph.vs)):
                for n in NewGraph.vs:
                    i = n['ID']
                    for j in range(len(NewGraph.vs)):
                        if j!=i and pref[str(i)][j]<=pref_ceil:
                            for x in NewGraph.vs.select(ID=info['Agent'][j]):
                                NewGraph.add_edge(n.index,x.index,weight=pref[str(i)][j])
                                NewGraph.vs[n.index]['Partners'].append(info['Agent'][j])
                                NewGraph.vs[n.index]['Preferences'].append(pref[str(i)][j])
            elif np.shape(pref)==(max(info['Community']),max(info['Community'])):
                nag = len(info['Agent'])
                for c in range(max(info['Community'])):
                    NewGraph.add_vertex(name='Community '+str(c+1),ID=nag+c,Type='Manager',
                                        AssetsNum=0,Assets=[],
                                        Partners=[],Preferences=[],Community=[],CommPref=[],CommGoal=None,ImpFee=0)
                cs = NewGraph.vs.select(Type='Manager')
                ns = NewGraph.vs.select(Type_ne='Manager')
                for n in cs:
                    for x in cs.select(ID_ne=n['ID']):
                        NewGraph.add_edge(n.index,x.index,weight=pref[str(n['ID']-nag)][x['ID']-nag])
                        NewGraph.vs[n.index]['Partners'].append(x['ID'])
                        NewGraph.vs[n.index]['Preferences'].append(pref[str(n['ID']-nag)][x['ID']-nag])
                    for x in ns:
                        if info['Community'][x['ID']]==n['ID']-nag+1:
                            NewGraph.add_edge(n.index,x.index,weight=0)
                            NewGraph.vs[n.index]['Community'].append(x['ID'])
                            NewGraph.vs[n.index]['CommPref'].append(0)
                            NewGraph.add_edge(x.index,n.index,weight=0)
                            NewGraph.vs[x.index]['Community'].append(n['ID'])
                            NewGraph.vs[x.index]['CommPref'].append(0)
                            NewGraph.vs[n.index]['CommGoal'] = self.community_goal_options[0]
        elif connectivity=='Full':
            for n in NewGraph.vs:
                for x in NewGraph.vs.select(ID_ne=n['ID']):
                    NewGraph.add_edge(n.index,x.index,weight=0)
                    NewGraph.vs[n.index]['Partners'].append(x['ID'])
                    NewGraph.vs[n.index]['Preferences'].append(0)
        elif connectivity=='Partial':
            cons = []
            prod = []
            pros = []
            for n in NewGraph.vs:
                prof_loc = []
                for nas in range(NewGraph.vs[n.index]['AssetsNum']):
                    if NewGraph.vs[n.index]['Assets'][nas]['p_bounds_up']<=0.0 and 'Cons' not in prof_loc:
                        prof_loc.append('Cons')
                    elif NewGraph.vs[n.index]['Assets'][nas]['p_bounds_low']>=0.0 and 'Prod' not in prof_loc:
                        prof_loc.append('Prod')
                    else:
                        prof_loc.append('Pros')
                if len(prof_loc)>1 or 'Pros' in prof_loc:
                    pros.append(n.index)
                elif 'Prod' in prof_loc:
                    prod.append(n.index)
                elif 'Cons' in prof_loc:
                    cons.append(n.index)
            for n in NewGraph.vs:
                if n.index in cons or n.index in pros:
                    for x in prod:
                        NewGraph.add_edge(n.index,x,weight=0)
                        NewGraph.vs[n.index]['Partners'].append(NewGraph.vs[x]['ID'])
                        NewGraph.vs[n.index]['Preferences'].append(0)
                if n.index in prod or n.index in pros:
                    for x in cons:
                        NewGraph.add_edge(n.index,x,weight=0)
                        NewGraph.vs[n.index]['Partners'].append(NewGraph.vs[x]['ID'])
                        NewGraph.vs[n.index]['Preferences'].append(0)
                for x in pros:
                    NewGraph.add_edge(n.index,x,weight=0)
                    NewGraph.vs[n.index]['Partners'].append(NewGraph.vs[x]['ID'])
                    NewGraph.vs[n.index]['Preferences'].append(0)
        elif connectivity=='Community':
            nag = len(info['Agent'])
            for c in range(max(info['Community'])):
                NewGraph.add_vertex(name='Community '+str(c+1),ID=nag+c,Type='Manager',
                                    AssetsNum=0,Assets=[],
                                    Partners=[],Preferences=[],Community=[],CommPref=[],CommGoal=None,ImpFee=0)
            cs = NewGraph.vs.select(Type='Manager')
            ns = NewGraph.vs.select(Type_ne='Manager')
            for n in cs:
                for x in cs.select(ID_ne=n['ID']):
                    NewGraph.add_edge(n.index,x.index,weight=0)
                    NewGraph.vs[n.index]['Partners'].append(x['ID'])
                    NewGraph.vs[n.index]['Preferences'].append(0)
                for x in ns:
                    if info['Community'][x['ID']]==n['ID']-nag+1:
                        NewGraph.add_edge(n.index,x.index,weight=0)
                        NewGraph.vs[n.index]['Community'].append(x['ID'])
                        NewGraph.vs[n.index]['CommPref'].append(0)
                        NewGraph.add_edge(x.index,n.index,weight=0)
                        NewGraph.vs[x.index]['Community'].append(n['ID'])
                        NewGraph.vs[x.index]['CommPref'].append(0)
                        NewGraph.vs[n.index]['CommGoal'] = self.community_goal_options[0]
        
        return NewGraph
        
    
    def OpenMarketGraph_csv(self,filename,connectivity='Full',pref_file=None,pref_ceil=None):
        NewMarket = self.LoadMarketGraph_csv(filename,connectivity,pref_file,pref_ceil)
        if self.VerifyMarketGraphFormat(NewMarket):
            self.MGraph = NewMarket
            self.current_filename = filename
            self.maxID = 0
            for ns in self.MGraph.vs:
                if self.maxID <= ns['ID']:
                    self.maxID = ns['ID']
            self.maxID += 1
        return
    
    def UnionMarketGraph_csv(self,filename,connectivity='Full',pref_file=None,pref_ceil=None):
        if connectivity!='PrefFile':
            pref_file = None
        NewMarket = self.LoadMarketGraph_csv(filename,connectivity,pref_file,pref_ceil)
        if self.VerifyMarketGraphFormat(NewMarket):
            Ag_old = [NewMarket.vs[i]['ID'] for i in range(len(NewMarket.vs))]
            Ag_IDs = [self.CreateAgent(True) for i in range(len(NewMarket.vs))]
            Ag_new = [self.MGraph.vs[i]['ID'] for i in Ag_IDs]
            for i in range(len(NewMarket.vs)):
                for att in self.default_vertex_attributes:
                    if att == 'Partners' or att=='Community':
                        self.MGraph.vs[Ag_IDs[i]][att] = [Ag_new[Ag_old.index(idx)] for idx in NewMarket.vs[i][att]]
                    elif att != 'ID':
                        self.MGraph.vs[Ag_IDs[i]][att] = NewMarket.vs[i][att]
            for i in range(len(NewMarket.es)):
                self.MGraph.add_edge(Ag_IDs[NewMarket.es[i].source], Ag_IDs[NewMarket.es[i].target], weight=NewMarket.es[i]['weight'])
            return ''
        else:
            return 'Wrong file format.'
    
    