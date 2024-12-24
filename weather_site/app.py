from flask import Flask, request, render_template, jsonify
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from weather_forecast import Forecast, error503
from weather_logic import Logic, days
from weather_graphics import Graphics

app = Flask(__name__)


forecast = Forecast(None, None)
logic = Logic(None)
graph = Graphics({'error': 'error'})
day = None
data = None

@app.route("/", methods=["GET", "POST"])
def form():
    return render_template('form_page.html')

@app.route("/res", methods=["GET", "POST"])
def res():
    global day, forecast, logic, data, graph
    if request.method == "POST":
        start_city = request.form["city1"]
        end_city = request.form["city2"]
        day = int(request.form["days"])
        if day > 5:
            return render_template('error.html', error='Прогноз доступен только на пять дней вперед.')
        forecast = Forecast(start_city, end_city)
        try:
            forecast.get_data_start()
            forecast.get_data_end()
            logic = Logic(forecast.get_all_data())
        except error503:
            return render_template('error.html', error='Проблема с подключением к серверу.')
        except:
            return render_template('error.html', error='Неправильно введено имя города. Попробуйте написать город на английском.')
        start_color, start_res = logic.get_res(start_city, day)
        end_color, end_res = logic.get_res(end_city, day)
        start_weather = forecast.get_scpecific(start_city, day)
        end_weather = forecast.get_scpecific(end_city, day)
        data = {'s_city': start_city, 'e_city': end_city, 'day': day, 'sc': start_color,
                'sr': start_res, 'sw': start_weather, 'ec': end_color, 'er': end_res, 'ew': end_weather}
        graph = Graphics(forecast.get_all_data())
        return render_template('res_page.html', start_city=start_city, end_city=end_city,
                               start_weather=start_weather, end_weather=end_weather,
                               end_res=end_res, start_res=start_res, start_color=start_color,
                               end_color=end_color, day=days(day))
    else:
        start_city = data['s_city']
        end_city = data['e_city']
        start_color, start_res, start_weather = data['sc'], data['sr'], data['sw']
        end_color, end_res, end_weather = data['ec'], data['er'], data['ew']
        return render_template('res_page.html', start_city=start_city, end_city=end_city,
                               start_weather=start_weather, end_weather=end_weather,
                               end_res=end_res, start_res=start_res, start_color=start_color,
                               end_color=end_color, day=days(day))

@app.route("/extra", methods=["POST"])
def new_res():
    global forecast, logic, graph, day
    if request.method == "POST":
        new_city = request.form["new_city"]
        try:
            forecast.get_data(new_city)
            graph.update_data(forecast.get_all_data())
        except error503:
            return render_template('error.html', error='Проблема с подключением к серверу.')
        except:
            return render_template('error.html', error='Неправильно введено имя города. Попробуйте написать город на английском.')
        logic.update_data(forecast.get_all_data())
        color, res = logic.get_res(new_city, day)
        weather = forecast.get_scpecific(new_city, day)
        return render_template('new_res_page.html', city=new_city, weather=weather, res=res, color=color, day=days(day))

dash_app = Dash(
    __name__,
    server=app,
    url_base_pathname='/visualization/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

dash_app.layout = dbc.Container([
    html.H1('Дашборд погодных данных', className='text-center text-primary mb-4'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Фильтр по городам'),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='city-dropdown',
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
                        options=[
                            {'label': f'Day {day}', 'value': day} for day in [1, 2, 3, 4, 5]
                        ],
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

@dash_app.callback(
    Output('city-dropdown', 'options'),
    [Input('city-dropdown', 'value')]
)
def update_city_options(selected_city):
    cities = [{'label': city, 'value': city} for city in graph.get_cities()]
    return cities

@dash_app.callback(
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
    wind_figure = graph.create_bargraph(day, 'wind_speed', 'Скорость ветра км/ч',[0,52])
    prob_figure = graph.create_bargraph(day, 'chance_fallout', 'Вероятность осадков %',[0,100])
    map = graph.create_map(day)
    return temp_figure, wind_figure, prob_figure, map

if __name__ == '__main__':
    app.run(debug=True)
