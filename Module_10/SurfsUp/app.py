# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify
from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;/api/v1.0/precipitation<br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;/api/v1.0/stations<br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;/api/v1.0/tobs<br/>"
        f"Replace &lt;start&gt; and &lt;end&gt; with Date format: YYYY-MM-DD<br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;/api/v1.0/&lt;start&gt;<br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


# Calculate the most recent measurement date and twelve months ago
measurement_most_recent_date = session.query(measurement.date).order_by(desc(measurement.date)).first()[0]
twelve_months_ago = datetime.strptime(measurement_most_recent_date, '%Y-%m-%d') - timedelta(days=365)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    
    # Perform a query to retrieve the precipitation data for the last 12 months
    precipitation_data_12mo = session.query(measurement.date, measurement.prcp)\
        .filter(measurement.date >= twelve_months_ago)\
        .order_by(measurement.date)\
        .all()

    # Check if any data was returned
    if not precipitation_data_12mo:
        return jsonify({"error": "No precipitation data found for the last 12 months."}), 404
    
    # Convert query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data_12mo}
    
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names."""
    
    # Perform a query to retrieve all station names
    stations = session.query(station.name).all()
    
    # Check if any stations were found
    if not stations:
        return jsonify({"error": "No stations found."}), 404
    
    # Convert query results to a list of station names
    station_list = [name[0] for name in stations]
    
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the most active station over the last 12 months."""

    # Find the most active station
    most_active_station = (
        session.query(measurement.station)
        .group_by(measurement.station)
        .order_by(func.count(measurement.tobs).desc())
        .first()
    )

    # Check if any station was found
    if not most_active_station:
        return jsonify({"error": "No stations found."}), 404

    # Extract the station ID from the result
    most_active_station_id = most_active_station[0]

    # Query for dates and temperature observations for the most active station in the last year
    temp_data = (
        session.query(measurement.date, measurement.tobs)
        .filter(measurement.station == most_active_station_id)
        .filter(measurement.date >= twelve_months_ago)
        .all()
    )

    # Check if any temperature data was found
    if not temp_data:
        return jsonify({"error": "No temperature observations found for the most active station in the last 12 months."}), 404

    # Convert results to a list of temperature observations
    temp_list = [tobs for date, tobs in temp_data]

    return jsonify(temp_list)




@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_andor_end(start, end=None):  # Set end to None if not provided
    # Convert the date strings to datetime objects
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d") if end else None  # Handle end date


    # Query to calculate TMIN, TAVG, TMAX
    query = session.query(
        func.min(measurement.tobs).label('TMIN'),
        func.avg(measurement.tobs).label('TAVG'),
        func.max(measurement.tobs).label('TMAX')
    ).filter(measurement.date >= start_date)

    if end_date:
        query = query.filter(measurement.date <= end_date)

    # Execute the query and fetch the results
    results = query.one_or_none()  # Use one_or_none to avoid exceptions if no results are found

    if results:
        # Convert the results to a dictionary
        temperature_stats = {
            'Average Temperature (TAVG)': results.TAVG,
            'Maximum Temperature (TMAX)': results.TMAX,
            'Minimum Temperature (TMIN)': results.TMIN 
        }
        return jsonify(temperature_stats)
    else:
        return jsonify({"error": "No data found for the specified date range."}), 404



session.close()
if __name__ == '__main__':
    app.run(debug=True)