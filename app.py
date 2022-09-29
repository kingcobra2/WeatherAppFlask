from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)

def get_weather_data(city):
    #Retrieve the lat and lon coordinates for the given city
    first_step_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&appid=7e085e8015c70bec0c4b339989937639'
    #feed the lat and lon into the API for info
    sec_step_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=imperial&appid=7e085e8015c70bec0c4b339989937639"
    cities = City.query.all()

    for city in cities:
        r = requests.get(first_step_url.format(city.name)).json()
        
        lat = r[0]['lat']
        lon = r[0]['lon']

        final = requests.get(sec_step_url.format(lat, lon)).json()
        return final

@app.route('/', methods=["GET"])
def home_get():
    #Retrieve the lat and lon coordinates for the given city
    first_step_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&appid=7e085e8015c70bec0c4b339989937639'
    #feed the lat and lon into the API for info
    sec_step_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=imperial&appid=7e085e8015c70bec0c4b339989937639"
    cities = City.query.all()

    weather_data = []
    for city in cities:
        r = requests.get(first_step_url.format(city.name)).json()
        
        lat = r[0]['lat']
        lon = r[0]['lon']


        final = requests.get(sec_step_url.format(lat, lon)).json()
        weather = {
            'city' : city.name,
            'temperature' : final['current']['temp'],
            'description' : final['current']['weather'][0]['description'],
            'icon': final['current']['weather'][0]['icon']
        }
        
        weather_data.append(weather)

    return render_template('main.html', weather_data= weather_data)

@app.route('/', methods=["POST"])
def home_post():
    if request.method == "POST":
        new_city = request.form.get('city')
        if new_city:
            existing_city = City.query.filter_by(name=new_city).first()

            if not existing_city:
        
                    new_city_obj = City(name=new_city)
                    db.session.add(new_city_obj)
                    db.session.commit()
                    flash('City added succesfully!')
                
            else:
                err_msg = 'City already exists!'
                flash(err_msg, 'error')
                    
    return redirect(url_for('home_get'))






