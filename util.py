from functools import wraps
from flask import request, abort

def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('api-key') and request.headers.get('api-key') == "50dab7b385ccc4b149dd2e6a2dd9c8a88ce":
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function