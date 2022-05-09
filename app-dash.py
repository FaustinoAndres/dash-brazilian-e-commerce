import pandas as pd
import plotly.express as px
import psycopg2
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from cfg import host, database, user, password

try:
    conn = psycopg2.connect(
        host = host,
        database = database,
        user = user,
        password = password
    )

    print("Successful connection")

except Exception as ex:
    print(ex)

most_bought_product = """select count(order_items_table.product_id) as qproducts, products_category_name_table.product_category_name_english
                         from order_items_table
                         join products_table on order_items_table.product_id = products_table.product_id
                         join products_category_name_table on products_table.product_category_name_id = products_category_name_table.category_id
                         group by products_category_name_table.product_category_name_english
                         order by qproducts desc
                         limit 10"""

df_most_bought_product = pd.io.sql.read_sql_query(most_bought_product, conn)
fig1 = px.bar(df_most_bought_product, x="product_category_name_english", y="qproducts")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], 
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
server = app.server

#---------------------------------------------------------------
#Taken from https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
df = pd.read_csv("COVID-19-geographic-disbtribution-worldwide-2020-03-29.csv")

dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths','cases']].sum()
#print (dff[:5])
#---------------------------------------------------------------
app.layout = dbc.Container(
    [
           html.H1(['Brazilian Ecommerce'], className="h-100 p-5 bg-light border rounded-3"),

           html.Div(children='''
                Analysis
            '''),
    dcc.Graph(figure = fig1),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
        #figure = fig1
    )


    ])

# app.layout = html.Div([
#     html.Div([
#         dash_table.DataTable(
#             id='datatable_id',
#             data=dff.to_dict('records'),
#             columns=[
#                 {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
#             ],
#             editable=False,
#             filter_action="native",
#             sort_action="native",
#             sort_mode="multi",
#             row_selectable="multi",
#             row_deletable=False,
#             selected_rows=[],
#             page_action="native",
#             page_current= 0,
#             page_size= 6,
#             # page_action='none',
#             # style_cell={
#             # 'whiteSpace': 'normal'
#             # },
#             # fixed_rows={ 'headers': True, 'data': 0 },
#             # virtualization=False,
#             style_cell_conditional=[
#                 {'if': {'column_id': 'countriesAndTerritories'},
#                  'width': '40%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'deaths'},
#                  'width': '30%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'cases'},
#                  'width': '30%', 'textAlign': 'left'},
#             ],
#         ),
#     ],className='row'),

#     html.Div([
#         html.Div([
#             dcc.Dropdown(id='linedropdown',
#                 options=[
#                          {'label': 'Deaths', 'value': 'deaths'},
#                          {'label': 'Cases', 'value': 'cases'}
#                 ],
#                 value='deaths',
#                 multi=False,
#                 clearable=False
#             ),
#         ],className='six columns'),

#         html.Div([
#         dcc.Dropdown(id='piedropdown',
#             options=[
#                      {'label': 'Deaths', 'value': 'deaths'},
#                      {'label': 'Cases', 'value': 'cases'}
#             ],
#             value='cases',
#             multi=False,
#             clearable=False
#         ),
#         ],className='six columns'),

#     ],className='row'),

#     html.Div([
#         html.Div([
#             dcc.Graph(id='linechart'),
#         ],className='six columns'),

#         html.Div([
#             dcc.Graph(id='piechart'),
#         ],className='six columns'),

#     ],className='row'),


# ])

# #------------------------------------------------------------------
# @app.callback(
#     [Output('piechart', 'figure'),
#      Output('linechart', 'figure')],
#     [Input('datatable_id', 'selected_rows'),
#      Input('piedropdown', 'value'),
#      Input('linedropdown', 'value')]
# )
# def update_data(chosen_rows,piedropval,linedropval):
#     if len(chosen_rows)==0:
#         df_filterd = dff[dff['countriesAndTerritories'].isin(['China','Iran','Spain','Italy'])]
#     else:
#         print(chosen_rows)
#         df_filterd = dff[dff.index.isin(chosen_rows)]

#     pie_chart=px.pie(
#             data_frame=df_filterd,
#             names='countriesAndTerritories',
#             values=piedropval,
#             hole=.3,
#             labels={'countriesAndTerritories':'Countries'}
#             )


#     #extract list of chosen countries
#     list_chosen_countries=df_filterd['countriesAndTerritories'].tolist()
#     #filter original df according to chosen countries
#     #because original df has all the complete dates
#     df_line = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

#     line_chart = px.line(
#             data_frame=df_line,
#             x='dateRep',
#             y=linedropval,
#             color='countriesAndTerritories',
#             labels={'countriesAndTerritories':'Countries', 'dateRep':'date'},
#             )
#     line_chart.update_layout(uirevision='foo')

#     return (pie_chart,line_chart)

# #------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
