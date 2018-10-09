# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 17:45:22 2018

@author: Thomas
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import os
#import flask

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





## Add a static image route that serves images from desktop
## Be *very* careful here - you don't want to serve arbitrary files
## from your computer or server
#css_directory = os.getcwd()
#stylesheets = ['stylesheet.css']
#static_css_route = '/static/'
#
#@app.server.route('{}<stylesheet>'.format(static_css_route))
#def serve_stylesheet(stylesheet):
#    if stylesheet not in stylesheets:
#        raise Exception(
#            '"{}" is excluded from the allowed static files'.format(
#                stylesheet
#            )
#        )
#    return flask.send_from_directory(css_directory, stylesheet)
#
#
#for stylesheet in stylesheets:
#    app.css.append_css({"external_url": "/static/{}".format(stylesheet)})



if __name__ == '__main__':
    app.run_server(debug=True)