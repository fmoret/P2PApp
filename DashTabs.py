# -*- coding: utf-8 -*-
"""
    File managing Dash tabs layout
"""

#import datetime
import dash_core_components as dcc
import dash_html_components as html
from loremipsum import get_sentences
import plotly.plotly as py
import plotly.graph_objs as go
from igraph import *

class TabApp:
    def __init__(self,Market):
        self.ShareWidth()
        self.MarketGraph = Market
        self.init_GraphOfMarketGraph()
    
    def ShareWidth(self,menu=None,graph=None):
        if menu is None:
            menu='40%'
        if graph is None:
            graph='60%'
        self.share_width_menu = menu
        self.share_width_graph = graph

    def MenuTab(self,menu_data,graph_data,bottom_data):
        if menu_data=='':
            width_menu = '0%'
            width_graph = '100%'
        elif graph_data=='':
            width_graph = '0%'
            width_menu = '100%'
        else:
            width_menu = self.share_width_menu
            width_graph = self.share_width_graph
        
        return html.Div([
                html.Div([
                    html.Div([menu_data], style={'width': width_menu, 'display': 'inline-block','vertical-align': 'top'}),
                    html.Div([graph_data], style= {'width': width_graph, 'display': 'inline-block'})
                ], style= {'width': '100%', 'display': 'block'}),
                html.Div([bottom_data], style= {'width': '100%', 'display': 'block'})
            ])
    
        
    def DataTabs(self,tab_id):
        return [
                {
                    'x': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                          2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    'y': [219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                          350, 430, 474, 526, 488, 537, 500, 439],
                    'name': 'Rest of world',
                    'marker': {
                        'color': 'rgb(55, 83, 109)'
                    },
                    'type': ['bar', 'scatter', 'box'][int(tab_id) % 3]
                }
            ]
    
    def ShowTab(self,tab_id):
        data = self.DataTabs(tab_id)
        menu_data = html.Div([
                html.Div(['aaa']),
                html.Div([str(self.MarketGraph)])
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
    
    #%% Market graph management
    def ListAgentsName(self,out_list=[]):
        ag_list = []
        for i in self.ListAgentsIndex(out_list):
            ag_list.append(self.MarketGraph.vs[i]['name'])
        return ag_list
    
    def ListAgentsIndex(self,out_list=[]):
        show_list = []
        for i in range(len(self.MarketGraph.vs)):
            if self.MarketGraph.vs[i].index not in out_list:
                show_list.append(self.MarketGraph.vs[i].index)
        return show_list
    
    #def ListAgentsIndex(self,show_self=True,show_type=None):
    #    if show_type==None and show_self:
    #        show_list = [i for i in range(len(self.MarketGraph.vs))]
    #    elif show_type==None and not show_self:
    #        show_list = [i for i in range(len(self.MarketGraph.vs)) if i!=self.AgentID]
    #    else:
    #        if show_self:
    #            show_list = [i for i in range(len(self.MarketGraph.vs)) if self.MarketGraph.vs[i]['Type']==show_type]
    #        else:
    #            show_list = [i for i in range(len(self.MarketGraph.vs)) if self.MarketGraph.vs[i]['Type']==show_type and i!=self.AgentID]
    #    return show_list
    
    def ListAgentsType(self):
        ag_list = []
        for i in range(len(self.MarketGraph.vs)):
            ag_list.append(self.MarketGraph.vs[i]['Type'])
        return ag_list
    
    def ListAgentsNumberAssets(self):
        ag_list = []
        for i in range(len(self.MarketGraph.vs)):
            ag_list.append(self.MarketGraph.vs[i]['AssetsNum'])
        return ag_list
    
    def init_GraphOfMarketGraph(self):
        self.N_vertices = -1
        self.N_edges = -1
    
    def BuildGraphOfMarketGraph(self):
        if self.N_vertices!=len(self.MarketGraph.vs) or self.N_edges!=len(self.MarketGraph.es):
            self.layt = self.MarketGraph.layout('kk')
            self.N_vertices = len(self.MarketGraph.vs)# number of vertices
            self.N_edges = len(self.MarketGraph.es)# number of edges
        Xn=[self.layt[k][0] for k in range(self.N_vertices)]# x-coordinates of nodes
        Yn=[self.layt[k][1] for k in range(self.N_vertices)]# y-coordinates
        Xe=[]
        Ye=[]
        for e in self.MarketGraph.es:
            Xe+=[self.layt[e.source][0],self.layt[e.target][0], None]# x-coordinates of edge ends
            Ye+=[self.layt[e.source][1],self.layt[e.target][1], None]
        trace1=go.Scatter(
                       x=Xe,
                       y=Ye,
                       mode='lines',
                       line=dict(color='rgb(125,125,125)', width=1),
                       hoverinfo='none'
                       )
        trace2=go.Scatter(
                       x=Xn,
                       y=Yn,
                       mode='markers',
                       name='actors',
                       marker=dict(symbol='circle-dot',
                                     size=6,
                                     #color=group,
                                     colorscale='Viridis',
                                     line=dict(color='rgb(50,50,50)', width=0.5)
                                     ),
                       #text=labels,
                       hoverinfo='text'
                       )
        axis=dict(showbackground=False,
                  showline=False,
                  zeroline=False,
                  showgrid=False,
                  showticklabels=False,
                  title=''
                  )
        layout = go.Layout(
                title="Network of coappearances of characters in Victor Hugo's novel - Les Miserables",
                width=1000,
                height=1000,
                showlegend=False,
                scene=dict(xaxis=dict(axis),yaxis=dict(axis)),
                margin=dict(t=100),
                hovermode='closest',
                annotations=[
                       dict(
                            showarrow=False,
                            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
                            xref='paper',
                            yref='paper',
                            x=0,
                            y=0.1,
                            xanchor='left',
                            yanchor='bottom',
                            font=dict(size=14)
                        )
                    ])
        #return html.Div(['hihi'])
        return dcc.Graph(figure=go.Figure(data=[trace1, trace2], layout=layout), id='my-graph2')
        
    
    def ShowMarketGraph(self):
        #test = html.Div([dcc.Graph( figure=go.Figure(
        #        data=[go.Bar( x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
        #                      y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,350, 430, 474, 526, 488, 537, 500, 439],
        #                      name='Rest of world',marker=go.Marker(color='rgb(55, 83, 109)')),
        #              go.Bar( x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
        #                      y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,299, 340, 403, 549, 499],
        #                      name='China',marker=go.Marker(color='rgb(26, 118, 255)'))],
        #              layout=go.Layout(title='US Export of Plastic Scrap',showlegend=True,legend=go.Legend(x=0,y=1.0),margin=go.Margin(l=40, r=0, t=40, b=30))
        #            ))],style={'height': 300},id='test-graph')
        test = ''
        return html.Div([test,
                html.Div([self.BuildGraphOfMarketGraph()],id='market-graph-graph'),
                dcc.Interval(id='market-graph-interval',interval=3*1000), # interval in milliseconds
                ])
    
    
    
    
    
    