from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse

from url_shortener.client_testing import DBClientPing
from url_shortener.hasher.hash_manager import Hash
from url_shortener.host_client_detail import push_client_ip_to_redis

app = FastAPI()
DBClientPing()


@app.get("/get_shorten_url/")
async def get_shorten_url(request: Request, query: Union[str, None] = None):
    await push_client_ip_to_redis(client_ip=request.client.host)
    hash_object = Hash()
    hash_id = await hash_object.get_hash(query)
    return {"tiny_url": f"http://0.0.0.0:8000/tiny?query={hash_id}"}


@app.get("/tiny/")
async def get_full_url(request: Request, query: Union[str, None] = None):
    await push_client_ip_to_redis(client_ip=request.client.host)
    hash_object = Hash()
    url = await hash_object.get_full_url(query)
    if url:
        return RedirectResponse(url=url, status_code=301)
    return {"Error": "Sorry we could find any url related"}


@app.get("/")
async def get_homepage():
    return FileResponse("url_shortener/templates/homepage.html")
