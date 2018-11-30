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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt;<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all dates with precipitation"""
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict[measurement.date] = measurement.prcp
        all_measurements.append(measurement_dict)

   
    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    
    results = session.query(Station.station).all()

    
    all_stations = list(np.ravel(results))

    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all dates with temperature observations starting one year prior to last date"""
    
    results = session.query(Measurement).filter(Measurement.date >= '2016-08-23').all()

    
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict[measurement.date] = measurement.tobs
        all_measurements.append(measurement_dict)

    
    return jsonify(all_measurements)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start, end='2017-08-23'):
    """Return a list of temperature metrics from a given start date to the last date"""
    
    def calc_temps(start_date, end_date):
        """Return a list of temperature metrics from a given start date to a given end date"""
        
        results = session.query(Measurement.tobs).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
        
        
        all_results = np.ravel(results)

        
        tmin = np.min(all_results)
        tavg = np.average(all_results)
        tmax = np.max(all_results)
        return tmin, tavg, tmax

    tmin, tavg, tmax = calc_temps(start, end)
    results_dict = {"TMIN": tmin.astype(float), "TAVG": tavg.astype(float), "TMAX": tmax.astype(float)}

    
    return jsonify(results_dict)

if __name__ == '__main__':
    app.run(debug=False)