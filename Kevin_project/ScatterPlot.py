import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
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
"""
data = data[data['deviceTime_local']> '2020-02-17 00:00:00-08:00']
data = data[data['deviceTime_local'] < '2020-02-18 00:00:00-08:00']
data2 = data2[data2['deviceTime_local']>'2020-01-01 00:00:00-08:00']
data3 = data3[data3['deviceTime_local'] > '2020-02-17 00:00:00-08:00']
data3 = data3[data3['deviceTime_local'] < '2020-02-18 00:00:00-08:00']
data4 = data4[data4['deviceTime_local'] > '2020-02-17 00:00:00-08:00']
data4 = data4[data4['deviceTime_local'] < '2020-02-18 00:00:00-08:00']
data5 = data5[data5['deviceTime_local'] > '2020-02-17 00:00:00-08:00']
data5 = data5[data5['deviceTime_local'] < '2020-02-18 00:00:00-08:00']
"""
names = np.array([])
def turnData(dataUrl):
    tempS = requests.get(dataUrl, headers=header).text
    tempDatas = pd.read_csv(io.StringIO(tempS))
    return tempDatas
def addName(name):
    global names
    names = np.append(names, name)
def addAvg(dataSet, name):
    temp = np.array(dataSet['cpm'])
    count = 0
    num = 0
    global dataX
    for i in range(len(temp)):
        count += temp[i]
        num += 1
    avg = count / num
    addName(name)
    dataX = np.append(dataX, avg)
def findAvg(dataSet):
    temp = np.array(dataSet['cpm'])
    count = 0
    num = 0
    global dataX
    for i in range(len(temp)):
        count += temp[i]
        num += 1
    avg = count / num
    return avg
def addNumAvg(dataSet):
    temp = np.array(dataSet['cpm'])
    temp2 = np.array(dataSet['cpmError'])
    count = 0
    global dataY
    avg = findAvg(dataSet)
    for i in range(len(temp)):
        low = temp[i] - temp2[i]
        high = temp[i] + temp2[i]
        if(avg > low and avg < high):
            count += 1
    dataY = np.append(dataY, count)
def addNumAvg(dataSet):
    temp = np.array(dataSet['cpm'])
    temp2 = np.array(dataSet['cpmError'])
    count = 0
    global dataY
    avg = findAvg(dataSet)
    for i in range(len(temp)):
        low = temp[i] - temp2[i]
        high = temp[i] + temp2[i]
        if(avg > low and avg < high):
            count += 1
    #dataY = np.append(dataY, count)
    return count
def refresh(urls, newName):
    addAvg(urls, newName)
    addNumAvg(urls)
    figs = createBarChart(dataX, dataY, names)
    print(dataX)
    print(dataY)
    return figs
dataX = np.array([])
dataY = np.array([])
addAvg(data, "University of Washington")
addAvg(data3, "Exploritorium")
#addAvg(data4, "test3")
#addAvg(data5, "test4")
addNumAvg(data)
addNumAvg(data3)
#addNumAvg(data4)
#addNumAvg(data5)
def createBarChart2(xData, yData, names):
    fig = go.Figure()
    for x in range(len(xData)):
        fig.add_trace(go.Scatter(
        x = np.array(xData[x]), y = np.array(yData[x]),
        name = names[x], text = '',
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
    return fig
fig2 = createBarChart(dataX, dataY, names)
tempUrl = ''
tempName = ''
app.layout = html.Div([
        html.H1(children='Tools for graphing data'),

        html.Div(children='''
            
        '''),

        dcc.Graph(
            id='example-graph',
            figure= fig2
        ),
                #below is input
        html.Br(),
        html.Div(id = 'my-output'),
        html.Label('Please enter the URL: '),
        dcc.Input(id='input-1-submit', type='text', placeholder='Enter URL'),
        html.Br(),
        html.Label('Please enter the name for the data: '),
        dcc.Input(id='input-2-submit', type='text', placeholder='Enter Name'),
        html.Br(),html.Br(),
        html.Button('Submit', id='btn-submit'),
        html.Br(),
        html.Hr(),
        html.Label('Output'), html.Br(),html.Br(),
        html.Div(id='output-submit'),
        html.Br(), html.Hr()
        ])
@app.callback(Output('example-graph3', 'figure'),
                #(Output('bar_graph', 'figure')),
                [Input('btn-submit3', 'n_clicks')],
                [State('input-1-submit3', 'value'),State('input-2-submit3', 'value')])
def update_graph(clicked, input1, input2):
    if clicked is None:
        return fig2
    if clicked:
        tempUrl = input1
        tempName = input2
        datas = turnData(tempUrl)
        fig = refresh3(datas, tempName)
        return fig
if __name__ == '__main__':
    app.run_server(debug=False, port=8080, host='127.0.0.1')