# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 17:41:02 2018

@author: Thomas
"""

import dash

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True