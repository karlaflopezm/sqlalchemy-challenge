# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


# 1. Start at the homepage and list all available routes.

@app.route("/")
def homepage():

    return(

    f"Welcome to the HomePage. Available API routes.<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br>"
    f"/api/v1.0/<start>/<end><br>"

    )

# 2a. Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value.
# 2b. Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation_analysis():
    session = Session(engine)

    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d").date()
    query_date = most_recent_date - dt.timedelta(days = 365)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).all()
    
    session.close()

    precip_analysis = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precip_analysis)

# 3. Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station_list():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()
    
    return jsonify([station[0] for station in stations])

# 4a. Query the dates and temperature observations of the most-active station for the previous year of data.
# 4b. Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d").date()
    query_date = most_recent_date - dt.timedelta(days=365)
    
    temp_list = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station == most_active_station).all()
    
    session.close()
    
    return jsonify([temp[1] for temp in temp_list])

#5a. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start 
# or start-end range.
# 5b.For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#5c For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    """Returns TMIN, TAVG, and TMAX for a given start date or date range."""
    session = Session(engine) 
    
    try:
        # Convert start date (and end date if provided)
        start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = dt.datetime.strptime(end, "%Y-%m-%d").date() if end else None

        # Query for temperature statistics
        query = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start_date)

        if end_date:
            query = query.filter(Measurement.date <= end_date)

        result = query.one()
        session.close()  # Close session

        # Format response
        temp_stats = {
            "start_date": start,
            "end_date": end if end else "latest",
            "TMIN": result[0],
            "TAVG": round(result[1], 2) if result[1] else None,  # Round avg temp
            "TMAX": result[2]
        }

        return jsonify(temp_stats)
    
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
