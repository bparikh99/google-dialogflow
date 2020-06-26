from flask import Flask,request,make_response
import os
from flask_cors import CORS,cross_origin
import pyowm
import json


app=Flask(__name__)

owmapikey="6b48a0640ad76920410b9f72d72e4322"
owm=pyowm.OWM(owmapikey)


@app.route('/webhook',methods=['POST'])
@cross_origin()
def webcall():
    req=request.get_json(silent=True,force=True)
    print("Request::")

    print(json.dumps(req))

    res=processRequest(req)

    res=json.dumps(res)
    print(res)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r

def processRequest(req):
    result=req.get("queryResult")
    parameters=result.get("parameters")
    city=parameters.get('geo-city')
    observation=owm.weather_at_place(city)
    w=observation.get_weather()

    wind_res=w.get_wind()
    wind_speed=str(wind_res.get("speed"))

    humidity=str(w.get_humidity())

    celsius_result=w.get_temperature('celsius')
    celsius_result=str(celsius_result['temp'])

    speech="Todays Weather in "+ city +"\n"+"Temprature "+celsius_result + "\n"+"Humidity " + humidity +"\n"+ "wind Speed is" + wind_speed 

    return {
         "fulfillmentText":speech,
         "displayText":speech

     }




if __name__ == "__main__":
    app.run(debug=True)