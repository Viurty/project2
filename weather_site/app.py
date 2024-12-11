from flask import Flask
from flask import request
from flask import render_template
from weather_forecast import Forecast, error503
from weather_logic import Logic, days


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        start_city = request.form["city1"]
        end_city = request.form["city2"]
        day_end = int(request.form["days"])
        if day_end > 5:
            return render_template('error.html',error='Прогноз доступен только на пять дней вперед.')
        forecast = Forecast(start_city, end_city, 0, day_end)
        try:
            logic = Logic(forecast.get_all_data(), start_city, end_city)
        except error503:
            return render_template('error.html',error='Проблема с подключением к серверу.')
        except:
            return render_template('error.html',error='Неправильно введено имя города. Попробуйте написать город на английском.')
        start_color, start_res = logic.get_res_start()
        end_color, end_res = logic.get_res_end()
        start_weather = forecast.get_scpecific(start_city)
        end_weather = forecast.get_scpecific(end_city)
        return render_template('res_page.html',
                               start_city=start_city,
                               end_city=end_city,
                               start_weather=start_weather,
                               end_weather=end_weather,
                               end_res=end_res,
                               start_res=start_res,
                               start_color=start_color,
                               end_color=end_color,
                               day=days(day_end))
    return render_template('form_page.html')


if __name__ == '__main__':
    app.run(debug=True)
