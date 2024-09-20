import json

async def response_error(status, body, send):
    await send(
        {
            "type": "http.response.start",
            "status": status,
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": body.encode('utf-8'),
        }
    )


async def response_ok(body, send):
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps(body).encode('utf-8'),
        }
    )
