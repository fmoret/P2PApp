# -*- coding: utf-8 -*-
"""
    Class managing market network tab layout
"""

import dash_core_components as dcc
import dash_html_components as html
from igraph import *
from loremipsum import get_sentences
from DashTabs import TabApp
import os


class MarketTabApp(TabApp):
    def __init__(self,Market):
        # Default parameters
        self.ShareWidth()
        self.init_GraphOfMarketGraph()
        self.init_DefaultMarketOptions()
        self.init_DefaultFilename()
        self.current_filename = self.default_filename
        # Default menu plot parameters
        self.market_topmenu_add = 'Add'
        self.market_topmenu_second = 'Agent'
        self.market_topmenu_third = ''
        self.default_AgentMenuTable = html.Div([
                html.Div([], style={'display':'table-cell','width':'27%'}),
                html.Div([], style={'display':'table-cell','width':'50%'}),
                html.Div([], style={'display':'table-cell','width':'3%'}),
                html.Div([], style={'display':'table-cell','width':'20%'}),
                ], style={'display':'table-row'})
        # State variables
        self.update_graph = False
        self.state_market_tab = 0 #Unused
        self.total_clicks = 0
        self.maxID = 0
        self.clicks_delete_confirm = 0
        self.clicks_delete_cancel = 0
        self.clicks_save = 0
        # Granting access to Market's graph 
        self.MarketGraph = Market
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
        self.community_goal_options = [
                 {'label':'Lowest Price','value':'Lowest Price'},
                 {'label':'Autonomy','value':'Autonomy'},
                 {'label':'Lowest Importation','value':'Lowest Importation'},
                 {'label':'Peak Shaving','value':'Peak Shaving'}]
    
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
    def ShowTab(self,tab_id):
        graph_data = html.Div([
                #html.Div(['aha']),
                self.ShowMarketGraph(),
                ])
        bottom_data = ''#'oho'
        menu_data = html.Div([self.ShowTabMarketTopMenu(),
                    html.Div([],id='market-menu')])
        return self.MenuTab(menu_data,graph_data,bottom_data)
    
    #%% Market tab -- Top menu   
    def ShowTabMarketTopMenu_Insert(self,insert_value=None):
        if insert_value is None:
            insert_value = self.market_topmenu_add
        else:
            self.market_topmenu_add = insert_value
        if insert_value=='Add':
            return html.Div([
                    dcc.Dropdown( id='market-topmenu-second-drop',
                                options=[
                                            {'label': 'Agent', 'value': 'Agent'},
                                            {'label': 'Community', 'value': 'Community'},
                                            {'label': 'Link (soon)', 'value': 'Link'},
                                            {'label': 'From example', 'value': 'Example'},
                                            {'label': 'From File', 'value': 'File'},
                                        ], 
                                value=self.market_topmenu_second,
                                clearable=False)
                    ])
        elif insert_value=='Change' or insert_value=='Delete':
            return html.Div([
                    dcc.Dropdown( id='market-topmenu-second-drop',
                                options=[
                                            {'label': 'Agent/Community', 'value': 'Agent/Community'},
                                            {'label': 'Link (soon)', 'value': 'Link'},
                                        ], 
                                value=self.market_topmenu_second,
                                clearable=False)
                    ])
        elif insert_value=='Save':
            return html.Div([
                    dcc.Dropdown( id='market-topmenu-second-drop',
                                options=[
                                            {'label': 'Save', 'value': 'Save'},
                                            {'label': 'Save as', 'value': 'Save as'},
                                        ], 
                                value='Save',
                                clearable=False)
                    ])
        elif insert_value=='Open':
            return html.Div([
                    dcc.Dropdown( id='market-topmenu-second-drop',
                                options=[
                                            {'label': 'New', 'value': 'New'},
                                            {'label': 'From example', 'value': 'Example'},
                                            {'label': 'From File', 'value': 'File'},
                                        ], 
                                value=self.market_topmenu_second,
                                clearable=False)
                    ])
        else:
            return html.Div([dcc.Dropdown( id='market-topmenu-second-drop')],style={'display':'none'})
    
    def ShowTabMarketTopMenu_Number(self,example_value=None,add_value=None):
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
                                 options=[{'label': self.MarketGraph.vs[i]['name'], 'value':i} for i in range(len(self.MarketGraph.vs))], 
                                 value=self.market_topmenu_third,
                                 clearable=False)
                    ])
        else:
            return html.Div([dcc.Input( id='market-topmenu-third-number', type='number', step=1, min=1, value=0)], style={'display':'none'})
    
    def ShowTabMarketTopMenu(self):
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
                    html.Div([self.ShowTabMarketTopMenu_Insert()
                            ], id='market-topmenu-second', style={'display': 'table-cell', 'width': '32%'}),
                    html.Div([], id='market-topmenu-void2', style={'display': 'table-cell', 'width': '2%'}),
                    html.Div([self.ShowTabMarketTopMenu_Number()], id='market-topmenu-third', style={'display': 'table-cell', 'width': '32%'}),
                    html.Div([], id='market-topmenu-void3', style={'display': 'table-cell', 'width': '2%'}),
                    html.Div([
                            html.Button(children='Select', id = 'add-button', type='submit', n_clicks=self.total_clicks)
                            ], id='test', style={'display': 'table-cell', 'width': '10%'})
                    ], id='market-topmenu', style={'display': 'table', 'width': '100%'}),
                    html.Hr()
                ])
    
    #%% Market tab -- Main menu
    def ShowTabMarketMenu(self,n_clicks,add_value,example_value,size_value):
        self.state_market_tab = 2
        if self.total_clicks != n_clicks:
            self.total_clicks = n_clicks
            self.update_graph = True
        else:
            self.update_graph = False
        
        if add_value=='Save':
            return self.ShowTabMarketMenu_Save(example_value)
        elif add_value=='Add':
            if example_value=='Agent':
                self.CreateAgent()
                return self.ShowTabMarketMenu_Agent()
            elif example_value=='Community':
                self.CreateCommunity(size_value)
                return self.ShowTabMarketMenu_Community()
            elif example_value=='Example':
                return self.ShowTabMarketMenu_AddFile('Example','Add')
            elif example_value=='File':
                return self.ShowTabMarketMenu_AddFile('File','Add')
            else:
                return 
        elif add_value=='Open':
            if example_value=='Example':
                return self.ShowTabMarketMenu_AddFile('Example','Open')
            elif example_value=='File':
                return self.ShowTabMarketMenu_AddFile('File','Open')
            elif example_value=='New':
                return self.ShowTabMarketMenu_AddFile('New','Open')
            else:
                return 
        else:
            if example_value=='Agent/Community':
                if add_value=='Delete':
                    return self.ShowTabMarketMenu_Delete()
                else:
                    self.AgentID = size_value
                    self.AgentName = self.MarketGraph.vs[self.AgentID]['name']
                    return self.ShowTabMarketMenu_Agent()
            else:
                return 
    
    def ShowTabMarketMenu_Preferences(self,idx=None):
        if idx is None:
            idx = self.AgentID
        return ','.join(str(x) for x in self.MarketGraph.vs[idx]['Preferences'])
    
    def ShowTabMarketMenu_CommPref(self):
        return ','.join(str(x) for x in self.MarketGraph.vs[self.AgentID]['CommPref'])
    
    #%% Market tab -- Agent menu
    def ShowTabMarketMenu_Agent(self):
        return html.Div([
                html.Div([
                    self.default_AgentMenuTable,
                    html.Div([
                            html.Div(['Agent type:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-type',
                                                 clearable=False,
                                                 options=[
                                                    {'label': 'Agent', 'value': 'Agent'},
                                                    {'label': 'Community Manager', 'value': 'Manager'},
                                                    #{'label': 'Grid', 'value': 'Grid'}
                                                ], value=self.MarketGraph.vs[self.AgentID]['Type'])
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}),
                            html.Div([
                                    html.Button(children='Refresh', id = 'agent-refresh-button', type='submit')
                                    ], style={'display':'table-cell'}, id='market-menu-agent-type-void'),
                                ], style={'display':'table-row'})
                        ], style={'display':'table','width':'100%'}),
                html.Div(self.ShowTabMarketMenu_AgentRefresh(), id='market-menu-agent-refresh')
                ])
    
    def ShowTabMarketMenu_AgentRefresh(self):
        return html.Div([], style={'display':'table','width':'100%'},id='market-menu-agent-data')
    
    def ShowTabMarketMenu_AgentData(self):
        if self.MarketGraph.vs[self.AgentID]['Type']=='Manager':
            Ag_name = 'Community name:'
            Comm_name = 'Community members:'
            min_ass = 0
            max_ass = 0
            self.MarketGraph.vs[self.AgentID]['AssetsNum'] = 0
            styl_goal = {'display':'table-row'}
            styl_ass = {'display':'none'}
        else:
            Ag_name = 'Agent name:'
            Comm_name = 'Community membership:'
            if self.MarketGraph.vs[self.AgentID]['AssetsNum'] == 0:
                self.MarketGraph.vs[self.AgentID]['AssetsNum'] = 1
            min_ass = 1
            max_ass = None
            styl_goal = {'display':'none'}
            styl_ass = {'display':'table-row'}
        AllowedPart = self.ListAllowedPartners()
        AllowedComm = self.ListAllowedCommunities()
        return [
                html.Div([self.default_AgentMenuTable,
                    html.Div([
                            html.Div([Ag_name], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-name', value=self.MarketGraph.vs[self.AgentID]['name'], type='text', style={'width':'99%'})
                                    ], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['Community objective:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-commgoal', 
                                                 clearable=False,
                                                 options=self.community_goal_options, 
                                                value=self.MarketGraph.vs[self.AgentID]['CommGoal'])
                                    ], style={'display':'table-cell'}),
                            ], style=styl_goal),
                    html.Div([
                            html.Div(['Trading partners:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-partners',
                                                 options=[{'label':self.MarketGraph.vs[i]['name'],'value':self.MarketGraph.vs[i]['ID']} for i in AllowedPart], 
                                                multi=True,
                                                value=self.MarketGraph.vs[self.AgentID]['Partners'])
                                    ], style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['Preferences:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-preferences', type='text', style={'width':'99%'},
                                              value=self.ShowTabMarketMenu_Preferences())
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}, id='market-menu-agent-preferences-void'),
                            ], style={'display':'table-row'}, id='market-menu-agent-prefDiv'),
                    html.Div([
                            html.Div([Comm_name], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Dropdown( id='market-menu-agent-community',
                                                 options=[{'label':self.MarketGraph.vs[i]['name'],'value':self.MarketGraph.vs[i]['ID']} for i in AllowedComm], 
                                                multi=True,
                                                value=self.MarketGraph.vs[self.AgentID]['Community'])
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}, id='market-menu-agent-community-void'),
                            ], style={'display':'table-row'}),
                    html.Div([
                            html.Div(['Community preference:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-commpref', type='text', style={'width':'99%'},
                                              value=self.ShowTabMarketMenu_CommPref())
                                    ], style={'display':'table-cell'}),
                            html.Div([], style={'display':'table-cell'}, id='market-menu-agent-commpref-void'),
                            ], style={'display':'table-row'}, id='market-menu-agent-commprefDiv'),
                    html.Div([
                            html.Div(['Number of assets:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input( id='market-menu-agent-number-assets', 
                                              value=self.MarketGraph.vs[self.AgentID]['AssetsNum'], 
                                              type='number', step=1, min=min_ass, max=max_ass, style={'width':'99%'})
                                    ], style={'display':'table-cell'}),
                            ], style=styl_ass),
                ], style={'display':'table','width':'100%'}),
                html.Div([], id='market-menu-assets'),
                ]
    
    #%% Market tab -- Community menu
    def ShowTabMarketMenu_Community(self):
        return [html.Div([self.default_AgentMenuTable,
                html.Div([
                        html.Div(['Community name:'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input( id='market-menu-community-name', value=self.MarketGraph.vs[self.AgentID]['name'], type='text', style={'width':'99%'})
                                ], style={'display':'table-cell'}),
                        html.Div([html.Button(children='Refresh', id = 'community-refresh-button', type='submit')], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                html.Div(self.ShowTabMarketMenu_CommunityRefresh(), id='market-menu-community-refresh')]
    
    def ShowTabMarketMenu_CommunityRefresh(self):
        AllowedPart = self.ListAllowedPartners()
        return html.Div([self.default_AgentMenuTable,
                html.Div([
                    html.Div(['Community objective:'], style={'display':'table-cell'}),
                    html.Div([
                            dcc.Dropdown( id='market-menu-community-commgoal', 
                                         clearable=False,
                                         options=self.community_goal_options, 
                                        value=self.MarketGraph.vs[self.AgentID]['CommGoal'])
                            ], style={'display':'table-cell'}),
                    ], style={'display':'table-row'}),
                html.Div([
                        html.Div(['Trading partners:'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Dropdown( id='market-menu-community-partners',
                                             options=[{'label':self.MarketGraph.vs[i]['name'],'value':self.MarketGraph.vs[i]['ID']} for i in AllowedPart], 
                                            multi=True,
                                            value=self.MarketGraph.vs[self.AgentID]['Partners'])
                                ], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                html.Div([
                        html.Div(['Preferences:'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input( id='market-menu-community-preferences', type='text', style={'width':'99%'},
                                          value=self.ShowTabMarketMenu_Preferences())
                                ], style={'display':'table-cell'}),
                        html.Div([], style={'display':'table-cell'}, id='market-menu-community-preferences-void'),
                        ], style={'display':'table-row'}, id='market-menu-community-prefDiv'),
                html.Div([
                        html.Div(['Community members'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input( id='market-menu-community-members', style={'width':'99%'},
                                            value=','.join([self.MarketGraph.vs.select(ID=x)['name'][0] for x in self.MarketGraph.vs[self.AgentID]['Community']]))
                                ], style={'display':'table-cell'}),
                        html.Div([], style={'display':'table-cell'}, id='market-menu-community-members-void'),
                        ], style={'display':'table-row'}),
            ], style={'display':'table','width':'100%'})
    
    #%% Market tab -- Delete menu
    def ShowTabMarketMenu_Delete(self):
        return html.Div(self.ShowTabMarketMenu_DeleteRefresh(), id='market-menu-delete-refresh')
    
    def ShowTabMarketMenu_DeleteRefresh(self,del_select=None):
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
                                             options=[{'label': x['name'] , 'value': x.index} for x in self.MarketGraph.vs])
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
    
    def ShowTabMarketMenu_DeleteType(self,Selected_Index=None):
        if Selected_Index != None:
            self.AgentID = Selected_Index
            if self.MarketGraph.vs[self.AgentID]['Type']=='Agent':
                return [html.Div(['What do you want to delete?'], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Dropdown( id='market-menu-delete-select-type',
                                             options=[{'label': 'The agent' , 'value': 'Agent'},
                                                     {'label': 'Some of its assets' , 'value': 'Assets'}], 
                                            value=None)
                                ], style={'display':'table-cell'}),
                        ]
            elif self.MarketGraph.vs[self.AgentID]['Type']=='Manager':
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
    
    def ShowTabMarketMenu_DeleteAssets(self,Selected_Type=None):
        if Selected_Type != None:
            if self.MarketGraph.vs[self.AgentID]['Type']=='Agent' and Selected_Type=='Assets':
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
                                         options=[{'label':self.MarketGraph.vs[self.AgentID]['Assets'][i]['name'],'value':i} for i in range(int(self.MarketGraph.vs[self.AgentID]['AssetsNum']))], 
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
    
    def ShowTabMarketMenu_DeleteWarning(self,Selected_Assets=None,Selected_Type=None):
        if Selected_Assets != None:
            message = []
            if isinstance(Selected_Assets,str) and Selected_Type!='Assets':
                if Selected_Type=='Agent':
                    message= [
                            html.Div([dcc.Markdown('**This action will delete the agent and all its assets!**')]),
                            html.Div(["Do you confirm the suppresion of agent '"+self.MarketGraph.vs[self.AgentID]['name']+"'?"])
                            ]
                elif Selected_Type=='Manager':
                    message= [
                            html.Div([dcc.Markdown('*Note that only the community manager will be deleted, other agents in the community will not be affected.*')]),
                            html.Div(["Do you confirm the suppresion of community manager '"+self.MarketGraph.vs[self.AgentID]['name']+"'?"])
                            ]
                elif Selected_Type=='Community':
                    message= [
                            html.Div([dcc.Markdown('**This action will delete all direct members of this community!**')]),
                            html.Div(["Do you confirm the suppresion of the community '"+self.MarketGraph.vs[self.AgentID]['name']+"'?"])
                            ]
            elif isinstance(Selected_Assets,list) and len(Selected_Assets)!=0 and Selected_Type=='Assets':
                length = len(Selected_Assets)-1
                list_assets = ""
                for i in range(length):
                    list_assets += "'"+ self.MarketGraph.vs[self.AgentID]['Assets'][Selected_Assets[i]]['name'] +"',"
                list_assets += "'"+ self.MarketGraph.vs[self.AgentID]['Assets'][Selected_Assets[length]]['name'] +"'"
                if length>0:
                    message= [
                            html.Div([dcc.Markdown('*Note that only the selected assets will be deleted, other assets will not be affected.*')]),
                            html.Div(["Do you confirm the suppresion of assets "+list_assets+" of agent "+self.MarketGraph.vs[self.AgentID]['name']+"?"])
                            ]
                else:
                    message= [
                            html.Div([dcc.Markdown('*Note that only the selected assets will be deleted, other assets will not be affected.*')]),
                            html.Div(["Do you confirm the suppresion of asset "+list_assets+" of agent "+self.MarketGraph.vs[self.AgentID]['name']+"?"])
                            ]
            if message!=[]:
                message.append(html.Div(html.Button(children='block', id ='market-menu-delete-show-confirm-button', type='submit', n_clicks=1), style={'display':'none'}))
                return html.Div(message)
            else:
                return [html.Div(html.Button(children='none', id ='market-menu-delete-show-confirm-button', type='submit', n_clicks=1), style={'display':'none'})]
        else:
            return [html.Div(html.Button(children='none', id ='market-menu-delete-show-confirm-button', type='submit', n_clicks=1), style={'display':'none'})]
    
    def ShowTabMarketMenu_DeleteConfirmed(self,n_cancel,n_confirm,delete_type=None,delete_asset=None):
        if self.clicks_delete_confirm != n_confirm:
            self.clicks_delete_confirm = n_confirm
            
            if delete_type=='Assets':
                length = len(delete_asset)-1
                list_assets = ""
                for i in range(length):
                    list_assets += "'"+ self.MarketGraph.vs[self.AgentID]['Assets'][delete_asset[i]]['name'] +"',"
                list_assets += "'"+ self.MarketGraph.vs[self.AgentID]['Assets'][delete_asset[length]]['name'] +"'"
                self.DeleteAssets(delete_asset)
                if length>0:
                    return ["Assets "+list_assets+" have been deleted"]
                else:
                    return ["Asset "+list_assets+" has been deleted"]
            elif delete_type=='Agent':
                message = ["Agent '"+self.MarketGraph.vs[self.AgentID]['name']+"' has been deleted"]
                self.DeleteAgent()
                return message
            elif delete_type=='Manager':
                message = ["Community mannager '"+self.MarketGraph.vs[self.AgentID]['name']+"' has been deleted"]
                self.DeleteAgent()
                return message
            elif delete_type=='Community':
                message = ["Community '"+self.MarketGraph.vs[self.AgentID]['name']+"' has been deleted"]
                self.DeleteCommunity()
                return message
            else:
                return []#['Confirm ',str(delete_type),' ',str(delete_asset)]
        elif self.clicks_delete_cancel != n_cancel:
            self.clicks_delete_cancel = n_cancel
            return []
        else:
            return [self.ShowTabMarketMenu_DeleteRefresh()]
    
    def ShowTabMarketMenu_DeleteShowConfirmed(self,show_disp):
        return {'display':show_disp}
    
    #%% Market tab -- Assets menu
    def ShowAssetsMenu(self):
        if self.AssetID >= int(self.MarketGraph.vs[self.AgentID]['AssetsNum']):
            self.AssetID = int(self.MarketGraph.vs[self.AgentID]['AssetsNum'])-1
        return html.Div([
                html.Div([
                    dcc.Tabs(
                            tabs=[
                                    {'label': 'Asset n° {}'.format(i+1), 'value': i} for i in range(int(self.MarketGraph.vs[self.AgentID]['AssetsNum']))
                                    ],
                            value=self.AssetID,
                            id='tab-assets',
                            vertical=True
                        )],
                    style={'width': '17%', 'float': 'left'}),
                html.Div(id='tab-assets-output',style={'width': '83%', 'float': 'right'})
                ], style={
                    'width': '100%',
                    'fontFamily': 'Sans-Serif',
                    'margin-left': 'auto',
                    'margin-right': 'auto'
                })
    
    def ShowAssetMenu(self,asset_tab_id):
        if int(self.MarketGraph.vs[self.AgentID]['AssetsNum'])==0:
            return []
        else:
            Asset_dict = self.MarketGraph.vs[self.AgentID]['Assets'][asset_tab_id]
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
                                                     options=[
                                                        {'label': 'Load', 'value': 'Load'},
                                                        {'label': 'Heat Pump', 'value': 'Heat Pump'},
                                                        {'label': 'Storage', 'value': 'Storage'},
                                                        {'label': 'EV', 'value': 'EV'},
                                                        {'label': 'PV', 'value': 'PV'},
                                                        {'label': 'Wind', 'value': 'Wind'},
                                                        {'label': 'Coal', 'value': 'Coal'},
                                                        {'label': 'Gas', 'value': 'Gas'},
                                                        {'label': 'Nuclear', 'value': 'Nuclear'}
                                                    ], 
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
    def ShowTabMarketMenu_Save(self,type_save='Save'):
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
    
    def ShowTabMarketMenu_SaveGraph(self,n_save=None,filename=None):
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
    def ShowTabMarketMenu_AddFile(self,filetype='Example',actiontype='Add'):
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
            drop = html.Div([dcc.Dropdown( id='market-menu-addfile-filename', value='****NEW****')], style={'display':'none'})
        else:
            if actiontype=='Open':
                button_chil = 'Open'
            else:
                button_chil = 'Add'
            entry = 'File:'
            drop = dcc.Dropdown( id='market-menu-addfile-filename', clearable=False,
                                options=[{'label':str(file[0:-6]),'value':str(file)} for file in os.listdir(self.current_dirpath) if file.endswith('.pyp2p')], 
                                value=self.current_filename)
        return html.Div([
                mark,
                html.Div([
                    html.Div([
                            html.Div([], style={'display':'table-cell','width':'10%'}),
                            html.Div([], style={'display':'table-cell','width':'40%'}),
                            html.Div([], style={'display':'table-cell','width':'10%'}),
                            html.Div([], style={'display':'table-cell','width':'10%'}),
                            html.Div([], style={'display':'table-cell','width':'30%'}),
                            ], style={'display':'table-row'}),
                    html.Div([
                        html.Div([entry], style={'display':'table-cell'}),
                        html.Div([drop], style={'display':'table-cell'}),
                        html.Div([
                                dcc.Input(id='market-menu-addfile-type', value=actiontype, style={'display':'none'})
                                ], style={'display':'table-cell'}),
                        html.Div([html.Button(children=button_chil, id = 'market-menu-addfile-button', type='submit', n_clicks=self.clicks_save)], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                        ], style={'display':'table','width':'100%'}),
                html.Div([], id='market-menu-addfile-message')
                ], id='market-menu-addfile-refresh')
    
    def ShowTabMarketMenu_AddFileMessage(self,n_add=None,filename=None,actiontype='Add'):
        if n_add is not None and self.clicks_save != n_add and filename is not None:
            self.clicks_save = n_add
            message = ''
            if actiontype=='Open' and filename=='****NEW****':
                self.MarketGraph = Graph(directed=True)
            elif actiontype=='Open':
                self.OpenMarketGraph(filename)
            elif actiontype=='Add':
                message = self.UnionMarketGraph(filename)
            return html.Div([
                    html.Button(children=message, id = 'market-menu-addfile-button-message', type='submit', n_clicks=0)
                    ], style={'display':'none'})
        else:
            return 
    
    
    #%% Market tab -- graph management -- Lists
    def ListAgentsID(self,show_self=True,show_type=None):
        if show_type is None and show_self:
            show_list = [self.MarketGraph.vs[i]['ID'] for i in range(len(self.MarketGraph.vs))]
        elif show_type is None and not show_self:
            show_list = [self.MarketGraph.vs[i]['ID'] for i in range(len(self.MarketGraph.vs)) if i!=self.AgentID]
        else:
            if show_self:
                show_list = [self.MarketGraph.vs[i]['ID'] for i in range(len(self.MarketGraph.vs)) if self.MarketGraph.vs[i]['Type']==show_type]
            else:
                show_list = [self.MarketGraph.vs[i]['ID'] for i in range(len(self.MarketGraph.vs)) if self.MarketGraph.vs[i]['Type']==show_type and i!=self.AgentID]
        return show_list 
    
    def ListAllowedPartners(self):
        exclusion_list = [self.MarketGraph.vs[self.AgentID].index]
        # Exclude all agents in the same community(ies)
        for x in self.MarketGraph.vs[self.AgentID]['Community']:
            exclusion_list.append(x)
            if not self.allow_P2P_within_community:
                exclusion_list.extend([self.MarketGraph.vs.select(ID=y)[0].index for y in self.MarketGraph.vs.select(ID=x)[0]['Community']])
        # Exclude trades 
        for x in self.MarketGraph.vs[self.AgentID]['Partners']:
            idx = self.MarketGraph.vs.select(ID=x)[0].index
            if self.MarketGraph.vs[idx]['Type']=='Manager':
                exclusion_list.extend([self.MarketGraph.vs.select(ID=y)[0].index for y in self.MarketGraph.vs[idx]['Community']])
            elif not self.allow_P2P_with_both_communitymanager_and_its_members:
                for y in self.MarketGraph.vs[idx]['Community']:
                    exclusion_list.append(self.MarketGraph.vs.select(ID=y)[0].index)
        return self.ListAgentsIndex(exclusion_list)
    
    def ListAllowedCommunities(self):
        # Exclude itself if is a manager and managers which are trading partners
        if self.MarketGraph.vs[self.AgentID]['Type'] == 'Manager':
            exclusion_list = [self.MarketGraph.vs[self.AgentID].index]
            if not self.allow_P2P_with_both_communitymanager_and_its_members:
                exclusion_list.extend([self.MarketGraph.vs.select(ID=x)[0].index for x in self.MarketGraph.vs[self.AgentID]['Partners']])
            return self.ListAgentsIndex(exclusion_list)
        else:
            inclusion_list = [x.index for x in self.MarketGraph.vs.select(Type='Manager') if x['ID'] not in self.MarketGraph.vs[self.AgentID]['Partners']]
            return inclusion_list
    
    #%% Market tab -- graph management -- Creation
    def CreateCommunity(self,n_agents,returnID=False):
        if self.update_graph:
            if not isinstance(n_agents,int):
                n_agents = int(n_agents)
            Ag_IDs = [self.CreateAgent(True) for i in range(n_agents+1)]
            self.AgentID = Ag_IDs.pop(0)
            self.MarketGraph.vs[self.AgentID]['name'] = 'Manager' + ' ' + str(self.AgentID+1)
            self.MarketGraph.vs[self.AgentID]['Type'] = 'Manager'
            self.MarketGraph.vs[self.AgentID]['Community'] = Ag_IDs
            self.MarketGraph.vs[self.AgentID]['CommPref'] = [self.default_community_preference for i in range(n_agents)]
            self.CreatePartnership()
        if returnID:
            return self.AgentID
    
    def CreateAgent(self,returnID=False):
        if self.update_graph:
            self.AgentName = 'Agent' + ' ' + str(self.maxID+1)
            self.MarketGraph.add_vertex(name=self.AgentName,ID=self.maxID,Type='Agent',
                                        AssetsNum=1,Assets=[self.default_asset.copy()],
                                        Partners=[],Preferences=[],Community=[],CommPref=[],CommGoal=None)
            self.AgentID = self.MarketGraph.vs.find(ID=self.maxID).index
            self.maxID += 1
        if returnID:
            return self.AgentID
    
    def CreateAsset(self):
        for i in range(len(self.MarketGraph.vs[self.AgentID]['Assets']),int(self.MarketGraph.vs[self.AgentID]['AssetsNum'])):
            asset_dict = self.default_asset.copy()
            asset_dict['id'] = i
            asset_dict['name'] = 'Asset '+ str(i+1)
            self.MarketGraph.vs[self.AgentID]['Assets'].append(asset_dict)
    
    #%% Market tab -- graph management -- Changes
    def AgentType(self,agent_type):
        self.MarketGraph.vs[self.AgentID]['Type'] = agent_type
        return self.ShowTabMarketMenu_AgentData()
    
    def AgentChange(self,agent_name,comm_goal,agent_n_assets):
        self.AgentName = agent_name
        self.MarketGraph.vs[self.AgentID]['name'] = agent_name
        self.MarketGraph.vs[self.AgentID]['CommGoal'] = comm_goal
        self.MarketGraph.vs[self.AgentID]['AssetsNum'] = agent_n_assets
        self.CreateAsset()
        return self.ShowAssetsMenu()
    
    def AgentPartners(self,agent_partners,agent_preferences):
        self.MarketGraph.vs[self.AgentID]['Partners'] = agent_partners
        return self.AgentPreferences(agent_preferences)
    
    def AgentCommunity(self,agent_community,agent_commpref):
        self.MarketGraph.vs[self.AgentID]['Community'] = agent_community
        return self.AgentCommPref(agent_commpref)
    
    def AgentChangeNAssets(self,agent_n_assets):
        if self.MarketGraph.vs[self.AgentID]['Type'] == 'Manager':
            self.MarketGraph.vs[self.AgentID]['AssetsNum'] = 0
        else:
            self.MarketGraph.vs[self.AgentID]['AssetsNum'] = agent_n_assets
        self.CreateAsset()
        return self.ShowAssetsMenu()
    
    def AssetChange(self,asset_name,asset_type,asset_costfct,asset_costfct_coeff,asset_p_bounds_up,asset_p_bounds_low):
        Asset_dict = self.MarketGraph.vs[self.AgentID]['Assets'][self.AssetID]
        Asset_dict['name'] = asset_name
        Asset_dict['type'] = asset_type
        Asset_dict['costfct'] = asset_costfct
        Asset_dict['costfct_coeff'] = [float(x) for x in asset_costfct_coeff.split(',')]
        Asset_dict['p_bounds_up'] = asset_p_bounds_up
        Asset_dict['p_bounds_low'] = asset_p_bounds_low
        self.MarketGraph.vs[self.AgentID]['Assets'][self.AssetID] = Asset_dict
        return []
    
    def AgentPreferences(self,Pref=[]):
        if isinstance(Pref, str):
            Pref = [float(x) for x in Pref.split(',') if x!='' and x!=' ']
        if Pref!=[]:
            self.MarketGraph.vs[self.AgentID]['Preferences'] = Pref
        for i in range( len(self.MarketGraph.vs[self.AgentID]['Partners']) - len(self.MarketGraph.vs[self.AgentID]['Preferences']) ):
            self.MarketGraph.vs[self.AgentID]['Preferences'].append(float(self.default_partnership_preference))
        self.CreatePartnership()
        return self.ShowTabMarketMenu_Preferences()
    
    def AgentCommPref(self,Pref=[]):
        if isinstance(Pref, str):
            Pref = [float(x) for x in Pref.split(',') if x!='' and x!=' ']
        if Pref!=[]:
            self.MarketGraph.vs[self.AgentID]['CommPref'] = Pref
        for i in range( len(self.MarketGraph.vs[self.AgentID]['Community']) - len(self.MarketGraph.vs[self.AgentID]['CommPref']) ):
            self.MarketGraph.vs[self.AgentID]['CommPref'].append(float(self.default_partnership_preference))
        self.CreatePartnership()
        return self.ShowTabMarketMenu_CommPref()
    
    def CreatePartnership(self,idx=None):
        if idx is None:
            idx = self.AgentID
        # Delete some edges if too many
        Edges = self.MarketGraph.es.select(_source=idx)
        if len(Edges) > (len(self.MarketGraph.vs[idx]['Partners']) + len(self.MarketGraph.vs[idx]['Community']) ):
            to_del = []
            for x in Edges:
                if self.MarketGraph.vs[x.tuple[1]]['ID'] not in self.MarketGraph.vs[idx]['Partners'] and self.MarketGraph.vs[x.tuple[1]]['ID'] not in self.MarketGraph.vs[idx]['Community']:
                    self.DeletePartnership(x.tuple[0],x.tuple[1])
                    to_del.append(x.index)
                        
            for x in self.MarketGraph.es.select(_target=idx):
                if self.MarketGraph.vs[x.tuple[0]]['ID'] not in self.MarketGraph.vs[idx]['Partners'] and self.MarketGraph.vs[x.tuple[0]]['ID'] not in self.MarketGraph.vs[idx]['Community']:
                    to_del.append(x.index)
            self.MarketGraph.delete_edges(to_del)
            
        # Update and/or add edges
        Edges = self.MarketGraph.es.select(_source=idx)
        c_target = []
        for x in Edges:
            c_target.append(x.tuple[1])
        for i in range(len(self.MarketGraph.vs[idx]['Partners'])):
            idp = self.MarketGraph.vs.find(ID=self.MarketGraph.vs[idx]['Partners'][i]).index
            if idp not in c_target:
                self.MarketGraph.add_edge(idx,idp,weight=float(self.MarketGraph.vs[idx]['Preferences'][i]))
                self.MarketGraph.add_edge(idp,idx,weight=float(self.default_partnership_preference))
                self.MarketGraph.vs[idp]['Partners'].append(self.MarketGraph.vs[idx]['ID'])
                self.MarketGraph.vs[idp]['Preferences'].append(float(self.default_partnership_preference))
            else:
                for x in Edges.select(_target=idp):
                    self.MarketGraph.es[x.index]['weight']=float(self.MarketGraph.vs[idx]['Preferences'][i])
        for i in range(len(self.MarketGraph.vs[idx]['Community'])):
            idc = self.MarketGraph.vs.find(ID=self.MarketGraph.vs[idx]['Community'][i]).index
            if idc not in c_target:
                self.MarketGraph.add_edge(idx,idc,weight=float(self.MarketGraph.vs[idx]['CommPref'][i]))
                self.MarketGraph.add_edge(idc,idx,weight=float(self.default_community_preference))
                self.MarketGraph.vs[idc]['Community'].append(self.MarketGraph.vs[idx]['ID'])
                self.MarketGraph.vs[idc]['CommPref'].append(float(self.default_community_preference))
            else:
                for x in Edges.select(_target=idc):
                    self.MarketGraph.es[x.index]['weight']=float(self.MarketGraph.vs[idx]['CommPref'][i])
    
    def CommunityChange(self,comm_name,comm_goal,comm_members):
        self.AgentName = comm_name
        self.MarketGraph.vs[self.AgentID]['name'] = comm_name
        self.MarketGraph.vs[self.AgentID]['CommGoal'] = comm_goal
        comm_members = comm_members.split(',')
        for i in range( min(len(self.MarketGraph.vs[self.AgentID]['Community']),len(comm_members)) ):
            self.MarketGraph.vs.select( ID=self.MarketGraph.vs[self.AgentID]['Community'][i] )[0]['name'] = comm_members[i]
        return []
    
    #%% Market tab -- graph management -- Suppresions
    def DeletePartnership(self,id_from,id_to):
        if self.MarketGraph.vs[id_from]['ID'] in self.MarketGraph.vs[id_to]['Partners']:
            if self.MarketGraph.vs[id_from]['ID'] in self.MarketGraph.vs[id_to]['Partners']:
                id_del = self.MarketGraph.vs[id_to]['Partners'].index(self.MarketGraph.vs[id_from]['ID'])
                useless = self.MarketGraph.vs[id_to]['Partners'].pop(id_del)
                useless = self.MarketGraph.vs[id_to]['Preferences'].pop(id_del)
            if self.MarketGraph.vs[id_to]['ID'] in self.MarketGraph.vs[id_from]['Partners']:
                id_del = self.MarketGraph.vs[id_from]['Partners'].index(self.MarketGraph.vs[id_to]['ID'])
                useless = self.MarketGraph.vs[id_from]['Partners'].pop(id_del)
                useless = self.MarketGraph.vs[id_from]['Preferences'].pop(id_del)
        elif self.MarketGraph.vs[id_from]['ID'] in self.MarketGraph.vs[id_to]['Community']:
            if self.MarketGraph.vs[id_from]['ID'] in self.MarketGraph.vs[id_to]['Community']:
                id_del = self.MarketGraph.vs[id_to]['Community'].index(self.MarketGraph.vs[id_from]['ID'])
                useless = self.MarketGraph.vs[id_to]['Community'].pop(id_del)
                useless = self.MarketGraph.vs[id_to]['CommPref'].pop(id_del)
            if self.MarketGraph.vs[id_to]['ID'] in self.MarketGraph.vs[id_from]['Community']:
                id_del = self.MarketGraph.vs[id_from]['Community'].index(self.MarketGraph.vs[id_to]['ID'])
                useless = self.MarketGraph.vs[id_from]['Community'].pop(id_del)
                useless = self.MarketGraph.vs[id_from]['CommPref'].pop(id_del)
    
    def DeleteAssets(self,delete_asset=[]):
        for i in range(int(self.MarketGraph.vs[self.AgentID]['AssetsNum']),len(self.MarketGraph.vs[self.AgentID]['Assets'])):
            useless = self.MarketGraph.vs[self.AgentID]['Assets'].pop()
        delete_asset.sort(reverse=True)
        for i in delete_asset:
            useless = self.MarketGraph.vs[self.AgentID]['Assets'].pop(i)
        if delete_asset!=[]:
            self.MarketGraph.vs[self.AgentID]['AssetsNum'] = str(len(self.MarketGraph.vs[self.AgentID]['Assets']))
    
    def DeleteAgent(self,del_id=None):
        if del_id is None:
            del_id = self.AgentID
        for x in self.MarketGraph.vs[del_id]['Partners']:
            for y in self.MarketGraph.vs.select(ID=x):
                self.DeletePartnership(del_id,y.index)
        for x in self.MarketGraph.vs[del_id]['Community']:
            for y in self.MarketGraph.vs.select(ID=x):
                self.DeletePartnership(del_id,y.index)
        self.MarketGraph.delete_vertices(del_id)
    
    def DeleteCommunity(self,del_id=None):
        if del_id is None:
            del_id = self.AgentID
        if self.MarketGraph.vs[del_id]['Type']=='Manager':
            for i in range(len(self.MarketGraph.vs[del_id]['Community'])):
                for y in self.MarketGraph.vs.select(ID=self.MarketGraph.vs[del_id]['Community'][0]):
                    self.DeleteAgent(y.index)
            self.DeleteAgent(del_id)
    
    #%% Market tab -- graph management -- Save & Open & Add from file
    def SaveMarketGraph(self,filename=None):
        if filename is None:
            filename = self.current_filename
        if not filename.endswith('.pyp2p'):
            filename += '.pyp2p'
        self.MarketGraph.save(self.current_dirpath+'/'+filename, format='picklez')
        self.current_filename = filename
        return 'The graph has been saved.'
    
    def LoadMarketGraph(self,filename=None):
        if filename is None:
            filename = self.current_filename
        if not filename.endswith('.pyp2p'):
            filename += '.pyp2p'
        return load(self.current_dirpath+'/'+filename, format='picklez'), filename
    
    def OpenMarketGraph(self,filename=None):
        NewMarket,filename = self.LoadMarketGraph(filename)
        if self.VerifyMarketGraphFormat(NewMarket):
            self.MarketGraph = NewMarket
            self.current_filename = filename
        return
    
    def UnionMarketGraph(self,filename=None):
        NewMarket,useless = self.LoadMarketGraph(filename)
        if self.VerifyMarketGraphFormat(NewMarket):
            Ag_IDs = [self.CreateAgent(True) for i in range(len(NewMarket.vs))]
            for i in range(len(NewMarket.vs)):
                for att in self.default_vertex_attributes:
                    if att != 'ID':
                        self.MarketGraph.vs[Ag_IDs[i]][att] = NewMarket.vs[i][att]
            for i in range(len(NewMarket.es)):
                self.MarketGraph.add_edge(Ag_IDs[NewMarket.es[i].source], Ag_IDs[NewMarket.es[i].target], weight=NewMarket.es[i]['weight'])
            return ''
        else:
            return 'Wrong file format.'
    
    def VerifyMarketGraphFormat(self,NewMarket=None):
        output = False
        if NewMarket is not None:
            self.default_vertex_attributes = ['ID', 'Type', 'AssetsNum', 'Assets', 'Partners', 'Preferences', 'Community', 'CommPref', 'CommGoal', 'name']
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
    