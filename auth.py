import re
from allnc.middleware import Middleware

STATIC_TOKEN = "absDMK4"


class TokenMiddleware(Middleware):
    regex = re.compile(r"^Token: (\w+)$")

    def process_request(self, request):
        header = request.headers.get("Authorization", "")
        match = self.regex.match(header)
        token = match and match.group(1) or None
        request.token = token

        # if match:
        #     token = match.group(1)
        # else:
        #     token = None


class InvalidTokenException(Exception):
    ...


def login_required(handler):
    def wrapped_handler(request, response, *args, **kwargs):
        token = getattr(request, "token", None)
        if token is None or token != STATIC_TOKEN:
            raise InvalidTokenException("invalid token")

        return handler(request, response, *args, **kwargs)

    return wrapped_handler


def on_exception(request, response, exception):
    if isinstance(exception, InvalidTokenException):
        response.text = "Token is invalid"
        response.status_code = 401
