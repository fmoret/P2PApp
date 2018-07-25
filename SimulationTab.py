# -*- coding: utf-8 -*-
"""
    Class managing simulation tab layout
"""

import dash_core_components as dcc
import dash_html_components as html
#from igraph import *
from loremipsum import get_sentences
from DashTabs import TabApp


class SimulationTabApp(TabApp):
    def ShowTab(self,tab_id):
        data = self.DataTabs(tab_id)
        menu_data = html.Div([
                html.Div(['aaa']),
                html.Div([str(self.MarketGraph)]),
                html.Div(self.ListAgentsName()),
                html.Div(self.ListAgentsType()),
                html.Div(self.ListAgentsNumberAssets()),
                ])
        graph_data = dcc.Graph(
                id='graph',
                figure={
                    'data': data,
                    'layout': {
                        'margin': {
                            'l': 30,
                            'r': 0,
                            'b': 30,
                            't': 0
                        },
                        'legend': {'x': 0, 'y': 1}
                    }
                }
            )
        bottom_data = ' '.join(get_sentences(10))
        
        return self.MenuTab(menu_data,graph_data,bottom_data)
    
    
    
    
    
    
    
    

