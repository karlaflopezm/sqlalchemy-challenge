# SQLAlchemy Climate Analysis Challenge

## Instructions

### Overview
Analyze climate data from Honolulu, Hawaii, using Python, SQLAlchemy, Pandas, and Matplotlib. After, create a Flask API to expose your analysis results.

### Part 1: Analyze and Explore the Climate Data

#### 1. Database Connection
- I have used `SQLAlchemy create_engine()` to connect to the SQLite database.
- Then `SQLAlchemy automap_base()` to reflect the tables (`station` and `measurement`).
- Create a session to interact with the database.

#### 2. Precipitation Analysis
- Find the most recent date in the dataset.
- Retrieve the last 12 months of precipitation data.
- Load the results into a Pandas DataFrame.
- Sort the data by date.
- Plot the precipitation data.
- Print summary statistics for the precipitation data.

#### 3. Station Analysis
- Calculate the total number of stations.
- Identify the most active station (the one with the most records).
- Retrieve the lowest, highest, and average temperature for this station.
- Get the last 12 months of temperature observation (TOBS) data for the most active station.
- Plot the results as a histogram with `bins=12`.

### Part 2: Design Your Climate App

Create a Flask API to serve the climate analysis results. Implement the following routes:

#### `/`
- Lists all available API routes.

#### `/api/v1.0/precipitation`
- Returns the last 12 months of precipitation data as a JSON dictionary (`date: prcp`).

#### `/api/v1.0/stations`
- Returns a JSON list of all stations in the dataset.

#### `/api/v1.0/tobs`
- Returns a JSON list of temperature observations for the most active station for the previous year.

#### `/api/v1.0/<start>`
- Returns the minimum, average, and maximum temperatures from the given `start` date.

#### `/api/v1.0/<start>/<end>`
- Returns the minimum, average, and maximum temperatures between the `start` and `end` dates.

### Hints
- Use `join()` to combine `station` and `measurement` tables.
- Use `jsonify()` to format API responses.
- Ensure your session is closed after executing queries.

---

## To Run the Flask App

1. Open the integrated terminal.
2. Run the Flask application with the command below:
      python3 app.py
   
3. Open a browser and navigate to `http://127.0.0.1:5000/` to access the API routes.

---

