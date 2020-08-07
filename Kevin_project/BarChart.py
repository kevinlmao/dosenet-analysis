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

#dataX = np.array([[]])
dataX = []
names = []
size = 0
colors = []
def limit(dataset):
    dataset = dataset[dataset['deviceTime_local'] > '2020-02-17 00:00:00-08:00']
    return dataset
def clearData(dataset):
    newData = []
    for i in range(len(dataset)):
        temp = []
        temp = dataset[i]
        temp2 = [0]
        sizes= [0]
        for x in range(len(temp)):
            z=0
            for y in range(len(temp2)):
                if temp[x] == temp2[y]:
                    z += 1
                    sizes[y] += 1
            if z == 0:        
                temp2.append(temp[x])
                sizes.append(1)
        temp3 = []
        for i in range(len(temp2)):
            y = 0
            if sizes[i] > 1:
                for x in range(sizes[i]):
                    temp3.append(temp2[i])
                    y += 1
        newData.append(temp3)
    return newData
def addData(dataset, name, color):
    temp = limit(dataset)
    temp = np.array(dataset['cpm'])
    global colors
    global dataX
    global names
    global size
    #size = np.append(size, )
    size += 1
    dataX.append(temp)
    names.append(name)
    colors.append(color)
def turnData(dataUrl):
    tempS = requests.get(dataUrl, headers=header).text
    tempDatas = pd.read_csv(io.StringIO(tempS))
    return tempDatas
def refresh(urls, newName, newColor):
    addData(urls, newName, newColor)
    figs = createBarChart(dataX, names, colors)
    return figs
def createBarChart(dataset, nameSet, colorSet):
    fig = go.Figure()
    dataset = clearData(dataset)
    for i in range(size):
        print(i)
        fig.add_trace(go.Histogram(
        x = np.array(dataset[i]),
        histnorm='percent', 
        name=names[i],
        xbins=dict(
            start= 0.0,
            end=1000.0,
            size=0.25
        ),
        marker_color=colorSet[i],
        opacity=0.75
        ))
    fig.update_layout(
        title_text='Test Bar Chart', # title of plot
        xaxis_title_text='# of times it reached a level of cpm', # xaxis label
        yaxis_title_text='Times', # yaxis label
        bargap=0.2,
        bargroupgap=0.1
    )
    return fig

addData(data, 'University of Washington', '#ff0000')
addData(data3, 'Exploritorium', '#005eff')
#addData(data4, 'Norra real Gym')
addData(data5, 'Pinewood School', '#89ddf5')
print(dataX)
print(size)
print(names)
figure2 = createBarChart(dataX, names, colors)

app.layout = html.Div([
    html.H1(children='Test'),

    html.Div(children='''
        Graphing tools
    '''),

    dcc.Graph(
        id='example-graph',
        figure= figure2
    ),
    html.Br(),
    html.Div(id = 'my-output'),
    html.Label('Text 1: '),
    dcc.Input(id='input-1-submit', type='text', placeholder='Enter URL'),
    html.Br(),
    html.Label('Text 2: '),
    dcc.Input(id='input-2-submit', type='text', placeholder='Enter Data Name'),
    html.Br(),html.Br(),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Red', 'value': '#ff0000'},
            {'label': 'Blue', 'value': '#005eff'},
            {'label': 'Green', 'value': '#1ba81b'},
            {'label': 'Yellow', 'value': '#f7f448'},
            {'label': 'Light Blue', 'value': '#89ddf5'},
            {'label': 'Purple', 'value': '#7f03fc'},
            {'label': 'Black', 'value': '#000000'},
            {'label': 'Rose Gold', 'value': '#f08c75'},
        ],
        value='#ff0000'
    ),
    html.Div(id='dd-output-container'),
    html.Button('Submit', id='btn-submit'),
    html.Br(),
    html.Hr(),
    html.Label('Output'), html.Br(),html.Br(),
    html.Div(id='output-submit'),
    
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
        return figure2
    if clicked:
        tempUrl = input1
        tempName = input2
        temp.replace(u'\ufeff', '')
        datas = turnData(tempUrl)
        print(datas)
        fig = refresh(datas, tempName, value)
        print(value)
        return fig
print('1')
if __name__ == '__main__':
    app.run_server(debug=False, port=8080, host='127.0.0.1')
print('2')