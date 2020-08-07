import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io
import requests
import dash
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

temp = ''
url = 'https://radwatch.berkeley.edu/test/tmp/dosenet/uw.csv?tedlcjkxo' #university of washington pocket geiger counts
#url = 'https://radwatch.berkeley.edu/test/tmp/dosenet/uw_adc.csv?trconeyw' #university of washington co2 sensor
url2 = 'https://radwatch.berkeley.edu/test/dosenet/etch_roof_aq.csv'
url3 = 'https://radwatch.berkeley.edu/test/tmp/dosenet/exploratorium.csv?glxwayoct' #exploritorium
url4 = 'https://radwatch.berkeley.edu/test/tmp/dosenet/norrareal.csv?cgszexm' #Norra real gym pocket geiger counts
url5 = 'https://radwatch.berkeley.edu/test/tmp/dosenet/pinewood.csv?szwzjx' #pinewood school
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
s2=requests.get(url2,headers=header).text
data2= pd.read_csv(io.StringIO(s2))
s3=requests.get(url3,headers=header).text
data3= pd.read_csv(io.StringIO(s3))
s=requests.get(url,headers=header).text
data = pd.read_csv(io.StringIO(s))
s4=requests.get(url4,headers=header).text
data4 = pd.read_csv(io.StringIO(s4))
s5=requests.get(url5,headers=header).text
data5 = pd.read_csv(io.StringIO(s5))
dataX = []
names = []
def limit(dataset):
    dataset = dataset[dataset['deviceTime_local'] > '2020-07-24 00:00:00-08:00']
    return dataset
def createGraph(dataset, name):
    fig = go.Figure()
    for i in range(len(dataset)):
        temp = limit(dataset[i])
        fig.add_trace(go.Scatter(
        x = temp['deviceTime_local'],
        y = temp['cpm'],
        mode='lines',
        name=name[i]      
    ))
    fig.update_layout(plot_bgcolor='white',width=1000, height=450)
    fig.update_yaxes(title="cpm",titlefont=dict(color='black', size=20),
                 showgrid=False,tickcolor='black',
                 tickfont=dict(color='black', size=16))
    fig.update_xaxes(title="Time (local) ",titlefont=dict(color='black', size=20),
                 linecolor='black',tickfont=dict(color='black',size=12))
    fig.update_layout(legend_orientation="h",
                  legend=dict(x=0,y=-.2, font=dict(size=13)))
    return fig
def addData(dataset, name):
    dataX.append(dataset)
    names.append(name)
def turnData(dataUrl):
    tempS = requests.get(dataUrl, headers=header).text
    tempDatas = pd.read_csv(io.StringIO(tempS))
    return tempDatas
def refresh(data, name):
    addData(data, name)
    fig = createGraph(dataX, names)
    return fig
addData(data, 'test')
addData(data3, 'test2')
fig = createGraph(dataX, names)

app.layout = html.Div([
    html.H1(children='Test'),

    html.Div(children='''
        Graphing tools
    '''),

    dcc.Graph(
        id='example-graph',
        figure= fig
    ),
    html.Br(),
    html.Div(id = 'my-output'),
    html.Label('Text 1: '),
    dcc.Input(id='input-1-submit', type='text', placeholder='Enter URL'),
    html.Br(),
    html.Label('Text 2: '),
    dcc.Input(id='input-2-submit', type='text', placeholder='Enter Data Name'),
    html.Br(),html.Br(),
    html.Div(id='dd-output-container'),
    html.Button('Submit', id='btn-submit'),
    html.Br(),
    html.Hr(),
    #html.Label('Output'), html.Br(),html.Br(),
   # html.Div(id='output-submit'),
    
    html.Br(), html.Hr()
    ])
@app.callback(Output('example-graph', 'figure'),
            #(Output('bar_graph', 'figure')),
           # Output('dd-output-container', 'children'),
            #[Input('demo-dropdown', 'value')],
            #dash.dependencies.Output('dd-output-container', 'children'),
            
            [Input('btn-submit', 'n_clicks')],
            [State('input-1-submit', 'value'),State('input-2-submit', 'value'), State('demo-dropdown', 'value')])
            #dash.dependencies.Output('example-graph', 'value'),
            
def update_graph(clicked, input1, input2, value):
    if clicked is None:
        print(value + ' wads')  
    if clicked:
        tempUrl = input1
        tempName = input2
        temp.replace(u'\ufeff', '')
        datas = turnData(tempUrl)
        print(datas)
        fig = refresh(datas, tempName)
        print(value)
    
    
    return fig
        
print('1')
if __name__ == '__main__':
    app.run_server(debug=False, port=8080, host='127.0.0.1')
print('2')