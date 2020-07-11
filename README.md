# Climate Flask API
![Histogram](https://github.com/remco-mooij/climate-api/blob/master/histogram.png)

Using Python and SQLalchemy, [climate analysis and data exploration](https://github.com/remco-mooij/climate-app/blob/master/climate_analysis.ipynb) was performed on a [climate database](https://github.com/remco-mooij/climate-app/blob/master/Resources/hawaii.sqlite).
The data was used to calculate the minimum, maximum and average temperatures on Hawaii between July 1 - 14 to plan for a trip to Honolulu.

A Flask API was designed based on the SQLAlchemy ORM queries that were developed. This API has the following available routes:


* / (home page with list of available routes)
* /api/v1.0/precipitation
* /api/v1.0/stations
* /api/v1.0/tobs
* /api/v1.0/(enter_start_date)
* /api/v1.0/(enter_start_date)/(enter_end_date)

To use the Flask API, run the following command in the root directory of the repo:
```
python app.py
```
