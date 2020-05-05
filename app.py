import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from dateutil.relativedelta import relativedelta

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
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/", methods=['GET'])
def welcome():
    """List all available api routes."""
    return (f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>")


@app.route("/api/v1.0/precipiation", methods=['GET'])
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all date and corresponding precipitation"""
    # Query all passengers

    results = session.query(Measurement.date, func.avg(
        Measurement.prcp)).group_by(Measurement.date)

    results_dict = [{
        'date': u,
        'precipitation': v
    } for (u, v) in results.all()]
    session.close()
    return jsonify(results_dict)


@app.route("/api/v1.0/stations", methods=['GET'])
def stations():
    session = Session(engine)
    results = session.query(Station)

    for _row in results.all():
        print(_row.station)

    retults_dict = [{
        "station": r.station,
        "name": r.name,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "elevation": r.elevation
    } for r in results.all()]
    session.close()
    return jsonify(retults_dict)


@app.route("/api/v1.0/tobs", methods=['GET'])
def temperature():
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(
        desc(Measurement.date)).first()
    one_year_delta = dt.datetime.strptime(latest_date[0],
                                          '%Y-%m-%d') - relativedelta(years=1)

    results = session.query(Measurement.date, func.avg(
        Measurement.prcp)).filter(Measurement.date > one_year_delta).group_by(
            Measurement.date)

    retults_dict = [{
        "date": r[0],
        "temperature": r[1],
    } for r in results.all()]
    session.close()
    return jsonify(retults_dict)


@app.route("/api/v1.0/<start>", defaults={'end': None}, methods=['GET'])
@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def temp_date_range(start, end):
    session = Session(engine)
    start_date = start
    end_date = end
    if end is None:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date)
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)

    retults_dict = [{
        "Tmin": r[0],
        "Tavg": r[1],
        "Tmax": r[2],
    } for r in results.all()]
    session.close()
    return jsonify(retults_dict)


if __name__ == '__main__':
    app.run(debug=True)
