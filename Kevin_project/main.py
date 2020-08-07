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

import flask
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

"""
1.) get page 2 and page 3 to update graph
2.) finish write up https://docs.google.com/document/d/1HqbxzryBCSK_hwipFnKKG6AjghOY_Q5YGxzJsLTxhuU/edit#heading=h.cx9f8tlqo9gz
3.) finish bio

"""

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
# bar functions
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
        title_text='Levels of CPM', # title of plot
        xaxis_title_text='# of times it reached a level of cpm', # xaxis label
        yaxis_title_text='Times', # yaxis label
        bargap=0.2,
        bargroupgap=0.1
    )
    return fig

#addData(data, 'University of Washington', '#ff0000')
addData(data3, 'Exploritorium', '#005eff')
#addData(data4, 'Norra real Gym')
addData(data5, 'Pinewood School', '#89ddf5')
figure2 = createBarChart(dataX, names, colors)

# timeline functions

dataX2 = []
names2 = []
def limit2(dataset):
    dataset = dataset[dataset['deviceTime_local'] > '2020-07-24 00:00:00-08:00']
    return dataset
def createGraph(dataset, name):
    fig = go.Figure()
    for i in range(len(dataset)):
        temp = limit2(dataset[i])
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
def addData2(dataset, name):
    dataX2.append(dataset)
    names2.append(name)
def turnData(dataUrl):
    tempS = requests.get(dataUrl, headers=header).text
    tempDatas = pd.read_csv(io.StringIO(tempS))
    return tempDatas
def refresh2(data, name):
    addData2(data, name)
    fig = createGraph(dataX2, names2)
    return fig
addData2(data, 'University of Washington')
addData2(data3, 'Exploritorium')
fig2 = createGraph(dataX2, names2)

#   scatter plot functions
names3 = np.array([])
dataX3 = np.array([])
dataY3 = np.array([])
def addName(name):
    global names3
    names3 = np.append(names3, name)
def addAvg(dataSet, name):
    temp = np.array(dataSet['cpm'])
    count = 0
    num = 0
    global dataX3
    for i in range(len(temp)):
        count += temp[i]
        num += 1
    avg = count / num
    addName(name)
    dataX3 = np.append(dataX3, avg)
def findAvg(dataSet):
    temp = np.array(dataSet['cpm'])
    count = 0
    num = 0
    global dataX3
    for i in range(len(temp)):
        count += temp[i]
        num += 1
    avg = count / num
    return avg
def addNumAvg(dataSet):
    temp = np.array(dataSet['cpm'])
    temp2 = np.array(dataSet['cpmError'])
    count = 0
    global dataY3
    avg = findAvg(dataSet)
    for i in range(len(temp)):
        low = temp[i] - temp2[i]
        high = temp[i] + temp2[i]
        if(avg > low and avg < high):
            count += 1
    dataY3 = np.append(dataY3, count)
def addNumAvg2(dataSet):
    temp = np.array(dataSet['cpm'])
    temp2 = np.array(dataSet['cpmError'])
    count = 0
    global dataY3
    avg = findAvg(dataSet)
    for i in range(len(temp)):
        low = temp[i] - temp2[i]
        high = temp[i] + temp2[i]
        if(avg > low and avg < high):
            count += 1
    return count
def refresh3(urls, newName):
    addAvg(urls, newName)
    addNumAvg(urls)
    figs = createBarChart2(dataX3, dataY3, names3)
    return figs
def createBarChart2(xData, yData, name):
    fig = go.Figure()
    for x in range(len(xData)):
        fig.add_trace(go.Scatter(
        x = np.array(xData[x]), y = np.array(yData[x]),
        name = name[x], text = '',
        marker_size = 111,
        ))
    fig.update_layout(
        title='Average value of CPM vs # of data',
        xaxis=dict(
            title='Average value of CPM',
            gridcolor='white',
            type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title='# of data near average',
            gridcolor='white',
            gridwidth=2,
        ),
        #paper_bgcolor='rgb(243, 243, 243)',
        #plot_bgcolor='rgb(243, 243, 243)',
    )
    print(xData)
    return fig
addAvg(data, "University of Washington")
addAvg(data3, "Exploritorium")
addNumAvg(data)
addNumAvg(data3)
print(dataX3)
print(dataY3)
print(names2)
fig3 = createBarChart2(dataX3, dataY3, names3)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    dcc.Link('Histogram', href='/page-1'),
    html.Br(),
    dcc.Link('Timeline Chart', href='/page-2'),
    html.Br(),
    dcc.Link('Scatterplot', href='/page-3'),
])

layout_page_1 = html.Div([
    html.H2('Histogram'),

    html.Div(children='''
        This Histogram compares the cpm values of a dataset to other datasets from February 17, 2020 to now.
    '''),

    dcc.Graph(
        id='example-graph',
        figure= figure2
    ),
    html.Br(),
    html.Div(id = 'my-output'),
    html.Label('Please enter URL: '),
    dcc.Input(id='input-1-submit', type='text', placeholder='Enter URL'),
    html.Br(),
    html.Label('Please enter data name: '),
    dcc.Input(id='input-2-submit', type='text', placeholder='Enter Name'),
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
    html.Div(id='output-submit'),
    dcc.Link('Home', href='/'),
    html.Br(),
    dcc.Link('Timeline Chart', href='/page-2'),
    html.Br(),
    dcc.Link('Scatterplot', href='/page-3'),
])

layout_page_2 = html.Div([
    html.H2('Timeline Chart'),
    html.Div(children='''
        Compares levels of CPM since July 24th, 2020
    '''),
    dcc.Graph(
        id='example-graph2',
        figure= fig2
    ),
    html.Br(),
    html.Div(id = 'my-output'),
    html.Label('Please enter URL: '),
    dcc.Input(id='input-1-submit2', type='text', placeholder='Enter URL'),
    html.Br(),
    html.Label('Please enter data name: '),
    dcc.Input(id='input-2-submit2', type='text', placeholder='Enter Name'),
    html.Br(),html.Br(),
    html.Div(id='dd-output-container'),
    html.Button('Submit', id='btn-submit2'),
    html.Br(),
    html.Hr(),
    dcc.Link('Home', href='/'),
    html.Br(),
    dcc.Link('Histogram', href='/page-1'),
    html.Br(),
    dcc.Link('Scatterplot', href='/page-3'),
])

layout_page_3 = html.Div([
        html.H2('Scatterplot'),
        html.Div(children='''
                The scatterplot is average value of CPM vs # of data points near the average since February 17, 2020
        '''),

        dcc.Graph(
            id='example-graph3',
            figure= fig2
        ),
                #below is input
        html.Br(),
        html.Div(id = 'my-output3'),
        html.Label('Please enter the URL: '),
        dcc.Input(id='input-1-submit3', type='text', placeholder='Enter URL'),
        html.Br(),
        html.Label('Please enter data name: '),
        dcc.Input(id='input-2-submit3', type='text', placeholder='Enter Name'),
        html.Br(),html.Br(),
        html.Button('Submit', id='btn-submit3'),
        html.Br(),
        html.Hr(),

        dcc.Link('Home', href='/'),
        html.Br(),
        dcc.Link('Histogram', href='/page-1'),
        html.Br(),
        dcc.Link('Timeline Chart', href='/page-2'),
])

# index layout
app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    layout_page_1,
    layout_page_2,
    layout_page_3,
])


# Index callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/page-1":
        return layout_page_1
    elif pathname == "/page-2":
        return layout_page_2
    elif pathname == "/page-3":
        return layout_page_3
    else:
        return layout_index

# Page 1 callbacks
@app.callback(Output('example-graph', 'figure'),
            [Input('btn-submit', 'n_clicks')],
            [State('input-1-submit', 'value'),State('input-2-submit', 'value'), State('demo-dropdown', 'value')])
def update_graph1(clicked, input1, input2, value):
    if clicked is None:
        print(value, ' wads')
        return figure2
    if clicked:
        tempUrl = input1
        tempName = input2
        #temp.replace(u'\ufeff', '')
        datas = turnData(tempUrl)
        #print(datas)
        fig = refresh(datas, tempName, value)
        #print(value)
        return fig

# Page 2 callbacks
@app.callback(Output('example-graph2', 'figure'),
            [Input('btn-submit2', 'n_clicks')],
            [State('input-1-submit2', 'value'),State('input-2-submit2', 'value')])
def update_graph(clicked, input1, input2):
    if clicked is None:
        print(' wads')
    if clicked:
        tempUrl = input1
        tempName = input2
        temp.replace(u'\ufeff', '')
        datas = turnData(tempUrl)
        #print(datas)
        fig = refresh2(datas, tempName)
        #print(value)
        return fig
    return fig2
#page 3 callbacks
@app.callback(Output('example-graph3', 'figure'),
                #(Output('bar_graph', 'figure')),
                [Input('btn-submit3', 'n_clicks')],
                [State('input-1-submit3', 'value'),State('input-2-submit3', 'value')])
def update_graph2(clicked, input1, input2):
    if clicked is None:
        return fig3
        print('3rd')
    if clicked:
        tempUrl = input1
        tempName = input2
        datas = turnData(tempUrl)
        fig = refresh3(datas, tempName)
        print('is 3rd')
        return fig

if __name__ == '__main__':
    app.run_server(debug=False, port=8080, host='127.0.0.1')