
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
# List all available api routes
    return (
        f"Available Routies:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def JSON_dates():
# Return the JSON representation of dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    JSON_list = []
    for date, prcp in results:
        JSON_dict = {}
        JSON_dict[date] = prcp
        JSON_list.append(JSON_dict)
    return jsonify(JSON_list)

@app.route("/api/v1.0/stations")
def JSON_stations():
# Return a JSON list of stations from the dataset
    results = session.query(Station)
    station_list = [i.station for i in results]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_observations():
# Return a JSON list of temperature observations for the previous year
    date = dt.datetime(2017, 8, 22) - dt.timedelta(days=365)
    sel = [Measurement.station, Measurement.date, Measurement.tobs]
    results = session.query(*sel).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start():
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
results = session.query(*sel).\
    filter(func.strftime('%Y-%m-%d', Measurement.date >= start)).all()
return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end():
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range
sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
results = session.query(*sel).\
    filter(func.strftime('%Y-%m-%d', Measurement.date >= start)).\
    filter(func.strftime('%Y-%m-%d', Measurement.date <= end)).all()
return jsonify(results)