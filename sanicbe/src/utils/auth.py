from functools import wraps
from sanic import text
from sanic.log import logger

import jwt


def check_token(request):
    if not request.token:
        return False

    try:
        jwt.decode(
            request.token, request.app.config.SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def decoded_token(request):
    return jwt.decode(
        request.token, request.app.config.SECRET, algorithms=["HS256"])


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)
