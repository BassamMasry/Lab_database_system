import os

from flask import redirect, session,render_template
from functools import wraps

def apology(name,code):
	return render_template("control/error.html",name=name, code=code)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (session.get("token") is None) or (session.get("username") is None):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    

def admin_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (session.get("admin") is None) or (session.get("password") is None):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check_admin_cookies():
    user = os.environ.get("admin1_user") == session.get("admin") or os.environ.get("admin2_user") == session.get("admin") or os.environ.get("admin3_user") == session.get("admin")
    passer = os.environ.get("admin1_pass") == session.get("password") or os.environ.get("admin2_pass") == session.get("password") or os.environ.get("admin3_pass") == session.get("password")
    if user and passer:
        return True
    return render_template("control/banned.html")

def check_admins():
    if not os.environ.get("admin1_user"):
        raise RuntimeError("admin1_user not set")
        exit(1)
    if not os.environ.get("admin1_pass"):
        raise RuntimeError("admin1_pass not set")
        exit(1)
		
    if not os.environ.get("admin2_user"):
        raise RuntimeError("admin2_user not set")
        exit(1)
    if not os.environ.get("admin2_pass"):
        raise RuntimeError("admin2_pass not set")
        exit(1)
		
    if not os.environ.get("admin3_user"):
        raise RuntimeError("admin3_user not set")
        exit(1)
    if not os.environ.get("admin3_pass"):
        raise RuntimeError("admin3_pass not set")
        exit(1)
    return True

def logger(db, admin, o_type, t_code, operation):
    """log opperation with paratmenters db as connection cursor, admin for admin, o_type as operand type, t_code is the code of the operand, operation is add,modify, or delete"""
    db.execute("INSERT INTO log (admin, type, t_code, operation, date) VALUES ('{admin}', '{o_type}', '{coder}', '{operation}', NOW());".format(admin = admin, o_type = o_type, coder = t_code, operation = operation))
    return None
