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
        self.__init_defaults__()
        self.__init_params__()
        self.titles_style = {'margin-bottom':'0.5em'}
        return
    
    def __init_defaults__(self):
        # set Tags for callback and generic function generators
        self.Tags = ['Ngen','Same','Coverage','Wind']
        self.GenericTags = ['Nhouse','Nstore']
        self.GenereciText = {
                'Nhouse':'Number of houses:',
                'Nstore':'Number of small stores:'
                }
        self.GenereciTitles = {
                'Nhouse':'Number of houses with all its appliances (water heater, TV, ...)',
                'Nstore':'Number of small stores (each using solely one edifice)'
                }
        # default parameters
        self.default = expando()
        self.default.G = expando()
        self.default.S = expando()
        self.default.R = expando()
        # variables associated to self.Tags
        self.default.G.Ngen = 1
        self.default.G.Same = True
        self.default.Max_Coverage = 150 # in %
        self.default.S.Prod_Coverage = 100 # in %
        self.default.S.Prod_Wind_share = 20 # in %
        self.default.R.Prod_Coverage = [90,110] # in %
        self.default.R.Prod_Wind_share = [10,20] # in %
        # variables associated to self.GenericTags
        self.default.S.Nhouse = 15
        self.default.R.Nhouse = [10,20]
        self.default.S.Nstore = 3
        self.default.R.Nstore = [2,5]
        return
    
    def __init_params__(self):
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
        for x in self.GenericTags:
            setattr(self.S,x, getattr(self.default.S,x) )
            setattr(self.R,x, getattr(self.default.R,x) )
#        self.S.Nhouses = self.default.S.Nhouses
#        self.R.Nhouses = self.default.R.Nhouses
#        self.S.Nstores = self.default.S.Nstores
#        self.R.Nstores = self.default.R.Nstores
        return
    
    def ShareWidth(self,menu=None,graph=None):
        if menu is None:
            menu='50%'
        if graph is None:
            graph='50%'
        self.share_width_menu = menu
        self.share_width_graph = graph
        self.defaultTable = html.Div([
                html.Div([], style={'display':'table-cell','width':'35%'}),
                html.Div([], style={'display':'table-cell','width':'30%'}),
                html.Div([], style={'display':'table-cell','width':'3%'}),
                html.Div([], style={'display':'table-cell','width':'15%'}),
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
                html.Div(bottom_data, style= {'width': '100%', 'display': 'block'})
            ], id='gen-main-tab')
    
    def ShowTab(self):
        menu_data = [self.GeneralMenu()]
        graph_data = [self.ParamsMenu()]
        bottom_data = [self.CasesMenu()]
        return self.MenuTab(menu_data,graph_data,bottom_data)
    
    
    #%% Menu -- General setup
    def GeneralMenu(self):
        return html.Div([
                html.H4('General information',style=self.titles_style, title='Parameters of the generator itself'),
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Number of test cases:'], style={'display':'table-cell'}, 
                                     title='Number of test cases to generate'),
                            html.Div([
                                    dcc.Input(type='number',min=1,step=1,value=self.G.Ngen, id='gen-general-Ngen', style={'width':'50%'})
                                    ], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                ], style={'display':'table','width':'100%','margin-bottom':'0.5em'}),
                html.Div(id='gen-general-Ngen-sel'),
            ], style={'margin-bottom':'1em'})
    
    def Ngen(self,Ngen=None):
        if Ngen is not None:
            self.G.Ngen = int(Ngen)
        if self.G.Ngen == 1:
            self.G.Same = True
            style_same = {'display':'none'}
        else:
            style_same = {'display':'table','width':'100%','margin-bottom':'0.5em'}
        return html.Div([
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Use the same composition for all test cases:'], style={'display':'table-cell'}, 
                                     title='Should all test cases be composed of the same elements?'),
                            html.Div([
                                    dcc.RadioItems( id='gen-general-Same', labelStyle={'display': 'block'}, 
                                                   value=self.G.Same,
                                                 options=[
                                                    {'label': 'Yes', 'value': True},
                                                    {'label': 'No', 'value': False},
                                                ])
                                    ], style={'display':'table-cell'}),
                        ], style={'display':'table-row'}),
                ], style=style_same),
                html.Div(id='gen-general-Same-sel'),
            ], style={'margin-bottom':'1em'})
        
    def Same(self,Same=None):
        if Same is not None:
            self.G.Same = bool(Same)
        compo = [self.defaultTable]
        compo.extend(self.GenericMenu())
        if self.G.Same:
            return html.Div([
                    html.Div([
                        self.defaultTable,
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
                        self.defaultTable,
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
                out.append( html.Div([
                            html.Div([self.GenereciText[tag]], style={'display':'table-cell'}, title=self.GenereciTitles[tag]),
                            html.Div([
                                    dcc.Input(type='number', min=0,step=1, value=getattr(self.S,tag) , id=f'gen-general-{tag}')
                                    ], style={'display':'table-cell','padding-bottom':'.25em'}),
                            html.Div(id=f'gen-general-{tag}-sel', style={'display':'none'}),
                        ], style={'display':'table-row'}) 
                    )
        else:
            for tag in tags:
                 out.append( html.Div([
                            html.Div([self.GenereciText[tag]], style={'display':'table-cell'}, title=self.GenereciTitles[tag]),
                            html.Div([
                                    dcc.Input(type='text', value=f'{getattr(self.R,tag)}', id=f'gen-general-{tag}'),
                                    ], style={'display':'table-cell','padding-bottom':'.25em'}),
                            html.Div(style={'display':'table-cell'}),
                            html.Div(id=f'gen-general-{tag}-sel', style={'display':'table-cell'}),
                        ], style={'display':'table-row'})
                    )
        return out
    
    def GenericFct(self,name):
        def fct(value):
            if value is not None:
                if isinstance(value,str):
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
                    setattr(self.R, name, val)
                    return f' {getattr(self.R,name)}'
                elif isinstance(value,int) or isinstance(value,float):
                    setattr(self.S, name, int(value))
            return
        return fct
    
    
    
    #%% Menu -- Characteristics
    def ParamsMenu(self):
        return html.Div([
                html.H4('Characteristics:',style=self.titles_style),
                html.Div(html.B('Houses',style={'font-style':'italic'})),
                html.Div([
                    self.defaultTable,
                    html.Div([
                            html.Div(['Minimal consumption:'], style={'display':'table-cell'}),
                            html.Div([
                                    dcc.Input(type='number',min=1,step=1,value=1, id='gen-params-Pmins')
                                    ], style={'display':'table-cell'})
                        ], style={'display':'table-row'}),
                ], style={'display':'table','width':'100%'})
                ], style={'margin-bottom':'1em'})
    
    
    
    
    
    #%% Menu -- cases setup
    def CasesMenu(self):
        return html.Div([
                    html.H4(''),
                ])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    