async def application(scope, receive, send):
    event = await receive()
    ...
    await send({"type": "websocket.send", ...: ...})


example_http_event = {
    "type": "http.request",
    "body": b"Hello World",
    "more_body": False,
}

example_websocket_event = {
    "type": "websocket.send",
    "text": "Hello world!",
}

example_http_scope = {
    'type': 'http',
    'method': 'POST',
    'path': '/echo',
    'headers': [...],
    ...: ...,
}
