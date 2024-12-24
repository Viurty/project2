import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import json
from weather_graphics import Graphics

# Загрузка данных и графиков
with open('data.json', 'r') as f:
    data = json.load(f)
graph = Graphics(data)
variant_city = ["Moscow","London","Omsk","Tomsk"]
variant_day = [1,2,3,4,5]

# Преобразование данных для Dropdown
city_options = [{'label': city, 'value': city} for city in variant_city]
day_options = [{'label': f'Day {day}', 'value': day} for day in variant_day]

# Инициализация приложения Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Макет приложения
app.layout = dbc.Container([
    html.H1('Дашборд погодных данных', className='text-center text-primary mb-4'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Фильтр по городам'),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='city-dropdown',
                        options=city_options,
                        value=None,
                        placeholder='Выберите город'
                    )
                ])
            ])
        ], md=4),


    dbc.Row([
        dbc.Col(dcc.Graph(id='temp_figure'), md=12)
    ]),

    dbc.Col([
            dbc.Card([
                dbc.CardHeader('Фильтр по дням'),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='day-dropdown',
                        options=day_options,
                        value=None,
                        placeholder='Выберите день'
                    )
                ])
            ])
        ], md=4),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='wind_figure'), md=6),
        dbc.Col(dcc.Graph(id='prob_figure'), md=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='map'), md=12),
    ])

], fluid=True)

# Коллбэки для обновления графиков
@app.callback(
    [Output('temp_figure', 'figure'),
     Output('wind_figure', 'figure'),
     Output('prob_figure', 'figure'),
     Output('map', 'figure')],
    [Input('city-dropdown', 'value'),
     Input('day-dropdown', 'value')]
)
def update_dashboard(city, day):
    if not city:
        city = graph.get_cities()[0]
    if not day:
        day = 1
    temp_figure = graph.create_linegraph(city, ['min_temperature', 'max_temperature'], 'Температура °C')
    wind_figure = graph.create_bargraph(day, 'wind_speed', 'Скорость ветра км/ч')
    prob_figure = graph.create_bargraph(day, 'prob', 'Вероятность осадков %')
    map = graph.create_map(day)
    return temp_figure, wind_figure, prob_figure, map

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
#################

