# Hospital_Department_Database

A full lab's database management system for hospitals

This application depends on:
- os library {setup by default in python}
- binascii  {setup by default in python}
- functools  {setup by default in python}
- cs50 (for SQL query parameterization)
- flask (the main frame of the server)
- flask_session (to handle cookies)
- tempfile (to handle cookies as a temporary file for enhanced security)
- werkzeug.exceptions (to handle exceptions)
- werkzeug.security (for password functionalities)
- mysql.connector (The main SQL interface)

To install dependencies please execute the command "pip3 install cs50 flask" and download mysql connector from
https://dev.mysql.com/downloads/connector/python/

to set environment variables in Ubuntu use the terminal command "export <variable name>=<variable value>" WITH NO SPACES between variable name, the equal sign, and variable value.
see exports.txt for more help

you must specify 'sqlpass' as an environment variable with value `<your sql server password>`
you must specify 'lab_exec' as an environment variable with value of root directory of this folder
see exports.txt for more help

to run flask on debugging mode use the terminal commands {note: the export statement can be used only once} 
"export FLASK_APP=application.py
export FLASK_DEBUG=1
flask run"
see exports.txt for more help
