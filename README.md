# Surf's Up Climate Analysis API

## Overview
This project analyzes climate data for a fictional surf shop business named "Surf's Up". It provides an API (Application Programming Interface) to access and query the climate data stored in a SQLite database. The data includes precipitation measurements, temperature observations, and station information.

## Project Structure
- `Resources/`: Contains the SQLite file used for the analysis.
- `app.py`: This Python script contains the Flask application that serves the API routes.
- `SurfsUp.ipynb`: This Jupyter Notebook contains the data analysis and visualization conducted on the climate data.

## API Routes
The following API routes are available in the application:

1. **Precipitation**: `/api/v1.0/precipitation`
   - Returns a JSON representation of the precipitation data for the last year.

2. **Stations**: `/api/v1.0/stations`
   - Returns a JSON list of weather stations.

3. **Temperature Observations (tobs)**: `/api/v1.0/tobs`
   - Returns temperature observations (tobs) for the most active weather station for the previous year.

4. **Temperature Statistics for a Start Date**: `/api/v1.0/<start>`
   - Accepts a start date in the format `yyyy-mm-dd`.
   - Returns the minimum, average, and maximum temperatures calculated from the given start date to the end of the dataset.

5. **Temperature Statistics for a Start-End Date Range**: `/api/v1.0/<start>/<end>`
   - Accepts start and end dates in the format `yyyy-mm-dd`.
   - Returns the minimum, average, and maximum temperatures calculated from the given start date to the given end date.

## Usage
To run the API, execute `app.py` in your terminal or command prompt: python app.py

Once the server is running, you can access the API routes using a web browser.

## Dependencies
- Flask
- SQLAlchemy
- Pandas



