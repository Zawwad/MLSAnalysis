import dash
from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

## reading data

clubsDF = pd.read_csv('../Datasets/clubsDF.csv')
newIndex = pd.read_csv('../Datasets/newIndex.csv')

newIndexInt = newIndex.select_dtypes(include = 'int64')


## club count plot

fig1 = px.histogram(clubsDF, x = 'Club')
fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,75,154,0.4)', font_color='white', yaxis_title='Count', title_x = 0.5)


## goals per year plot

byYearG = newIndex.groupby('Year', as_index=False)
byYearGdf = byYearG['G'].sum()

fig2 = px.line(byYearGdf, x='Year', y='G', title='Goals by Year')
fig2.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0,75,154,0.4)', font_color='white', yaxis_title='Goals', title_x = 0.5)


## assist per year

byYearA = newIndex.groupby('Year', as_index=False)
byYearAdf = byYearA['A'].sum()

assistYearPlot = px.line(byYearAdf, x='Year', y='A', title = 'Assists Per Year')
assistYearPlot.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0,75,154,0.4)', font_color='white', yaxis_title='Assists', title_x = 0.5)
assistYearPlot.update_traces(line_color='mediumseagreen')

## assist per year statment

mostA = byYearA['A'].sum().max()[1]
mostAIndex = byYearA.sum().index[byYearA.sum()['A'] == byYearA.sum()['A'].max()][0]
mostAY = int(byYearA.sum().iloc[mostAIndex][0])

mostAText = 'The highest number of assists was in the year ' + str(mostAY) + '. The number was ' + str(mostA) + '.'


## yellow cards per player

byPlayerYC = newIndex.groupby('Player', as_index=False)
byPlayerYCdf = byPlayerYC['YC'].sum().sort_values('YC', ascending = False).head(15)

YCPlayerPlot = px.bar(byPlayerYCdf, x='Player', y='YC', title = 'Yellow Cards per Player')
YCPlayerPlot.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0,75,154,0.4)', font_color='white', yaxis_title='Yellow Cards', title_x = 0.5)
YCPlayerPlot.update_traces(marker_color='yellow')


## yellow cards per player statement

byPlayerYCMax = newIndex.groupby('Player')['YC']
totalYC = byPlayerYCMax.sum().max()
YCPlayer = byPlayerYCMax.sum().idxmax()

YCplayerClubdf = newIndex.groupby('Player')['Club'].value_counts()
YCplayerClub = YCplayerClubdf[YCPlayer].index[0]

mostYCText = str(YCPlayer) + ' had the highest number of yellow cards at ' + str(totalYC) + ' and he played for ' + str(YCplayerClub) + '.'

## penalty kick goals

playerPKGdf = newIndex.groupby('Player', as_index=False)['PKG'].sum().sort_values('PKG', ascending = False).head(15)

playerPKGPlot = px.bar(playerPKGdf, x='PKG', y='Player', title = 'Top Penalty Kick Goals per Player')
playerPKGPlot.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0,75,154,0.4)', font_color='white', yaxis_title='Penalty Kick Goals', title_x = 0.5)
playerPKGPlot.update_traces(marker_color='lightgreen')


## penalty kick goals statement

playerPKG = newIndex.groupby('Player')['PKG']

PKGScorersTotal = playerPKG.sum().value_counts()[1:].sum()
PKGTotal = newIndex['PKG'].sum()

PKGTotalScorers = str(PKGTotal) + ' penalty kick goals were scored in total. ' + str(PKGScorersTotal) + ' different players scored penalty kick goals.'

## at least one goal

oneGoal = newIndex[newIndex.G != 0].reset_index(drop=True).groupby(['Club', 'Player'], as_index=False)['G'].sum()['Club'].value_counts()

oneGoaldfTop = oneGoal.reset_index().head(10)
oneGoaldfBottom = oneGoal.reset_index().tail(10)

oneGoalPlotT = px.pie(oneGoaldfTop, values = 'count', names = 'Club', title = 'Most Players with at least one Goal')
oneGoalPlotT.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0,75,154,0.4)', font_color='white')
oneGoalPlotT.update_traces(textinfo='value')

oneGoalPlotB = px.pie(oneGoaldfBottom, values = 'count', names = 'Club', title = 'Least Players with at least one Goal')
oneGoalPlotB.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0,75,154,0.4)', font_color='white')
oneGoalPlotB.update_traces(textinfo='value')

## at least one goal statement

oneGoalTopTeam = oneGoal.idxmax()
oneGoalTopCount = oneGoal.max()

oneGoalText = str(oneGoalTopTeam) + ' had the most players with at least one goal, ' + str(oneGoalTopCount) + '.'


## dashboard components
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

initLayout = html.Div([

    html.H1('Club Performance', style={'textAlign': 'center'}),
    
    dcc.Link('Go to Player Performance', href = '/assignLayout', style={"display": "flex", "justifyContent": "center"}),

    html.Br(),
    html.Br(),
    
    html.H3('Count of Clubs', style={'textAlign': 'center', 'background' : 'rgba(255,255,0,0.4)'}),
    
    dcc.Graph(figure = fig1),
    
    html.Br(),
    html.Br(),
    
    html.H3('All Numeric Visualizations', style={'textAlign': 'center', 'background' : 'rgba(255,255,0,0.4)'}),
    
    dcc.Dropdown(id = "x_axis",
        options = [{"label" : col, "value" : col} for col in newIndexInt.columns[1:]],
        value = newIndexInt.columns[1],
        style={'color': 'black'},
    ),
    
    dcc.Graph(id = "plot"),

    html.Br(),
    html.Br(),
    
    html.H4(oneGoalText, style={'textAlign': 'center', 'background' : 'rgba(255,255,0,0.4)'}),
    
    html.Div([
    
        dcc.Graph(figure = oneGoalPlotT),
        dcc.Graph(figure = oneGoalPlotB),
        
    ], style = {'display': 'flex', "justifyContent": "center"}),
    
    
], style={'margin': '20px'})

assignLayout = html.Div([

    html.H1('Player Performance', style={'textAlign': 'center'}),

    dcc.Link('Go to Club Performance', href = '/initLayout', style={"display": "flex", "justifyContent": "center"}),

    html.Br(),
    html.Br(),
    
    html.H3("Goals Scored by Player", style={'background' : 'rgba(255,255,0,0.4)'}),
    
    dcc.Dropdown(id = "name",
        options = [{"label" : val, "value" : val} for val in newIndex['Player'].unique()],
        value = newIndex['Player'].unique()[0],
        style = {'color': 'black'},
    ),
    
    html.Br(),
    
    html.Div(id = "output_message", style = {'fontSize' : '25px'},),

    html.Br(),
    html.Br(),
    
    html.H4(mostYCText, style={'textAlign': 'center', 'background' : 'rgba(255,255,0,0.4)'}),
    
    dcc.Graph(figure = YCPlayerPlot),

    html.Br(),
    html.Br(),
    
    html.H4(PKGTotalScorers, style={'textAlign': 'center', 'background' : 'rgba(255,255,0,0.4)'}),
    
    dcc.Graph(figure = playerPKGPlot),
    
    html.Br(),
    html.Br(),
    
    html.H3('Trends over the Years', style={'textAlign': 'center', 'background' : 'rgba(255,255,0,0.4)'}),
    
    html.Br(),
    
    html.Div([
        
        dcc.Graph(figure = fig2),
        
        dcc.Graph(figure = assistYearPlot),
        
    ], style = {'display': 'flex', "justifyContent": "center"}),

    
], style={'margin': '20px'})



app.layout = html.Div([
    dcc.Location(id = 'url', refresh=False),
    html.Div(id = 'page-content')
])

## handling links
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)

def displayPage(pathname):
    if pathname == '/assignLayout':
        return assignLayout
    else:
        return initLayout


## text box input
@app.callback(
    Output('output_message', 'children'),
    [Input('name', 'value')]
)

def TotalGoals(Name):
    goals = 0
    if not Name:
        return "No player provided."
    else:
        for n in range(0,len(newIndex["Player"])):
            if newIndex["Player"][n] == Name:
                goals = goals + newIndex["G"][n]
        goalsstr = str(goals)
        return Name + " scored " + goalsstr + " goals."


## bar plot by dropdown
@app.callback(
    Output('plot', 'figure'),
    [Input('x_axis', 'value')]
)

def bar_plot(selected_var):
    bar_data = newIndex.groupby('Club', as_index=False)[selected_var].sum()
    fig = px.bar(bar_data, x = 'Club' , y = selected_var, color=selected_var, title = selected_var + ' by Club')
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0,75,154,0.4)', font_color='white', title_x = 0.5)
    return fig

## initializing dash

if __name__ == '__main__':
    app.run(debug = True)
