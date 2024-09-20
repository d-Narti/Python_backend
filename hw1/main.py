import math
import json

from urllib.parse import parse_qs
from statistics import mean
from responses_hw1 import response_ok, response_error

async def app(scope, receive, send):
    message = await receive()

    if message["type"] == "http.disconnect":
        print(f"Received message:", message)

    if scope["path"] == '/factorial' and scope["method"] == 'GET':

        query_string = scope["query_string"].decode('utf-8')
        n = parse_qs(query_string)

        try:
            clean_n = int(n.get('n', [None])[0])
        except (ValueError, TypeError):
            await response_error(422, "Invalid value for n, must be non-negative number", send)
            return
        if clean_n < 0:
            await response_error(400, "Invalid value for n, must be non-negative number", send)
            return
        await response_ok({"result": math.factorial(clean_n)}, send)
        return
    elif scope["path"].startswith('/fibonacci') and scope["method"] == 'GET':

        n = scope["path"].split('/')

        try:
            clean_n = int(n[2]) if len(n) > 2 else None
        except ValueError:
            await response_error(422, "Invalid value for n, must be non-negative number", send)
            return
        if clean_n is None:
            await response_error(422, "Invalid value for n, must be non-negative number", send)
            return
        if clean_n < 0:
            await response_error(400, "Invalid value for n, must be non-negative number", send)
            return
        fib1, fib2 = 1, 1
        for _ in range(clean_n - 2):
            fib1, fib2 = fib2, fib1 + fib2

        await response_ok({"result": fib2}, send)
        return
    elif scope['path'] == '/mean' and scope['method'] == 'GET':

        try:
            body = json.loads(message.get('body', b'').decode('utf-8'))
        except json.JSONDecodeError:
            await response_error(422, "Invalid value for body, must be non-empty array of floats", send)
            return
        if not isinstance(body, list):
            await response_error(422, "Invalid value for body, must be non-empty array of floats", send)
            return
        if len(body) == 0:
            await response_error(400, "Invalid value for body, must be non-empty array of floats", send)
            return
        try:
            float_array = [float(i) for i in body]
        except ValueError:
            await response_error(422, "Invalid value for body, must be non-empty array of floats", send)
            return
        await response_ok({"result": mean(float_array)}, send)
        return
    else:
        await response_error(404, "There is no such path", send)
        return
