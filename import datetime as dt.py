import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation<br/>")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(func.count(Station.station)).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    temp = session.query(Measurement.tobs)
    filter(Measurement.station == 'USC00519397')
    return jsonify(temp)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    Min = func.min(Measurement.tobs) 
    avg = func.avg(Measurement.tobs)
    Max = func.max(Measurement.tobs)
    
    if Max == None:
        results = session.query(avg)
        filter(Measurement.date >= Min).all()
        return jsonify(results)

    results = session.query(avg)
    filter(Measurement.date >= start)
    filter(Measurement.date <= end).all()
    return jsonify(results)

if __name__ == '__main__':
    app.run()
