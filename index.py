# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 17:45:22 2018

@author: Thomas
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from MainApp import P2PMarket_App


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/generator':
         return ['Test case generator']
    else:
         return P2PMarket_App.layout

if __name__ == '__main__':
    app.run_server(debug=True)