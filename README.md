# Animal Weights API

To run the API, create a virtualenv with Python 3.6+.

Inside the virtualenv, run `pip install -r requirements.txt` from the root of the `weightsapi` directory.

**IMPORTANT**: Inside `./weightsapi/settings.py`, add some random value to the `SECRET_KEY` const.

Then run `./manage.py migrate` to create the SQLite database with necessary tables.

Finally, run `./manage.py runserver 0:8000` to launch the Python webserver.

The site will be accessible via `http://localhost:8000/animals/`

To run tests: `./manage.py test`

# Task Details

A time limit of *3 hours* was imposed on this task.

**Goal**: Build an API endpoint that records animal weights at a given point in time. Build a second endpoint that lets users query estimated weights for a given date (e.g. user has records for Jan 1 and Jan 5, but wants the estimated weight for Jan 3).

Uses Linear Interpolation / Extrapolation to calculate the estimated weight of an anmial for a given datetime timestamp.

# Implementation Notes
- Used scipy for calculating the Linear Interpolation/Extrapolation due to time constraints and its well-tested implementation. 

- Data is stored in SQLite.

- The estimate_weight endpoint stores the calculated weight in the DB for future, repeated lookups. This acts a sort of cache for the estimated values.
    - "Cache" busting was not implemented to remove or invalidate the stored estimated weights if new data BEFORE the estimated date was added. E.g if we have a stored estimated weight for Jan 6 and a recorded weight for Jan 5 is added, the Jan 6 estimated weight will still exist even though it could be affected by this new value.

- Project set up is simplified due to 3-hour constraint. Typical installation would use separate settings files for different environments.