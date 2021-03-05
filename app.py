import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation dates"""
    # Query all precipitation
    results = session.query(Measurements.date, Measurements.prcp).all()

    session.close()

    # # Convert list of tuples into normal list
    # all_precipitation = list(np.ravel(results))


    # return jsonify(all_precipitation)

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    stationResults = session.query(Stations.station).all()

    session.close()

    all_station = []
    for station in stationResults:
        station_dict = {}
        station_dict["station"] = station
        all_station.append(station_dict)

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all tobs
    tobsResults = session.query(Measurements.date, Measurements.tobs).all()

    session.close()

    all_tobs = []
    for date, tobs in tobsResults:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    start = session.query(func.max(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).all()

    session.close()

    all_start = []
    for tobs in start:
        start_dict = {}
        start_dict["tobs"] = tobs
        all_start.append(start_dict)

    return jsonify(all_start)

if __name__ == '__main__':
    app.run(debug=True)
