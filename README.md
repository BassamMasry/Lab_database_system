# Hospital_Department_Database

A full lab's database management system for hospitals

## This application depends on:
* os library {setup by default in python}
* binascii  {setup by default in python}
* functools  {setup by default in python}
* flask (the main frame of the server)
* flask_session (to handle cookies)
* tempfile (to handle cookies as a temporary file for enhanced security)
* werkzeug.exceptions (to handle exceptions)
* werkzeug.security (for password functionalities)
* mysql.connector (The main SQL interface)

## How to use the app:
* FOR FIRST TIME ONLY: execute init.py to setup the database
* Open a terminal window
* Modify export.txt file as needed
* Enter the commands from export.txt in the terminal
* execute "flask run"
* copy the generated link in a browser
* use as desired

### To install dependencies please execute the command "pip3 install flask" and download mysql connector from
https://dev.mysql.com/downloads/connector/python/

### To set environment variables in Ubuntu use the terminal command "export <variable name>=<variable value>" WITH NO SPACES between variable name, the equal sign, and variable value.
see exports.txt for more help

### You must specify 'sqlpass' as an environment variable with value `<your sql server password>`

### You must specify 'lab_exec' as an environment variable with value of root directory of this folder
see exports.txt for more help

## To run flask on debugging mode use the terminal commands:
"export FLASK_APP=application.py
export FLASK_DEBUG=1
flask run"
{note: the export statement is set every time a new shell environment is started}
see exports.txt for more help
