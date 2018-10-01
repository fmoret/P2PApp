# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:17:06 2018

@author: Thomas
"""

#import datetime
import dash_core_components as dcc
import dash_html_components as html
from loremipsum import get_sentences
import plotly.plotly as py
import plotly.graph_objs as go
from igraph import *
import numpy as np

class MGraph(Graph):
    def __init__(self, *args, **kwds): 
#        kwds = self.DefaultParams(kwds)
        Graph.__init__(self, *args, **kwds)
        self.BuildGraphOfMarketGraph(True)
        
        return
    
#    def DefaultParams(self,kwds):
#        kwd_order = ['N_vertices','N_edges'] 
#        self.N_vertices = 0
#        self.N_edges = 0
#        # Update default parameters
#        for idk, k in enumerate(kwd_order):
#            if k in kwds:
#                if k=='N_vertices':
#                    self.N_vertices = int(kwds[k])
#                elif k=='N_edges':
#                    self.N_edges = str(kwds[k])
#                del kwds[k]
#        return kwds
    
    @classmethod 
    def Load(cls, f, format=None, *args, **kwds):
        g = Graph.Load(f, format=format, *args, **kwds)
        out=MGraph(directed=True)
        out.add_vertices(len(g.vs))
        for i in range(len(g.vs)):
            for idx,k in enumerate(g.vs[i].attributes()):
                out.vs[i][k] = g.vs[i][k]
        for i in range(len(g.es)):
            out.add_edge(g.es[i].source,g.es[i].target)
            for idx,k in enumerate(g.es[i].attributes()):
                out.es[i][k] = g.es[i][k]
        return out
    
    @classmethod 
    def Save(cls, g, f, format=None):
        out=Graph(directed=True)
        out.add_vertices(len(g.vs))
        for i in range(len(g.vs)):
            for idx,k in enumerate(g.vs[i].attributes()):
                out.vs[i][k] = g.vs[i][k]
        for i in range(len(g.es)):
            out.add_edge(g.es[i].source,g.es[i].target)
            for idx,k in enumerate(g.es[i].attributes()):
                out.es[i][k] = g.es[i][k]
        return out.save(f, format=format)
    
    #%% Graph plot
    def BuildLayout(self,first=False):
        update = False
        if first==True:
            # Graph characteristics
            self.N_vertices = len(self.vs)
            self.N_edges = len(self.es)
        if first or self.N_vertices!=len(self.vs) or self.N_edges!=len(self.es):
            update = True
            self.N_vertices = len(self.vs)
            # Graph layout
            self.layt = self.layout('kk')
            # Nodes coordinates
            self.Xn=[self.layt[k][0] for k in range(self.N_vertices)]# x-coordinates of nodes
            self.Yn=[self.layt[k][1] for k in range(self.N_vertices)]# y-coordinates
#        if first or (self.N_vertices==len(self.vs) and self.N_edges!=len(self.es)):
#            update = True
            self.N_edges = len(self.es)
            # Edges coordinates
            self.Xe=[]
            self.Ye=[]
            for e in self.es:
                self.Xe+=[self.layt[e.source][0],self.layt[e.target][0], None]# x-coordinates of edge ends
                self.Ye+=[self.layt[e.source][1],self.layt[e.target][1], None]
        return update
            
        
    
    def BuildGraphOfMarketGraph(self,first=False):
        if self.BuildLayout(first):
            trace1=go.Scatter(
                           x=self.Xe,
                           y=self.Ye,
                           mode='lines',
                           line=dict(color='rgb(125,125,125)', width=1),
                           hoverinfo='none'
                           )
            trace2=go.Scatter(
                           x=self.Xn,
                           y=self.Yn,
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
#            axis=dict(showbackground=False,
#                      showline=False,
#                      zeroline=False,
#                      showgrid=False,
#                      showticklabels=False,
#                      title=''
#                      )
            layout = go.Layout(
                    #title="Network of coappearances of characters in Victor Hugo's novel - Les Miserables",
                    width=1000,
                    height=1000,
                    showlegend=False,
                    #scene=dict(xaxis=dict(axis),yaxis=dict(axis)),
                    xaxis=dict(
                        autorange=True,
                        showgrid=True,
                        zeroline=False,
                        showline=False,
                        ticks='',
                        showticklabels=False
                    ),
                    yaxis=dict(
                        autorange=True,
                        showgrid=True,
                        zeroline=False,
                        showline=False,
                        ticks='',
                        showticklabels=False
                    ),
                    margin=dict(t=100),
                    hovermode='closest',
                    annotations=[
                           dict(
                                showarrow=False,
                                #text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
                                text='',
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
            self.Show = dcc.Graph(figure=go.Figure(data=[trace1, trace2], layout=layout), id='my-graph2')
        return self.Show