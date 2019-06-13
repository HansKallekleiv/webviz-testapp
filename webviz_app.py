#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import os.path as path
from pathlib import Path, PosixPath
from flask_talisman import Talisman
from webviz_config.common_cache import cache
from webviz_config.webviz_store import webviz_storage
from webviz_config.webviz_assets import webviz_assets
import webviz_config.containers as standard_containers


app = dash.Dash(__name__, external_stylesheets=[])
server = app.server

app.title = 'Reek Webviz Demonstration'
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

app.webviz_settings = {
    'portable': True,
    'plotly_layout': {'paper_bgcolor': 'rgba(90, 90, 90)', 'plot_bgcolor': 'rgba(90, 90, 90)', 'colorway': ['#14213d', '#3a2d58', '#69356a', '#9a3a6f', '#c84367', '#ea5954', '#fe7c37', '#ffa600']}
                      }

cache.init_app(server)

CSP = {'default-src': "'self'", 'prefetch-src': "'self'", 'style-src': ["'self'", "'unsafe-inline'", 'https://webviz-cdn.azureedge.net'], 'script-src': ["'self'", "'unsafe-eval'", "'sha256-jZlsGVOhUAIcH+4PVs7QuGZkthRMgvT2n0ilH6/zTM0='"], 'img-src': ["'self'", 'data:', 'https://sibwebvizcdn.blob.core.windows.net'], 'navigate-to': "'self'", 'base-uri': "'self'", 'form-action': "'self'", 'frame-ancestors': "'none'", 'child-src': "'none'", 'object-src': "'self'", 'plugin-types': 'application/pdf', 'font-src': ['https://webviz-cdn.azureedge.net']}
FEATURE_POLICY = {'camera': "'none'", 'geolocation': "'none'", 'microphone': "'none'", 'payment': "'none'"}

Talisman(server, content_security_policy=CSP, feature_policy=FEATURE_POLICY)

webviz_storage.use_storage = True
webviz_storage.storage_folder = path.join(path.dirname(path.realpath(__file__)),
                                          'webviz_storage')

webviz_assets.portable = True


app.layout = dcc.Tabs(parent_className="layoutWrapper",
                      content_className='pageWrapper',
                      vertical=True, children=[
   
    dcc.Tab(id='logo',
            className='styledLogo',children=[
                 standard_containers.BannerImage(**{'image': PosixPath('/tmp/webviz/webviz-config/examples/example_banner.png'), 'title': 'My banner image'}).layout,
                 dcc.Markdown(r'''Webviz created from configuration file.'''),
                 dcc.Markdown(r'''Some other text, potentially with strange letters like Åre, Smørbukk Sør.''')
                 ]
    ),
    dcc.Tab(id='table_example',label='Table example',
            selected_className='selectedButton',
            className='styledButton',children=[
                 standard_containers.DataTable(**{'csv_file': PosixPath('/tmp/webviz/webviz-config/examples/example_data.csv'), 'filtering': True}).layout
                 ]
    ),
    dcc.Tab(id='syntax_highlighting_example',label='Syntax highlighting example',
            selected_className='selectedButton',
            className='styledButton',children=[
                 standard_containers.SyntaxHighlighter(**{'filename': PosixPath('/tmp/webviz/webviz-config/examples/basic_example.yaml')}).layout
                 ]
    ),
    dcc.Tab(id='plot_a_table',label='Plot a table',
            selected_className='selectedButton',
            className='styledButton',children=[
                 standard_containers.TablePlotter(app=app, **{'title': 'Plotter', 'csv_file': PosixPath('/tmp/webviz/webviz-config/examples/example_data.csv')}).layout
                 ]
    ),
    dcc.Tab(id='last_page',label='Plot a table (locked)',
            selected_className='selectedButton',
            className='styledButton',children=[
                 standard_containers.TablePlotter(app=app, **{'title': 'Initial reservoir pressure', 'csv_file': PosixPath('/tmp/webviz/webviz-config/examples/example_data.csv'), 'lock': True, 'plot_options': {'x': 'Well', 'y': 'Initial reservoir pressure (bar)', 'size': 'Average permeability (D)', 'facet_col': 'Segment'}}).layout
                 ]
    )]
)

if __name__ == '__main__':
    # This part is ignored when the webviz app is started
    # using Docker container and uwsgi (e.g. when hosted on Azure).

    dash_auth.BasicAuth(app, {'some_username': 'some_password'})
    app.run_server(host='localhost', port=8050, ssl_context=('server.crt', 'server.key'), dev_tools_hot_reload=True)