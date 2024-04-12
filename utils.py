# -*- coding:utf-8 -*-

import json
import os
import time

import aiohttp
import requests

COMMON_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Referer": "https://suno.com/",
    "Origin": "https://suno.com",
}

BASE_URL = "https://studio-api.suno.ai"

def fetch(url, headers=None, data=None, method="POST"):
    if headers is None:
        headers = {}
    headers.update(COMMON_HEADERS)
    if data is not None:
        data = json.dumps(data)

    try:
        resp = None
        if method == "GET":
            resp = requests.get(url=url, headers=headers)
        else:
            resp = requests.post(url=url, headers=headers, data=data)
        if resp.status_code != 200:
            print(resp.text)
        return resp.json()
    except Exception as e:
        return {"detail":str(e)}


def get_feed(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/feed/?ids={ids}"
    response = fetch(api_url, headers, method="GET")
    return response


def generate_music(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/v2/"
    response = fetch(api_url, headers, data)
    return response


def generate_lyrics(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/"
    data = {"prompt": prompt}
    return fetch(api_url, headers, data)


def get_lyrics(lid, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/{lid}"
    return fetch(api_url, headers, method="GET")

def local_time():
    return  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())