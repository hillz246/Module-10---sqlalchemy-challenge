**Module-10---sqlalchemy-challenge**
Assignment 10 - Module 10 - sqlalchemy-challenge

#Overview:
I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I decide to do a climate analysis about the area.

The Weather API is a Flask application that provides access to weather data from a SQLite database. It allows users to retrieve precipitation and temperature observations from various weather stations in Hawaii. This API offers endpoints for accessing recent weather data, including temperature observations for the most active stations over the past year.

## Structure:
The project is organized into the following directories and files:

1. SurfsUp has two files. app.py and climate_starter.ipynb
* app.py is a Main application file to run the Flask API.
   ![python_app_py](https://github.com/user-attachments/assets/c363fe5e-ce2e-4905-a6d9-3c576568c16e)

- climate_starter.ipynb is a Jupyter Notebook for initial data exploration and analysis.

2. Resources/ folder has three files, two of them are csv and one SQLite
* hawaii.sqlite: SQLite database containing weather data. hawaii_measurements.csv: CSV file with measurement data. hawaii_stations.csv: CSV file with station information.

### Technologies:
Flask is using for a web framework for building the API. SQLAlchemy is for an ORM for interacting with the SQLite database. SQLite is for a lightweight database for storing weather data. Jupyter Notebook is for an interactive environment for data exploration and analysis. Pandas is for a data manipulation library for handling structured data. Matplotlib is for a plotting library for visualizing data.
