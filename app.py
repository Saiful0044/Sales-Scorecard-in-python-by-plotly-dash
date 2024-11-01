import numpy as np
import pandas as pd
import dash
import plotly.graph_objects as go
from dash import Dash,html,dcc,Input,Output,callback
from datetime import datetime
import dash_table as dt

# external css
external_stylesheets= [
      {
            "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
            "rel":"stylesheet",
            "integrity" : "sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" ,
            "crossorigin": "anonymous"
      }]


df = pd.read_csv("dataset/train.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Year']=df['Order Date'].dt.year
df['Month_name'] = df['Order Date'].dt.month_name()

app = dash.Dash(__name__,external_stylesheets=external_stylesheets,meta_tags=[{'name':'viewport','content':'width=device-width'}])

app.layout = html.Div([
      html.Div([
            html.Div([
                  html.H3("Sales Scorecard",style={'color':'white'})
            ],className='col-3'),
            html.Div([
                  html.P('Year',style={'color':'white'}),
                  dcc.Slider(
                        id='select_year',
                        included=False,
                        updatemode='drag',
                        tooltip={'always_visible':True},
                        min = 2015,
                        max = 2018,
                        step= 1,
                        value= 2018,
                        marks= {str(yr): str(yr) for yr in (list(df['Year'].unique()))}
                  )
            ],className='col-5'),


            html.Div([
                  html.P("Segment", style={'color':'white','text-align':'center'}),
                  dcc.RadioItems(
                        id='radio_items',
                        labelStyle={'display':'inline-block'},
                        value='Consumer',
                        options=[{'label':i, 'value':i} for i in list(df['Segment'].unique())],
                        style={'text-align':'center','color':'white'}
                  )
            ],className='col-4')
      ],className='row',style={'padding-top':"5px"}),


      html.Br(),

      html.Div([
            html.Div([
                  html.Div([
                        html.Div([
                              dcc.RadioItems(
                                    id='radio_item1',
                                    labelStyle={'display':'inline-block'},
                                    value='Sub-Category',
                                    options=[
                                          {'label':'Sub-Category' , 'value':'Sub-Category'},
                                          {'label':'Region' , 'value':'Region'}
                                    ],
                                    style={'text-align':'center', 'color':'white'}
                              ),

                              dcc.Graph(
                                    id='bar_chart1',
                                    style = {'height': '330px'}
                              )
                        ],className='card-body')
                  ],className='card',style={'background-color':'#1f2c56'})
            ],className='col-3' ),

            html.Div([
                  html.Div([
                        html.Div([
                              dcc.Graph(
                                    id='pie_chart',
                                    style = {'height': '350px'}
                              )
                        ], className='card-body')
                  ],className='card', style={'background-color':'#1f2c56'})
            ],className='col-3'),

            html.Div([
                  html.Div([
                        html.Div([
                              dcc.Graph(
                                    id='line_chart',
                                    style = {'height': '350px'}
                              )
                        ], className='card-body')
                  ], className='card', style={'background-color':'#1f2c56'})
            ],className='col-4'),

            html.Div([
                  html.Div([
                        html.Div([
                              html.Div(id='text1'),
                              html.Div(id='text2'),
                              html.Div(id='text3')
                        ], className='card-body',style = {'height': '380px'})
                  ], className='card',style={'background-color':'#1f2c56'})
            ],className='col-2')
      ],className='row h-25'),

      html.Br(),
      html.Div([
            html.Div([
                  dt.DataTable(
                        id='my_datatable',
                        columns=[{'name':i, 'id': i} for i in df.loc[:,['Sales','Customer ID','Customer Name','Segment', 'City', 'State', 'Region','Category', 'Sub-Category', 'Product Name','Sales', 'Year', 'Month_name']]],

                        virtualization = True,
                        style_cell={
                              'textAlign':'left',
                              'min-width': '100px',
                              'backgroundColor':'#1f2c56',
                              'color':'#FEFEFE',
                              'border-bottom':'0.01rem solid #19AAE1',
                              
                        },
                        sort_action='native',
                        sort_mode ='multi',
                        style_as_list_view=True,
                        style_header={
                              'backgroundColor':'#1f2c56',
                              'fontWeight':'bold',
                              'font':'Lato, sans-serif',
                              'color':'orange',
                              'border':'#1f2c56'
                        },
                        style_data = {
                              'textOverflow':'hidden',
                              'color':'white'
                        },
                        fixed_rows={'headers':True}
                  )
            ], className='col-3'),


            html.Div([
                  html.Div([
                        html.Div([
                              dcc.RadioItems(
                                    id='radio_item4',
                                    labelStyle={"display": "inline-block"},
                                    value='State',
                                    options=[
                                          {'label':'State', 'value':'State'},
                                          {'label':'City', 'value':'City'}
                                    ],
                                    style={'text-align':'center', 'color':'white'}
                              ),

                              dcc.Graph(
                                    id='bar_chart2',
                                    config= {'displayModeBar': 'hover'}
                                    
                              )
                        ],className='card-body')
                  ],className='card',style={'background-color':'#1f2c56'})
            ], className='col-3'),


            html.Div([
                  html.Div([
                        html.Div([
                              dcc.Graph(
                                    id='bubble_chart',
                                    config = {'displayModeBar': 'hover'}
                        
                              )
                        ], className='card-body')
                  ],className='card', style={'background-color':'#1f2c56'})
            ], className='col-6')
      ],className='row')
],className='container')

@app.callback(
      Output('bar_chart1','figure'),
      [Input('select_year','value'),
       Input('radio_item1','value'),
       Input('radio_items', 'value')
      ]
)

def update_graph(select_year,radio_item1, radio_items):
      sales1 = df.groupby(['Year','Segment','Sub-Category'])['Sales'].sum().reset_index()
      sales2 = sales1[(sales1['Year'] == select_year) & (sales1['Segment']== radio_items)].sort_values(by='Sales',ascending=False).head(5)
      sales3 = df.groupby(['Year','Segment','Region'])['Sales'].sum().reset_index()
      sales4 = sales3[(sales3['Year'] == select_year ) & (sales3['Segment']== radio_items)].sort_values(ascending=False,by='Sales')

      if radio_item1 == 'Sub-Category':
            return {
                  'data':[
                        go.Bar(
                              x = sales2['Sales'],
                              y = sales2['Sub-Category'],
                              orientation='h',
                              text = sales2['Sales'],
                              texttemplate='$' + '%{text:.2s}',
                              textposition= 'auto',
                              marker=dict(color = '#19AAE1'),
                              hoverinfo='text',
                              hovertext=
                                    '<b>Year</b>: ' + sales2['Year'].astype(str) + '<br>' + \
                                    '<b>Segment</b>: ' + sales2['Segment'].astype(str) + '<br>'+ \
                                    '<b>Sub-Category</b>: ' + sales2['Sub-Category'].astype(str) + '<br>' + \
                                    '<b>Sales</b>: ' + sales2['Sales'].astype(str)
                        )
                  ],

                  'layout': go.Layout(
                              
                              plot_bgcolor='#1f2c56',
                              paper_bgcolor='#1f2c56',
                              title={
                                    'text':f"Sales by Sub-Category in Year {select_year}",
                                    'y':0.98,
                                    'x':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              titlefont={
                                    'color':'white',
                                    'size':12
                              },
                              hovermode='closest',
                              margin=dict(t=50,r=0),
                              xaxis=dict(
                                    title = '<b></b>',
                                    color ='orange',
                                    showline= True,
                                    showgrid = True,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    ),
                              
                              ),
                              yaxis=dict(
                                    title = '<b></b>',
                                    autorange = 'reversed',
                                    color ='orange',
                                    showline= False,
                                    showgrid = False,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    )
                              
                              ),
                              legend ={
                                    'orientation':'h',
                                    'bgcolor':'#1f2c56',
                                    'x':1.25,
                                    'y':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              font = dict(
                                    family = "sans-serif",
                                    size = 15,
                                    color = 'white'),
                        )       
            }
      elif radio_item1 == 'Region':
            return {
                  'data': [
                        go.Bar(
                              x = sales4['Sales'],
                              y = sales4['Region'],
                              text = sales2['Sales'],
                              orientation='h',
                              texttemplate='$' + '%{text:.2s}',
                              textposition= 'auto',
                              marker=dict(color = '#19AAE1'),
                              hoverinfo='text',
                              hovertext=
                                    '<b>Year</b>: ' + sales4['Year'].astype(str) + '<br>' + \
                                    '<b>Segment</b>: ' + sales4['Segment'].astype(str) + '<br>'+ \
                                    '<b>Region</b>: ' + sales4['Region'].astype(str) + '<br>' + \
                                    '<b>Sales</b>: ' + sales4['Sales'].astype(str)
                        )
                  ],

                  'layout': go.Layout(
                              
                              plot_bgcolor='#1f2c56',
                              paper_bgcolor='#1f2c56',
                              title={
                                    'text':f"Sales by Sub-Category in Year {select_year}",
                                    'y':0.98,
                                    'x':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              titlefont={
                                    'color':'white',
                                    'size':12
                              },
                              hovermode='closest',
                              margin=dict(t=50,r=0),
                              xaxis=dict(
                                    title = '<b></b>',
                                    color ='orange',
                                    showline= True,
                                    showgrid = True,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    ),
                              
                              ),
                              yaxis=dict(
                                    title = '<b></b>',
                                    autorange = 'reversed',
                                    color ='orange',
                                    showline= False,
                                    showgrid = False,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    )
                              
                              ),
                              legend ={
                                    'orientation':'h',
                                    'bgcolor':'#1f2c56',
                                    'x':1.25,
                                    'y':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              font = dict(
                                    family = "sans-serif",
                                    size = 15,
                                    color = 'white'),
                        )
            }            

# Pie Chart
@app.callback(
      Output('pie_chart', 'figure'),
      [Input('select_year','value'),
      Input('radio_items','value')
      ]
)

def update_graph(select_year, radio_items):
      sales5 = df.groupby(['Year', 'Segment', 'Category'])['Sales'].sum().reset_index()
      furniture_sales = sales5[(sales5['Year'] == select_year) & (sales5['Segment']== radio_items) & (sales5['Category'] == 'Furniture')]['Sales'].sum()

      office_sales = sales5[(sales5['Year'] == select_year) & (sales5['Segment']== radio_items) & (sales5['Category'] == 'Office Supplies')]['Sales'].sum()

      technology_sales = sales5[(sales5['Year'] == select_year) & (sales5['Segment']== radio_items) & (sales5['Category'] == 'Technology')]['Sales'].sum()

      colors = ['#30C9C7', '#7A45D1', 'orange']

      return {
            'data': [
            go.Pie(
                  labels = ['Furniture', 'Office Supplies', 'Technology'],
                  values = [furniture_sales, office_sales, technology_sales],
                  marker= dict(colors=colors),
                  hoverinfo= 'label+value+percent',
                  textinfo=  'label+value',
                  textfont=dict(size=13),
                  texttemplate= "%{label} <br> $%{value:,.2f}",
                  textposition='auto',
                  hole = 0.7,
                  rotation=160,
                  insidetextorientation='radial'
            )
            ],

            'layout': go.Layout(
                        plot_bgcolor='#1f2c56',
                        paper_bgcolor= '#1f2c56',
                        hovermode='x',
                        title = {
                              "text" :f'Sales by Category in Year {select_year}',
                              'y': 0.98,
                              'x': 0.5,
                              'xanchor':'center',
                              'yanchor': 'top'
                        },
                        titlefont = {
                              'color': 'white',
                              'size': 15},
                        legend = {
                              'orientation': 'h',
                              'bgcolor': '#1f2c56',
                              'xanchor': 'center', 'x': 0.5, 'y': -0.15},

                        font = dict(
                              family = "sans-serif",
                              size = 12,
                              color = 'white')
                  )
      }

@app.callback(
      Output('line_chart', 'figure'),
      [
            Input('select_year', 'value'),
            Input('radio_items','value')
      ]
)

def updata_graph(select_year,radio_items):
      sales6 = df.groupby(['Year','Segment','Month_name'])['Sales'].sum().reset_index()
      sales7 = sales6[(sales6['Year'] == select_year) & (sales6['Segment']== radio_items)]

      return {
            'data': [
                  go.Scatter(
                        x = sales7['Month_name'],
                        y = sales7['Sales'],
                        name = 'Sales',
                        text = sales7['Sales'],
                        texttemplate= '%{text:.2s}',
                        textposition= 'bottom left',
                        mode = 'markers + lines + text',
                        line = dict(width = 3,color = 'orange'),
                        marker = dict(
                              size = 10,
                              symbol = 'circle',
                              color = '#19AAE1',
                              line = dict(
                                    color = '#19AAE1',
                                    width = 2
                              )
                        ),
                        hoverinfo = 'text',
                        hovertext =
                              '<b>Year</b>: ' + sales7['Year'].astype(str) + '<br>' +
                              '<b>Month</b>: ' + sales7['Month_name'].astype(str) + '<br>' +
                              '<b>Segment</b>: ' + sales7['Segment'].astype(str) + '<br>' +
                              '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales7['Sales']] + '<br>'
                  )
            ],

            'layout': go.Layout(
                        plot_bgcolor='#1f2c56',
                        paper_bgcolor='#1f2c56',
                        title={
                              'text': f"Sales Trend in year {select_year}",
                              'y':0.97,
                              'x':0.5,
                              'xanchor':'center',
                              'yanchor':'top'
                        },
                        titlefont={
                              'color':'white',
                              'size':15
                        },
                        hovermode= 'closest',
                        margin= dict(t=5,l=0, r= 0),

                        xaxis= dict(
                              title = '<b></b>',
                              visible = True,
                              color = 'orange',
                              showline = True,
                              showgrid = False,
                              showticklabels = True,
                              linecolor = 'orange',
                              linewidth = 1,
                              ticks ='outside',
                              tickfont = dict(
                                    family = 'Arial',
                                    size = 12,
                                    color = 'orange'
                              )
                        ),
                        yaxis = dict(
                              title = '<b></b>',
                              visible = True,
                              color = 'orange',
                              showline = False,
                              showgrid = True,
                              showticklabels = False,
                              linecolor = 'orange',
                              linewidth = 1,
                              ticks = '',
                              tickfont = dict(
                              family = 'Arial',
                              size = 12,
                              color = 'orange')

                        ),
                        legend = {
                              'orientation': 'h',
                              'bgcolor': '#1f2c56',
                              'x': 0.5,
                              'y': 1.25,
                              'xanchor': 'center',
                              'yanchor': 'top'},

                        font = dict(
                              family = "sans-serif",
                              size = 12,
                              color = 'white'),

                        )
      }

@app.callback(
      Output('text1', 'children'),
      [Input('select_year', 'value')]

)

def update_text(select_year):
      sales8 = df.groupby('Year')['Sales'].sum().reset_index()
      current_year = sales8[sales8['Year']==select_year]['Sales'].sum()

      return [
            html.H6(
                  children='Current Year',
                  style={
                        'textAlign':'center',
                        'color': 'white'
                  }
            ),
            html.P('${0:,.2f}'.format(current_year),
                   style={
                         'textAlign':'center',
                         'color':'#19AAE1',
                         'fontSize':15,
                         'margin-top': '-10px'
                   }
            
            )
      ]

@app.callback(
      Output('text2', 'children'),
      [Input('select_year', 'value')]

)

def update_text(select_year):
      sales9 = df.groupby('Year')['Sales'].sum().reset_index()
      sales9['PY'] = sales9['Sales'].shift(1)
      previous_year = sales9[sales9['Year']==select_year]['PY'].sum()

      return [
            html.H6(
                  children='Previous Year',
                  style={
                        'textAlign':'center',
                        'color': 'white'
                  }
            ),
            html.P('${0:,.2f}'.format(previous_year),
                   style={
                         'textAlign':'center',
                         'color':'#19AAE1',
                         'fontSize':15,
                         'margin-top': '-10px'
                   }
            
            )
      ]

@app.callback(
      Output('text3', 'children'),
      [Input('select_year', 'value')]

)

def update_text(select_year):
      sales9 = df.groupby('Year')['Sales'].sum().reset_index()
      sales9['PY'] = sales9['Sales'].shift(1)
      sales9['YOY Growth'] = sales9['Sales'].pct_change()
      sales9['YOY Growth'] = sales9['YOY Growth']*100
      previous_year_growth = sales9[sales9['Year']==select_year]['YOY Growth'].sum()

      return [
            html.H6(
                  children='YOY Growth',
                  style={
                        'textAlign':'center',
                        'color': 'white'
                  }
            ),
            html.P('${0:,.2f}'.format(previous_year_growth),
                   style={
                         'textAlign':'center',
                         'color':'#19AAE1',
                         'fontSize':15,
                         'margin-top': '-10px'
                   }
            
            )
      ]

@app.callback(
      Output('my_datatable','data'),
      [
            Input('select_year','value'),
            Input('radio_items', 'value')
      ]
)

def display_table(select_year,radio_items):
      data_table = df[(df['Year'] == select_year) & (df['Segment']==radio_items)]

      return data_table.to_dict('records')


# Bar chart 2
@app.callback(
      Output('bar_chart2', 'figure'),
      [
            Input('select_year', 'value'),
            Input('radio_items', 'value'),
            Input('radio_item4', 'value')
      ]
)

def update_graph(select_year,radio_items,radio_item4):
      sales1 = df.groupby(['Year','Segment','State'])['Sales'].sum().reset_index()
      sales2 = sales1[(sales1['Year']==select_year) & (sales1['Segment']==radio_items)].sort_values(by='Sales',ascending=False).nlargest(10,columns=['Sales'])
      sales3 = df.groupby(['Year','Segment','City'])['Sales'].sum().reset_index()
      sales4 = sales3[(sales3['Year']==select_year) & (sales3['Segment']==radio_items)].sort_values(by='Sales',ascending=False).nlargest(10,columns=['Sales'])

      if radio_item4 == 'State':
            return {
                  'data':[
                        go.Bar(
                              x = sales2['Sales'],
                              y = sales2['State'],
                              text = sales2['Sales'],
                              orientation='h',
                              texttemplate='$' + '%{text:.2s}',
                              textposition= 'auto',
                              marker=dict(color = '#19AAE1'),
                              hoverinfo='text',
                              hovertext=
                                    '<b>Year</b>: ' + sales2['Year'].astype(str) + '<br>' + 
                                    '<b>Segment</b>: ' + sales2['Segment'].astype(str) + '<br>'+ 
                                    '<b>State</b>: ' + sales2['State'].astype(str) + '<br>' + 
                                    '<b>Sales</b>: ' + sales2['Sales'].astype(str)
                        )

                  ],

                  'layout': go.Layout(
                              plot_bgcolor='#1f2c56',
                              paper_bgcolor='#1f2c56',
                              title={
                                    'text':f"Sales by State in Year {select_year}",
                                    'y':0.98,
                                    'x':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              titlefont={
                                    'color':'white',
                                    'size':12
                              },
                              hovermode='closest',
                              margin=dict(t=50,r=0),
                              xaxis=dict(
                                    title = '<b></b>',
                                    color ='orange',
                                    showline= True,
                                    showgrid = True,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    ),
                              
                              ),
                              yaxis=dict(
                                    title = '<b></b>',
                                    autorange = 'reversed',
                                    color ='orange',
                                    showline= False,
                                    showgrid = False,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    )
                              
                              ),
                              legend ={
                                    'orientation':'h',
                                    'bgcolor':'#1f2c56',
                                    'x':1.25,
                                    'y':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              font = dict(
                                    family = "sans-serif",
                                    size = 15,
                                    color = 'white'),
                        )
            }
      elif radio_item4 =='City':
            return {
                  'data': [
                        go.Bar(
                              x = sales4['Sales'],
                              y = sales4['City'],
                              text = sales4['Sales'],
                              orientation='h',
                              texttemplate='$' + '%{text:.2s}',
                              textposition= 'auto',
                              marker=dict(color = '#19AAE1'),
                              hoverinfo='text',
                              hovertext=
                                    '<b>Year</b>: ' + sales4['Year'].astype(str) + '<br>' + \
                                    '<b>Segment</b>: ' + sales4['Segment'].astype(str) + '<br>'+ \
                                    '<b>City</b>: ' + sales4['City'].astype(str) + '<br>' + \
                                    '<b>Sales</b>: ' + sales4['Sales'].astype(str)
                        )
                  ],

                  'layout': go.Layout(
                              plot_bgcolor='#1f2c56',
                              paper_bgcolor='#1f2c56',
                              title={
                                    'text':f"Sales by City in Year {select_year}",
                                    'y':0.98,
                                    'x':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              titlefont={
                                    'color':'white',
                                    'size':12
                              },
                              hovermode='closest',
                              margin=dict(t=50,r=0),
                              xaxis=dict(
                                    title = '<b></b>',
                                    color ='orange',
                                    showline= True,
                                    showgrid = True,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    ),
                              
                              ),
                              yaxis=dict(
                                    title = '<b></b>',
                                    autorange = 'reversed',
                                    color ='orange',
                                    showline= False,
                                    showgrid = False,
                                    showticklabels = True,
                                    linecolor ='orange',
                                    linewidth = 2,
                                    ticks='outside',
                                    tickfont = dict(
                                          family='Arial',
                                          size= 12,
                                          color= 'orange'
                                    )
                              
                              ),
                              legend ={
                                    'orientation':'h',
                                    'bgcolor':'#1f2c56',
                                    'x':1.25,
                                    'y':0.5,
                                    'xanchor':'center',
                                    'yanchor':'top'
                              },
                              font = dict(
                                    family = "sans-serif",
                                    size = 15,
                                    color = 'white'),
                        )

            }


@app.callback(
      Output('bubble_chart','figure'),
      [
            Input('select_year', 'value'),
            Input('radio_items', 'value')
      ]
)

def update_graph(select_year, radio_items):
      sales10 = df.groupby(['Year','Segment','State','City','Month_name'])['Sales'].sum().reset_index()
      sales11 = sales10[(sales10['Year']== select_year) & (sales10['Segment']== radio_items)]

      return {
            'data' : [
                  go.Scatter(
                        x = sales11['Month_name'],
                        y = sales11['Sales'],
                        mode = 'markers',
                        marker=dict(
                              size = sales11['Sales']/250,
                              color = sales11['Sales'],
                              colorscale = 'HSV',
                              showscale = False,
                              line = dict(
                                    color = 'MediumPurple',
                                    width = 2
                              )
                        ),
                        hoverinfo= 'text',
                        hovertext= 
                              '<b>Year</b>: ' + sales11['Year'].astype(str) + '<br>' +
                              '<b>Month</b>: ' + sales11['Month_name'].astype(str) + '<br>' +
                              '<b>Segment</b>: ' + sales11['Segment'].astype(str) + '<br>' +
                              '<b>State</b>: ' + sales11['State'].astype(str) + '<br>' +
                              '<b>City</b>: ' + sales11['City'].astype(str) + '<br>' +
                              '<b>Sales</b>: ' + sales11['Sales'].astype(str) + '<br>'
                  )
            ],

            'layout':  go.Layout(
                        plot_bgcolor= '#1f2c56',
                        paper_bgcolor= '#1f2c56',
                        title=dict(
                              text = f'Sales by State and City in Year {select_year}',
                              y = 0.98,
                              x = 0.5,
                              xanchor = 'center',
                              yanchor = 'top'
                        ),
                        titlefont=dict(
                              color = 'white',
                              size = 15
                        ),
                        margin=dict(t=40,r=0,l=0),
                        xaxis=dict(
                              title = '<b></b>',
                              color = 'orange',
                              showline = False,
                              showgrid = False,
                              linewidth = 1
                              
                        ),
                        yaxis=dict(
                              title = '<b></b>',
                              color = 'orange',
                              visible = True,
                              showline = False,
                              showgrid = True,
                              linewidth = 1
                        )
                  )
      }



if __name__=='__main__':
      app.run(debug=True)