1) in order to execute the application, pls.
1.1) use"pip install flask" to install flask first. Our  framework is flask.
1.2) Run the python scripts (db_script.py) to initialize the database
1.3) set enviornment FLASK_APP=webapp.
1.4) execute python -m flask run
1.5) execute db_script.py for database initialization (Optional)
with default testing login account as following
user@gmail.com pass:12345678
admin@gmail.com pass:12345678
oper@gamil.com pass:12345678

user@gmail.com pass:12345678 is used to login in customer page.
admin@gmail.com pass:12345678 is used to login in manager page.
oper@gamil.com pass:12345678 is used to login in operator page.

Description
-Flask as (web framework) and SQLITE (as data storage) is using in this project.
-With hierachy that frontend codes are located as following
    - HTML5 pages for customer (under /templates folder)
    - HTML5 pages for operator (under /templates/admin/ folder)
    - HTML5 pages for manager (under /templates/manager/ folder)
    - resources for pages e.g. css,java script,jquery,images..
      (developed by team or from external parties) (under /static/ folder)
-Backend code mainly on routing, some business logic and database access
    - dataAccess.py (under / project folder) with codes that access database
    - views.py (under / project folder) with codes 1) do routing 2) provide rendered pages from
      templates correspondingly 3) provide api that support ajax from client, with json object exchange.

-db_script.py Script to create database and insert initial data for the project
