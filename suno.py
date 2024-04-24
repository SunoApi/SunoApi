# -*- coding:utf-8 -*-
import json,os

from fastapi import FastAPI, HTTPException, Request, status, Header
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field
from starlette.requests import Request
from urllib.parse import urlparse
import uvicorn
import aiohttp

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Response(BaseModel):
    code: Optional[int] = 0
    msg: Optional[str] = "success"
    data: Optional[Any] = None

@app.get("/")
async def root():
    return Response()

@app.get("/files/{file_name}")
async def files(request: Request, file_name: str):
    # print(request.url._url)
    result = urlparse(request.url._url)
    file_url = "https://cdn1.suno.ai" + result.path.replace("/files", "")
    file_path = result.path.replace("/files", "files")

    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        result = await download(file_url, file_path)
        try:
            if result == "200":
                return FileResponse(file_path)
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