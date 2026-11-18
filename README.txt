Bikesharing
===========

A Flask and SQLite demonstration of a bike-sharing service. Customers rent
and return bikes and report defects. Operators review defect reports and
station occupancy. Managers view trip counts and generate reports.

Run the local demo
------------------

The project targets Python 3.7. Pipfile.lock records the original web-app
environment, including Flask 1.1.1, NumPy, pandas and Matplotlib. From the
root of a checkout named Bikesharing, with Python 3.7 and Pipenv available,
run the following in a POSIX shell.

    pipenv sync
    test -e bikeRenting.db || cp bikerenting.db bikeRenting.db
    PYTHONPATH=.. FLASK_APP=Bikesharing.webapp pipenv run python -m flask run

Open http://127.0.0.1:5000/ and use the registration form to create a
local test customer. Sign in to explore the rental and profile pages. The
operator and manager views require the corresponding role in the demo
database. db_script.py defines the sample roles and records.

The working directory matters. The application reads bikeRenting.db and
the checked-in sample is named bikerenting.db. The copy above supplies the
name expected on a case-sensitive filesystem and leaves an existing database
in place. To build a new sample from scratch, run db_script.py once in a
fresh working directory. It inserts fixed sample IDs and can report duplicate
keys if run on an already-seeded database.

Where the code lives
--------------------

webapp.py loads the Flask application and views.py registers the routes.
dataAccess.py handles SQLite queries. Customer pages live under templates/,
operator pages under templates/admin/ and manager reports under
templates/manager/. The static/ directory holds styles, scripts and images.
Sample charts from the trip analysis are in visualzation_result/.
