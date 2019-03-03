import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)


app = Flask(__name__)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    
    rain_results_db = session.query(Measurement.date, Measurement.prcp).all()
    measurements_db = []
    for measurement in rain_results_db:
        measurement_lib_db = {}
        measurement_lib_db[measurement.date] = measurement.prcp
        measurements_db.append(measurement_lib_db)

   
    return jsonify(measurements_db)

@app.route("/api/v1.0/stations")
def stations():
    
    
    rain_results_db = session.query(Station.station).all()

    
    all_stations = list(np.ravel(rain_results_db))

    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    
    rain_results_db = session.query(Measurement).filter(Measurement.date >= '2016-08-23').all()

    
    measurements_db = []
    for measurement in rain_results_db:
        measurement_lib_db = {}
        measurement_lib_db[measurement.date] = measurement.tobs
        measurements_db.append(measurement_lib_db)

    
    return jsonify(measurements_db)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start, end='2017-08-23'):
    
    
    def calc_temps(start_date, end_date):
        
        
        rain_results_db = session.query(Measurement.tobs).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
        
        
        all_rain_results_db = np.ravel(rain_results_db)

        
        temp_min = np.min(all_rain_results_db)
        tavg = np.average(all_rain_results_db)
        temp_max = np.max(all_rain_results_db)
        return temp_min, tavg, temp_max

    temp_min, tavg, temp_max = calc_temps(start, end)
    rain_results_db_dict = {"Minimum Temprature Measured": temp_min.astype(float), "Average Temprature": tavg.astype(float), "Maximum Temprature Measured": temp_max.astype(float)}

    
    return jsonify(rain_results_db_dict)

if __name__ == '__main__':
    app.run(debug=False)
