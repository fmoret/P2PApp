# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 11:04:59 2018

@author: Thomas
"""

"""
    File managing TestGen layout
"""

#import datetime
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

class expando(object):
    pass

class TestGenTab:
    def __init__(self):
        self.ShareWidth()
        self.__init__defaults__()
        self.__init__general__()
        self.__init__params__()
        self.titles_style = {'margin-bottom':'0.5em'}
        self.n_clicksG_default = 0
        self.n_clicksP_default = 0
        self.n_clicks_generate = 0
        return
    
    def __init__defaults__(self):
        # set Tags for callback and generic function generators
        self.Tags = ['Ngen','Same','Coverage','Wind']
        self.GenericTags = [
                {'var':'Nhouse' ,'solar':True  ,'name':'Houses'               ,'type':'consumption' ,'controlable':True },
                {'var':'Nstore' ,'solar':True  ,'name':'Stores'               ,'type':'consumption' ,'controlable':True },
                {'var':'Nflats' ,'solar':True  ,'name':'Flats'                ,'type':'consumption' ,'controlable':True },
                {'var':'Nmall'  ,'solar':True  ,'name':'Malls'                ,'type':'consumption' ,'controlable':True },
                {'var':'Nfact'  ,'solar':False ,'name':'Factories'            ,'type':'consumption' ,'controlable':True },
                {'var':'Nplant' ,'solar':False ,'name':'Thermal power plants' ,'type':'production'  ,'controlable':True },
                {'var':'Nwind'  ,'solar':False ,'name':'Wind farms'           ,'type':'production'  ,'controlable':False},
                ]
        self.GenereciText = {
                'Nhouse':'Number of houses:',
                'Nstore':'Number of small stores:',
                'Nflats':'Number of builfings with flats:',
                'Nmall':'Number of malls:',
                'Nfact':'Number of factoties:',
                'Nplant':'Number of thermal power plant:',
                'Nwind':'Number of wind farms:',
                }
        self.GenereciTitles = {
                'Nhouse':'Number of houses with all its appliances (water heater, TV, ...)',
                'Nstore':'Number of small stores (each using solely one edifice)',
                'Nflats':'Number of buildings with several appartments within',
                'Nmall':'Number of buildings with several stores within',
                'Nfact':'Number of factories',
                'Nplant':'Number of thermal power plant (total production capacity share between all thermal plants and wind farms)',
                'Nwind':'Number of wind farms (total production capacity share between all thermal plants and wind farms)',
                }
        # default parameters
        self.default = expando()
        self.default.G = expando()
        self.default.S = expando()
        self.default.R = expando()
        self.default.Max_Solar_Penetration = expando()
        self.default.Power_min = expando()
        self.default.Power_max = expando()
        self.default.Price_min = expando()
        self.default.Price_max = expando()
        self.default.Max_Solar_Installed = expando()
        self.default.Solar_Installed = expando()
        # variables associated to self.Tags
        self.default.G.Ngen = 1
        self.default.G.Same = True
        self.default.Max_Coverage = 150             # in %
        self.default.S.Prod_Coverage = 100          # in %
        self.default.S.Prod_Wind_share = 20         # in %
        self.default.R.Prod_Coverage = [90,110]     # in %
        self.default.R.Prod_Wind_share = [10,20]    # in %
        # variables associated to self.GenericTags
        # for Nhouse
        self.default.S.Nhouse = 15                      # number (int)
        self.default.R.Nhouse = [10,20]                 # numbers (int)
        self.default.S.Nhouse_solar = 10                # in %
        self.default.R.Nhouse_solar = [0,20]            # in %
        self.default.Max_Solar_Penetration.Nhouse = 100 # in %
        self.default.Power_min.Nhouse = [2,4]           # in kW
        self.default.Power_max.Nhouse = [5,8]           # in kW
        self.default.Price_min.Nhouse = [11,13.5]       # in c$/kWh
        self.default.Price_max.Nhouse = [14.5,17]       # in c$/kWh
        self.default.Max_Solar_Installed.Nhouse = 120   # in %
        self.default.Solar_Installed.Nhouse = [20,60]   # in %
        # for Nstore
        self.default.S.Nstore = 5                       # numbers (int)
        self.default.R.Nstore = [2,8]                   # numbers (int)
        self.default.S.Nstore_solar = 20                # in %
        self.default.R.Nstore_solar = [0,60]            # in %
        self.default.Max_Solar_Penetration.Nstore = 100 # in %
        self.default.Power_min.Nstore = [5,9]           # in kW
        self.default.Power_max.Nstore = [12,36]         # in kW
        self.default.Price_min.Nstore = [10,12]         # in c$/kWh
        self.default.Price_max.Nstore = [15,19]         # in c$/kWh
        self.default.Max_Solar_Installed.Nstore = 120   # in %
        self.default.Solar_Installed.Nstore = [30,80]   # in %
        # for Nflats
        self.default.S.Nflats = 10                      # number (int)
        self.default.R.Nflats = [10,20]                 # numbers (int)
        self.default.S.Nflats_solar = 20                # in %
        self.default.R.Nflats_solar = [0,50]            # in %
        self.default.Max_Solar_Penetration.Nflats = 100 # in %
        self.default.Power_min.Nflats = [] # in kW
        self.default.Power_max.Nflats = [] # in kW
        self.default.Price_min.Nflats = [11,13.5]       # in c$/kWh
        self.default.Price_max.Nflats = [14.5,17]       # in c$/kWh
        self.default.Max_Solar_Installed.Nflats = 120   # in %
        self.default.Solar_Installed.Nflats = [5,30]    # in %
        # for Nmall
        self.default.S.Nmall = 3                        # numbers (int)
        self.default.R.Nmall = [0,5]                    # numbers (int)
        self.default.S.Nmall_solar = 33                 # in %
        self.default.R.Nmall_solar = [0,66]             # in %
        self.default.Max_Solar_Penetration.Nmall = 100  # in %
        self.default.Power_min.Nmall = [] # in kW
        self.default.Power_max.Nmall = [] # in kW
        self.default.Price_min.Nmall = [10,12]          # in c$/kWh
        self.default.Price_max.Nmall = [15,19]          # in c$/kWh
        self.default.Max_Solar_Installed.Nmall = 120    # in %
        self.default.Solar_Installed.Nmall = [5,30]     # in %
        # for Nfact
        self.default.S.Nfact = 6                        # numbers (int)
        self.default.R.Nfact = [3,9]                    # numbers (int)
        self.default.S.Nfact_solar = 0                  # in %
        self.default.R.Nfact_solar = [0,33]             # in %
        self.default.Max_Solar_Penetration.Nfact = 100  # in %
        self.default.Power_min.Nfact = [5,9]            # in kW
        self.default.Power_max.Nfact = [36,100]         # in kW
        self.default.Price_min.Nfact = [9,10]           # in c$/kWh
        self.default.Price_max.Nfact = [15,19]          # in c$/kWh
        self.default.Max_Solar_Installed.Nfact = 120    # in %
        self.default.Solar_Installed.Nfact = []     # in %
        # for Nplant
        self.default.S.Nplant = 7                       # numbers (int)
        self.default.R.Nplant = [5,10]                  # numbers (int)
        self.default.Price_min.Nplant = [12,14]         # in c$/kWh
        self.default.Price_max.Nplant = [17,20]         # in c$/kWh
        # for Nwind
        self.default.S.Nwind = 4                        # numbers (int)
        self.default.R.Nwind = [0,8]                    # numbers (int)
        return
    
    def __init__general__(self):
        # current parameters
        self.G = expando()
        self.S = expando()
        self.R = expando()
        # variables associated to self.Tags
        self.G.Ngen = self.default.G.Ngen
        self.G.Same = self.default.G.Same
        self.S.Prod_Coverage = self.default.S.Prod_Coverage
        self.S.Prod_Wind_share = self.default.S.Prod_Wind_share
        self.R.Prod_Coverage = self.default.R.Prod_Coverage
        self.R.Prod_Wind_share = self.default.R.Prod_Wind_share
        # variables associated to self.GenericTags
        for tag in self.GenericTags:
            setattr(self.S,tag['var'], getattr(self.default.S,tag['var']) )
            setattr(self.R,tag['var'], getattr(self.default.R,tag['var']) )
            if tag['solar']:
                setattr(self.S,f"{tag['var']}_solar", getattr(self.default.S,f"{tag['var']}_solar") )
                setattr(self.R,f"{tag['var']}_solar", getattr(self.default.R,f"{tag['var']}_solar") )
        return
    
    def __init__params__(self):
        self.Power_min = expando()
        self.Power_max = expando()
        self.Price_min = expando()
        self.Price_max = expando()
        self.Solar_Installed = expando()
        # variables associated to self.GenericTags
        for tag in self.GenericTags:
            if tag['controlable']:
                setattr(self.Price_min,tag['var'], getattr(self.default.Price_min,tag['var']) )
                setattr(self.Price_max,tag['var'], getattr(self.default.Price_max,tag['var']) )
                if tag['type']=='consumption':
                    setattr(self.Power_min,tag['var'], getattr(self.default.Power_min,tag['var']) )
                    setattr(self.Power_max,tag['var'], getattr(self.default.Power_max,tag['var']) )
                    if tag['solar']:
                        setattr(self.Solar_Installed,tag['var'], getattr(self.default.Solar_Installed,tag['var']) )
        return
    
    def ShareWidth(self,menu=None,graph=None):
        if menu is None:
            menu='50%'
        if graph is None:
            graph='50%'
        self.share_width_menu = menu
        self.share_width_graph = graph
        self.defaultTablel = html.Div([
                html.Div([], style={'display':'table-cell','width':'35%'}),
                html.Div([], style={'display':'table-cell','width':'30%'}),
                html.Div([], style={'display':'table-cell','width':'3%'}),
                html.Div([], style={'display':'table-cell','width':'15%'}),
                ], style={'display':'table-row'})
        self.defaultTabler = html.Div([
                html.Div([], style={'display':'table-cell','width':'35%'}),
                html.Div([], style={'display':'table-cell','width':'25%'}),
                html.Div([], style={'display':'table-cell','width':'3%'}),
                html.Div([], style={'display':'table-cell','width':'37%'}),
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
                    html.Div(menu_data, style={'width':width_menu,'display':'inline-block','vertical-align':'top'}),
                    html.Div(graph_data, style={'width':width_graph,'display':'inline-block','vertical-align':'top'}),
                ], style= {'width': '100%', 'display': 'block'}),
                html.Div([
                    html.Hr()
                    ],style={'width':'95%','padding-bottom':'0.5em','margin':'auto'}),
                html.Div(bottom_data, style= {'width': '100%', 'display': 'block'})
            ], id='gen-main-tab')
    
    def ShowTab(self):
        menu_data = [self.GeneralMenu()]
        graph_data = [self.ParamsMenu()]
        bottom_data = [self.GenerateMenu()]
        return self.MenuTab(menu_data,graph_data,bottom_data)
    
    
    #%% Menu -- General setup
    def GeneralMenu(self):
        return html.Div([
                html.Div([html.Div([
                        html.Div([
                                html.H4('General information',style=self.titles_style, title='Parameters of the generator itself'),
                                ], style={'width':'75%','display':'table-cell'}),
                        html.Div([
                                html.Button(children='Set to default', type='submit', id='gen-general-default', n_clicks=self.n_clicksG_default)
                                ], style={'width':'25%','display':'table-cell'}),
                        ],style={'display':'table-row'}),],style={'display':'table','width':'100%'}),
                html.Div(id='gen-general-refresh')
               ])
    
    def GeneralMenuDefault(self,n_clicks=None):
        if n_clicks is not None and n_clicks!=self.n_clicksG_default:
            self.n_clicksG_default = n_clicks
            self.__init__general__()
        return [html.Div([
                    self.defaultTablel,
                    html.Div([
                            html.Div(['Number of test cases:'], style={'display':'table-cell'}, 
                                     title='Number of test cases to generate'),
                            html.Div([
                                    dcc.Input(type='number',min=1,step=1,value=self.G.Ngen, id='gen-general-Ngen')
                                    ], style={'display':'table-cell'}),
                            html.Div(id='gen-general-Ngen-sel',style={'display':'none'}),
                        ], style={'display':'table-row','padding-bottom':'0.5em'}),
                    html.Div([
                            html.Div(['Use the same composition for all test cases:'], style={'display':'table-cell'}, 
                                     title='Should all test cases be composed of the same elements?'),
                            html.Div([self.SameShowRefresh()
                                    ], style={'display':'table-cell','padding-bottom':'0.5em'},id='gen-general-Same-show'),
                        ], style=self.SameShowHide(),id='gen-general-Same-row'),
                ], style={'display':'table','width':'100%'}),
                html.Div(id='gen-general-Same-sel', style={'margin-bottom':'1em'}),
                ]
    
    def SameShowRefresh(self,click=None):
        if self.G.Ngen == 1:
            self.G.Same = True
        return dcc.RadioItems(id='gen-general-Same', labelStyle={'display': 'block'}, 
                             value=self.G.Same,
                             options=[
                                {'label': 'Yes', 'value': True},
                                {'label': 'No', 'value': False},
                            ])
    
    def SameShowHide(self,click=None):
        if self.G.Ngen > 1:
            return {'display':'table-row'}
        else:
            return {'display':'none'}
    
    def Ngen(self,Ngen=None):
        if Ngen is not None:
            if self.G.Ngen!=int(Ngen):
                self.G.Ngen = int(Ngen)
                out = [html.Button(children='',type='submit',id='gen-general-Same-hide',n_clicks=1)]
                if self.G.Ngen == 1 and not self.G.Same:
                    out.append(
                            html.Button(children='',type='submit',id='gen-general-Same-refresh',n_clicks=1)
                            )
                return out
        
    def Same(self,Same=None):
        if Same is not None:
            self.G.Same = bool(Same)
        compo = [self.defaultTablel]
        compo.extend(self.GenericMenu())
        if self.G.Same:
            return html.Div([
                    html.Div([
                        self.defaultTablel,
                        html.Div([
                                html.Div(['Production coverage:'], style={'display':'table-cell'}, 
                                         title='Production capacity vs. Consumption capacity'),
                                html.Div([
                                        dcc.Slider(min=0,max=self.default.Max_Coverage, value=self.S.Prod_Coverage, id='gen-general-Coverage')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id='gen-general-Coverage-sel', style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                        html.Div([
                                html.Div(['Wind production share:'], style={'display':'table-cell'}, 
                                         title='Installed wind capacity vs. Total production capacity'),
                                html.Div([
                                        dcc.Slider(min=0,max=100,value=self.S.Prod_Wind_share, id='gen-general-Wind')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id='gen-general-Wind-sel', style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.H4('Cases composition',style=self.titles_style),
                    html.Div(compo, style={'display':'table','width':'100%'}),
                ], style={'margin-bottom':'1em'})
        else:
            return html.Div([
                    html.Div([
                        self.defaultTablel,
                        html.Div([
                                html.Div(['Production coverage:'], style={'display':'table-cell'}, 
                                         title='Production capacity vs. Consumption capacity'),
                                html.Div([
                                        dcc.RangeSlider(min=0,max=self.default.Max_Coverage,step=1, value=self.R.Prod_Coverage, id='gen-general-Coverage')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id='gen-general-Coverage-sel', style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                        html.Div([
                                html.Div(['Wind production share:'], style={'display':'table-cell'}, 
                                         title='Installed wind capacity vs. Total production capacity'),
                                html.Div([
                                        dcc.RangeSlider(min=0,max=100,step=1,value=self.R.Prod_Wind_share, id='gen-general-Wind')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id='gen-general-Wind-sel', style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                    ], style={'display':'table','width':'100%'}),
                    html.H4('Cases composition',style=self.titles_style),
                    html.Div(compo, style={'display':'table','width':'100%'}),
                ], style={'margin-bottom':'1em'})
    
    def Coverage(self,Coverage=None):
        if Coverage is not None:
            if isinstance(Coverage,list):
                self.R.Prod_Coverage = [int(i) for i in Coverage]
                return f' {self.R.Prod_Coverage}%'
            else:
                self.S.Prod_Coverage = int(Coverage)
                return f' {self.S.Prod_Coverage}%'
        else:
            return
    
    def Wind(self,Wind=None):
        if Wind is not None:
            if isinstance(Wind,list):
                self.R.Prod_Wind_share = [int(i) for i in Wind]
                return f' {self.R.Prod_Wind_share}%'
            else:
                self.S.Prod_Wind_share = int(Wind)
                return f' {self.S.Prod_Wind_share}%'
        else:
            return
    
    #%% Generic Tags functions
    def GenericMenu(self,tags=None):
        if tags is None:
            tags = self.GenericTags
        out = []
        if self.G.Same:
            for tag in tags:
                if tag['solar']:
                    padd = '0em'
                else:
                    padd = '.5em'
                out.extend([ html.Div([
                            html.Div([self.GenereciText[tag['var']]], style={'display':'table-cell'}, title=self.GenereciTitles[tag['var']]),
                            html.Div([
                                    dcc.Input(type='number', min=0,step=1, value=getattr(self.S,tag['var']) , id=f'gen-general-{tag["var"]}')
                                    ], style={'display':'table-cell','padding-bottom':padd}),
                            html.Div(id=f'gen-general-{tag["var"]}-sel', style={'display':'none'}),
                        ], style={'display':'table-row'}),
#                        html.Div(style={'display':'table-row'},id=f'gen-general-{tag["var"]}-show')
                    ])
                if tag['solar']:
                    out.append( html.Div([
                                html.Div(['Part owning solar PV panels:'], style={'display':'table-cell','padding-left':'3%','padding-bottom':'.5em'}, 
                                             title='Percentage with PV panels installed on the roof'),
                                html.Div([
                                        dcc.Slider(min=0,max=getattr(self.default.Max_Solar_Penetration,tag['var']), step=1,
                                                   value=getattr(self.S,f'{tag["var"]}_solar'), id=f'gen-general-{tag["var"]}-solar')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id=f'gen-general-{tag["var"]}-solar-sel', style={'display':'table-cell'}),
                            ], style={'display':'table-row'}) 
                        )
        else:
            for tag in tags:
                if tag['solar']:
                    padd = '0em'
                else:
                    padd = '.5em'
                out.extend([ html.Div([
                            html.Div([self.GenereciText[tag['var']]], style={'display':'table-cell'}, title=self.GenereciTitles[tag['var']]),
                            html.Div([
                                    dcc.Input(type='text', value=f'{getattr(self.R,tag["var"])}', id=f'gen-general-{tag["var"]}'),
                                    ], style={'display':'table-cell','padding-bottom':padd}),
                            html.Div(style={'display':'table-cell'}),
                            html.Div(id=f'gen-general-{tag["var"]}-sel', style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
#                        html.Div(style={'display':'table-row'},id=f'gen-general-{tag["var"]}-show')
                    ])
                if tag['solar']:
                    out.append( html.Div([
                                html.Div(['Part owning solar PV panels:'], style={'display':'table-cell','padding-left':'3%','padding-bottom':'.5em'}, 
                                             title='Percentage with PV panels installed on the roof'),
                                html.Div([
                                        dcc.RangeSlider(min=0,max=getattr(self.default.Max_Solar_Penetration,tag['var']), step=1,
                                                   value=getattr(self.R,f'{tag["var"]}_solar'), id=f'gen-general-{tag["var"]}-solar')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id=f'gen-general-{tag["var"]}-solar-sel', style={'display':'table-cell'}),
                            ], style={'display':'table-row'}) 
                        )
        return out
    
    def GenericFct(self,name):
        def fct(value):
            if value is not None:
                if isinstance(value,str):
                    val = self.String2List(value)
                    setattr(self.R, name, val)
                    return f' {getattr(self.R,name)}'
#                    return [html.Div([f' {getattr(self.R,name)}']),
#                            html.Div([
#                                    html.Button(children='', id=f'gen-general-{name}-click', type='submit', n_clicks=0)
#                                    ],style={'display':'none'}),
#                            ]
                elif isinstance(value,int) or isinstance(value,float):
                    setattr(self.S, name, int(value))
                    return f' {getattr(self.S,name)}'
#                    return [html.Div([f' {getattr(self.S,name)}']),
#                            html.Div([
#                                    html.Button(children='', id=f'gen-general-{name}-click', type='submit', n_clicks=0)
#                                    ],style={'display':'none'}),
#                            ]
        return fct
    
    def String2List(self,value):
        if value.find('[')>-1:
            value = value[value.find('[')+1:]
        if value.find(']')>-1:
            value = value[:value.find('[')]
        value = value.replace(' ','')
        value = value.split(',')
        val = []
        for i in range(len(value)):
            try:
                x=int(float(value[i]))
            except ValueError:
                x=-1
            if x>=0:
                val.append(x)
        for i in range(len(val),2):
            val.append(0)
        val.sort()
        if len(val)>2:
            val = [val[0],val[-1]]
        return val
    
    def GenericFctSolar(self,name):
        def fct(value):
            if value is not None:
                if isinstance(value,list):
                    val = [int(float(i)) for i in value]
                    setattr(self.R, f"{name}_solar", val)
                    return f' {getattr(self.R,f"{name}_solar")} %'
                elif isinstance(value,int):
                    setattr(self.S, f"{name}_solar", int(float(value)))
                    return f' {getattr(self.S,f"{name}_solar")} %'
        return fct
    
    
    
    #%% Menu -- Characteristics
    def ParamsMenu(self):
        return html.Div([
                html.Div([html.Div([
                        html.Div([
                                html.H4('Items characteristics:', style=self.titles_style, title='Characteristics of controlable elements')
                                ], style={'width':'66%','display':'table-cell'}),
                        html.Div([
                                html.Button(children='Set to default', type='submit', id='gen-params-default', n_clicks=self.n_clicksP_default)
                                ], style={'width':'34%','display':'table-cell'}),
                        ],style={'display':'table-row'}),],style={'display':'table','width':'100%'}),
                html.Div(id='gen-params-refresh')
               ])
    
    def ParamsMenuDefault(self,n_clicks=None):
        if n_clicks is not None and n_clicks!=self.n_clicksP_default:
            self.n_clicksP_default = n_clicks
            self.__init__params__()
        return self.GenericMenuParams()
    
    def GenericMenuParams(self,tags=None):
        if tags is None:
            tags = self.GenericTags
        out = []
        for tag in tags:
            if tag['controlable']:
                if tag['type']=='consumption':
                    padd = '0.25em'
                else:
                    padd = '0em'
                mess = [self.defaultTabler,
                        html.Div([
                            html.Div(["Lower price:"], style={'display':'table-cell','padding-botton':'0.25em'}, title="Lower price's range"),
                            html.Div([
                                    dcc.Input(type='text', value=f'{getattr(self.Price_min,tag["var"])}', id=f'gen-params-Price-min-{tag["var"]}')
                                    ], style={'display':'table-cell'}),
                            html.Div(style={'display':'table-cell'}),
                            html.Div(id=f'gen-params-Price-min-{tag["var"]}-sel', style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                        html.Div([
                            html.Div(["Upper price:"], style={'display':'table-cell'}, title="Upper price's range"),
                            html.Div([
                                    dcc.Input(type='text', value=f'{getattr(self.Price_max,tag["var"])}', id=f'gen-params-Price-max-{tag["var"]}')
                                    ], style={'display':'table-cell'}),
                            html.Div(style={'display':'table-cell'}),
                            html.Div(id=f'gen-params-Price-max-{tag["var"]}-sel', style={'display':'table-cell'}),
                        ], style={'display':'table-row'})
                    ]
                if tag['type']=='consumption':
                    if tag['solar']:
                        padd = '0.25em'
                    else:
                        padd = '0em'
                    mess.extend([
                            html.Div([
                                html.Div(["Lower cunsumption:"], style={'display':'table-cell','padding-botton':'0.25em'}, title="Lower cunsumption's range"),
                                html.Div([
                                        dcc.Input(type='text', value=f'{getattr(self.Power_min,tag["var"])}', id=f'gen-params-Power-min-{tag["var"]}')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id=f'gen-params-Power-min-{tag["var"]}-sel', style={'display':'table-cell'}),
                            ], style={'display':'table-row'}),
                            html.Div([
                                html.Div(["Upper consumption:"], style={'display':'table-cell','padding-botton':padd}, title="Upper consumption's range"),
                                html.Div([
                                        dcc.Input(type='text', value=f'{getattr(self.Power_max,tag["var"])}', id=f'gen-params-Power-max-{tag["var"]}')
                                        ], style={'display':'table-cell'}),
                                html.Div(style={'display':'table-cell'}),
                                html.Div(id=f'gen-params-Power-max-{tag["var"]}-sel', style={'display':'table-cell'}),
                                ], style={'display':'table-row'})
                        ])
                    if tag['solar']:
                        mess.extend([
                                html.Div([
                                    html.Div(["Solar capacity:"], style={'display':'table-cell'}, title='in % of maximal consumption'),
                                    html.Div([
                                            dcc.RangeSlider(min=0, step=1, max=getattr(self.default.Max_Solar_Installed,tag['var']), 
                                                            value=getattr(self.Solar_Installed,tag['var']), id=f'gen-params-solar-{tag["var"]}')
                                            ], style={'display':'table-cell'}),
                                    html.Div(style={'display':'table-cell'}),
                                    html.Div(id=f'gen-params-solar-{tag["var"]}-sel', style={'display':'table-cell'}),
                                ], style={'display':'table-row'})
                            ])
                            
                out.extend([
                            html.Div(html.B(tag['name'],style={'font-style':'italic'})),
                            html.Div(mess, style={'display':'table','width':'100%','margin-bottom':'1em'})
                        ])
        return html.Div(out)
    
    def GenericFctParams(self,att,name):
        def fct(value):
            if value is not None:
                if isinstance(value,str):
                    val = self.String2List(value)
                elif isinstance(value,list):
                    val = [int(i) for i in value]
                else:
                    val = getattr(getattr(self.default,att),name)
                setattr(getattr(self,att), name, val)
                if att[0:5]=='Power':
                    unit='kW'
                elif att[0:5]=='Price':
                    unit='c$/kWh'
                elif att[0:5]=='Solar':
                    unit='%'
                else:
                    unit=''
                return f' {getattr(getattr(self,att),name)} {unit}'
        return fct
    
    
    #%% Menu -- cases setup
    def GenerateMenu(self):
        return html.Div(self.GenerateRefresh(), id='gen-gen-refresh')
    
    def GenerateRefresh(self):
        return [
                html.Div([html.Div([
                    html.Div([ 
                            html.Button(children='Generate', id='gen-launch-button', n_clicks=self.n_clicks_generate, style={'width':'60%','height':'2em'}) 
                            ], style={'display':'table-cell','width':'15%','text-align':'center'}),
                    html.Div([ 
                            html.I('Note that this operation may take some time.') 
                            ], style={'display':'table-cell','width':'75%'}),
                    ], style={'display':'table-row'}),
                    html.Div(id='gen-launch-button-sel', style={'display':'table-row'})
                    ],style={'display':'table','width':'100%','margin-bottom':'1em'}),
                html.Div(id='gen-generator-output')
                ]
    
    def GenerateLaunch(self,click=None):
        if click is not None and click!=self.n_clicks_generate:
            return html.Div([ html.Button(id='gen-generator-trigger', n_clicks=1) ], style={'display':'none'})
        else:
            return ''
    
    def Generate(self,click=None):
        return 'Youpi'
    
    
    