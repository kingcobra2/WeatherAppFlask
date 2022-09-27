from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret"
db = SQLAlchemy()
DB_NAME = 'database.db'

@app.route('/', methods=["GET", "POST"])
def home():
    #first_step_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&appid=702aa28ac324aba75a8ae1c7e05bb923'
    sec_step_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=imperial&appid=7e085e8015c70bec0c4b339989937639"
    #city = 'Las Vegas'
    lat = 36.16
    lon = -115.14

    #r = requests.get(first_step_url.format(city)).json()
    #print(r)

    final = requests.get(sec_step_url.format(lat, lon)).json()
    print(final)



    return render_template('main.html')






