import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
 
USERNAME_PASSWORD_PAIRS = [
    ['tstn','testn'],['guvi', 'guvi']
]
 
app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server
df = pd.read_csv('https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/matches.csv')
df.dropna(subset=['winner'], inplace=True)
a=df['winner'].value_counts().head()
fig1 = px.histogram(df, x=a.index,y=a.values,title='Top 5 Teams based on winning Count',color_discrete_sequence=["indianred"],text_auto=True, labels={'x':'winner', 'y':'Total wins'})
a=df['player_of_match'].value_counts().head()
fig2 = px.histogram(df, x=a.index,y=a.values,title='Top 5 Players',color=a.values,text_auto=True, labels={'x':'Player', 'y':'Total wins'})
dtmp1=df.groupby(['winner'])['win_by_wickets'].sum().sort_values(ascending=False).head(10)
fig3 = px.bar(dtmp, x=dtmp1.index,y=dtmp1,title='Top 10 Teams based on Win By Wickets',text_auto=True, labels={'x':'Winner', 'y':'Win By Wickets'},color=dtmp1)
dtmp=df.groupby(['winner'])['win_by_runs'].sum().sort_values(ascending=False).head(10)
fig4 = px.bar(dtmp, x=dtmp.index,y=dtmp,title='Top 10 Teams based on Win By Runs',text_auto=True, labels={'x':'Winner', 'y':'Win_by_runs'},color=dtmp)
app.layout = html.Div(children=[
    dcc.Graph(
       id='winteam',
       figure=fig1
    ),
    dcc.Graph(
       id='winplyr',
       figure=fig2
    ),dcc.Graph(
       id='winbwckt',
       figure=fig3
    ),
    dcc.Graph(
       id='winbrunr',
       figure=fig4
    ),
    dcc.RangeSlider(
        id='range-slider',
        min=-5,
        max=6,
        marks={i:str(i) for i in range(-5, 7)},
        value=[-3, 4]
    ),
    html.H1(id='product')  # this is the output
], style={'width':'50%'})
 
@app.callback(
    Output('product', 'children'),
    [Input('range-slider', 'value')])
def update_value(value_list):
    return value_list[0]*value_list[1]
 
if __name__ == '__main__':
    app.run_server(debug=True)
