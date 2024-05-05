# -*- coding:utf-8 -*-
import json,os,io

from fastapi import FastAPI, HTTPException, Request, status, Header
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse,Response
from fastapi.responses import StreamingResponse
from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field
from starlette.requests import Request
from urllib.parse import urlparse
import uvicorn
import aiohttp
import os,sys,re
import mimetypes

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class jsonResponse(BaseModel):
    code: Optional[int] = 0
    msg: Optional[str] = "success"
    data: Optional[Any] = None

@app.get("/")
async def root():
    return jsonResponse()

@app.get("/files/{file_name}")
async def files(request: Request, file_name: str):
    # print(request.url._url)
    result = urlparse(request.url._url)
    file_url = "https://cdn1.suno.ai" + result.path.replace("/files", "")
    file_path = result.path.replace("/files", "files")

    media_type = "text/plain"
    if file_path.endswith(".png"):
        media_type = "image/png"
    elif file_path.endswith(".mp3"):
        media_type = "audio/mpeg"
    elif file_path.endswith(".mp4"):
        media_type = "video/mp4"
    else:
        media_type = "application/octet-stream"

    if os.path.exists(file_path):
        return write_file(request, file_path, media_type)
    else:
        result = await download(file_url, file_path)
        try:
            if result == "200":
                return write_file(request, file_path, media_type)
            else:
                return result
        except Exception as e:
            return {"detail":str(e)}


async def download(url, filename):
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(filename, 'wb') as f:
                        f.write(await response.read())
                    return str(response.status)
                else:
                    return {"detail":str(response.status)}
        except Exception as e:
            return {"detail":str(e)}

def write_file(request, file_path, media_type):
    if file_path.endswith(".png"):
        return FileResponse(file_path)
        # return StreamingResponse(open(file_path, 'rb'), media_type=media_type)
    else:
        start, end = get_range(request)
        return partial_response(media_type, file_path, start, end)

def get_buff_size(file_size):
    buff_size = 2097152
    if file_size > 1073741824:
        buff_size = 4194304
    return buff_size

def get_range(request):
    range = request.headers.get('Range')
    m = None
    if range:
        m = re.match(r'bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None

def partial_response(media_type, path, start, end=None):
    if not os.path.exists(path):
        return {"detail":"file not fount!"}
    file_size = os.path.getsize(path)
    buff_size = get_buff_size(file_size)

    if end is None:
        end = start + buff_size - 1
    end = min(end, file_size - 1)
    end = min(end, start + buff_size - 1)
    length = end - start + 1

    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Range": "bytes {0}-{1}/{2}".format(start, end, file_size,)
    }

    return Response(bytes, 206, headers, media_type, None)
    