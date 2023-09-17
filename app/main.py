from fastapi import FastAPI, Response, HTTPException, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.logger import logger
from random import randint, choice

app = FastAPI(debug=True, description="Trivial app for ECS Service Connect")

sad_emoji = "😔"
happy_emoji = "🖖"

@app.get("/")
def read_root():
    """Because of course..."""
    return {"Hello": "World"}


@app.get("/ready", summary="Server readiness", response_description="200 OK, or 503 SERVICE UNAVAILABLE", response_class=PlainTextResponse)
def read_ready():
    return "READY"


@app.get("/health", summary="Health Summary", description="Health Description", response_description="Health Response Description", response_class=PlainTextResponse)
def read_health():
    if choice([True, False]):
        logger.debug(f"Health check passed! {happy_emoji}")
        return "OK"
    logger.error(f"Health check failed with a 500! {sad_emoji}")
    raise HTTPException(status_code=500)


@app.get("/hostname", response_class=PlainTextResponse)
def read_hostname():
    from socket import gethostname
    return gethostname()


@app.get("/teapot", status_code=418, summary="April Fools", response_description="A joke that made its way into an RFC!", response_class=HTMLResponse)
def read_teapot():
    """Every server needs a 418..."""
    logger.warn(f"Looks like the tea has been discovered! 🫖")
    return "eye'm a 🫖\n"


@app.get("/random")
def read_random():
    """Returns a random integer between 99 and 99*99"""
    data = str(randint(99, 99*99))
    return Response(content=data, media_type="text/plain")


@app.get("/request/{item}", response_class=JSONResponse)
def read_response(item: str, request: Request):
    agreeable = [ "base_url", "body", "cookies", "get", "headers", "method", "path_params", "query_params", "state", "url" ]
    if item in agreeable:
        logger.debug(f"Receive request for {item=} returning: {getattr(request, item)}")
        return getattr(request, item)
    logger.error(f"Received invalid request: {item}")
    raise HTTPException(status_code=400)
