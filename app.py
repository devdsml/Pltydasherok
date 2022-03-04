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
fig1 = px.bar(df,y=a.index,x=a.values,title='Top 5 Teams based on Winning Count',text_auto=True, labels={'y':'Winner', 'x':'Total Wins'}, orientation='h',color_discrete_sequence= px.colors.sequential.Plasma)
fig1.update_layout(yaxis={'categoryorder':'total ascending'})

fig2 = px.treemap(df, path=['player_of_match'],title='Best PLayer based on Player of Match')
fig2.update_traces(textinfo = 'label + value',hovertemplate="<b>Player:</b> %{label} <br> <b>Total Wins:</b> %{value}")

dtmp1=df.groupby(['winner'])['win_by_wickets'].sum().sort_values(ascending=False).head(10)
fig3 = px.bar(dtmp1, x=dtmp1.index,y=dtmp1,title='Top 10 Teams based on Win By Wickets',text_auto=True, labels={'x':'Winner', 'y':'Win By Wickets'},color_discrete_sequence= px.colors.qualitative.Prism)

dtmp=df.groupby(['winner'])['win_by_runs'].sum().sort_values(ascending=False).head(10)
fig4 = px.bar(dtmp,y=dtmp.index,x=dtmp,title='Top 10 Teams based on Win By Runs',text_auto=True, labels={'x':'Win By Runs', 'y':'Winning Team'},orientation='h',color_discrete_sequence=px.colors.sequential.RdBu)
fig4.update_layout(yaxis={'categoryorder':'total ascending'})

fig6= px.sunburst(df, path=['toss_winner', 'winner'],title='Winning probability by Winning Toss')

fig6.update_traces(textinfo="label+percent parent+value")

app.layout = html.Div(children=[
  html.H2(children='Data Analysis with IPL Datset',style={'textAlign': 'center',color='#5A1404'}),
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
    ),dcc.Graph(
       id='winprobt',
       figure=fig6
    )
    
   
])


 
if __name__ == '__main__':
    app.run_server(debug=True)
