# Animal Weights API

To run the API, create a virtualenv with Python 3.6+.

Inside the virtualenv, run `pip install -r requirements.txt` from the root of the `weightsapi` directory.

**IMPORTANT**: Inside `./weightsapi/settings.py`, add some random value to the `SECRET_KEY` const.

Then run `./manage.py migrate` to create the SQLite database with necessary tables.

Finally, run `./manage.py runserver 0:8000` to launch the Python webserver.

The site will be accessible via `http://localhost:8000/animals/`