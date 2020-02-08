import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask routes
@app.route("/")
def index():
    return (
        f"Welcome to the Climate app <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_month = last_date[0].split("-")[1]
    last_year = last_date[0].split("-")[0]
    previous_year = int(last_year) - 1
    
    begin_period = dt.date(previous_year, int(last_month), 1)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= begin_period).\
                order_by(Measurement.date.desc()).all()
    
    date = [result[0] for result in results]
    prcp = [result[1] for result in results]

    prcp_dict = {}
    for date, prcp in results:
        prcp_dict[date] = prcp
        
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations_count = session.query(Measurement.station, func.count(Measurement.station)).\
                        group_by(Measurement.station).all()

    station_list = [result[0] for result in stations_count]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_month = last_date[0].split("-")[1]
    last_year = last_date[0].split("-")[0]
    previous_year = int(last_year) - 1
    
    begin_period = dt.date(previous_year, int(last_month), 1)

    # Query the last 12 months of temperature observation data
    station_data = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= begin_period).\
                    order_by(Measurement.date.desc()).all()

    dates_tobs = []
    for date, tobs in station_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        dates_tobs.append(tobs_dict)

    return jsonify(dates_tobs)

@app.route("/api/v1.0/<start>")
def stats_start(start):
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = last_date[0]
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end_date).all()


    tmin = round(results[0][0], 0)
    tavg = round(results[0][1], 0)
    tmax = round(results[0][2], 0)
    
    stats_list = []
    stats_dict = {"Minimum temperature": tmin, "Average temperature": tavg, "Maximum temperature": tmax}
    stats_list.append(stats_dict)
       

    return jsonify(stats_list)

@app.route("/api/v1.0/<start>/<end>")
def stats_start_end(start, end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    tmin = round(results[0][0], 0)
    tavg = round(results[0][1], 0)
    tmax = round(results[0][2], 0)
    
    stats_list = []
    stats_dict = {"Minimum temperature": tmin, "Average temperature": tavg, "Maximum temperature": tmax}
    stats_list.append(stats_dict)
       
    return jsonify(stats_list)

if __name__ == '__main__':
    app.run(debug=True)