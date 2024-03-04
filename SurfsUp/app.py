# Import the dependencies
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

# Create Flask app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define routes
@app.route("/")
def home():
    """Homepage with list of available routes."""
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data for the last year."""
    # Calculate the date one year ago from the last date in the database
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Query precipitation data for the last year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close()
    
    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations."""
    # Query all stations
    stations = session.query(Station.station, Station.name).all()

    session.close()
    
    # Convert list of tuples into normal list
    station_list = [{"Station ID": station, "Name": name} for station, name in stations]
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temperature observations for the most active station for the previous year."""
    # Find the most active station
    most_active_station = session.query(Measurement.station,
                                        func.count(Measurement.station).label('count')).\
                                        group_by(Measurement.station).\
                                        order_by(func.count(Measurement.station).desc()).first()
    
    # Extract the station ID of the most active station
    most_active_station_id = most_active_station[0]
    
    # Calculate the date one year ago from the last date in the database
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Query temperature observations for the previous year for the most active station
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == most_active_station_id).\
                filter(Measurement.date >= one_year_ago).\
                filter(Measurement.date <= most_recent_date).all()
    
    session.close()
    
    # Convert list of tuples into normal list
    tobs_list = [{"Date": date, "Temperature (°F)": tobs} for date, tobs in tobs_data]
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def calc_temps_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return the minimum, average, and maximum temperatures for a start date."""
    # Convert start date string to datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # Calculate the most recent date from the database
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    
    # Query temperatures greater than or equal to the start date
    temps = session.query(func.min(Measurement.tobs),
                          func.avg(Measurement.tobs),
                          func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
    
    session.close()
    
    # Extract the temperature values from the query result
    min_temp, avg_temp, max_temp = temps[0]

    # Create a dictionary to hold the temperature data
    temp_data = {
        "Start Date": start_date.strftime('%Y-%m-%d'),
        "End Date": most_recent_date.strftime('%Y-%m-%d'),
        "Min Temperature": min_temp,
        "Average Temperature": avg_temp,
        "Max Temperature": max_temp
    }
    
    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def calc_temps_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return the minimum, average, and maximum temperatures for a start-end range."""
    # Convert start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    # Query temperatures between the start and end dates
    temps = session.query(func.min(Measurement.tobs),
                          func.avg(Measurement.tobs),
                          func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all()
    
    session.close()
    
    # Extract the temperature values from the query result
    min_temp, avg_temp, max_temp = temps[0]

    # Create a dictionary to hold the temperature data
    temp_data = {
        "Start Date": start_date.strftime('%Y-%m-%d'),
        "End Date": end_date.strftime('%Y-%m-%d'),
        "Min Temperature": min_temp,
        "Average Temperature": avg_temp,
        "Max Temperature": max_temp
    }
    
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)
