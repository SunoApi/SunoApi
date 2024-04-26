# -*- coding:utf-8 -*-

import json
import os
import time

import requests,random

COMMON_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
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
        requests.packages.urllib3.disable_warnings()
        if method == "GET":
            resp = requests.get(url=url, headers=headers, verify=False)
        else:
            resp = requests.post(url=url, headers=headers, data=data, verify=False)
        if resp.status_code != 200:
            print(resp.text)
        result = resp.text.replace('https://cdn1.suno.ai/', 'https://res.sunoapi.net/files/')
        return json.loads(result)
        # return resp.json()
    except Exception as e:
        return {"detail":str(e)}


def get_feed(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/feed/?ids={ids}"
    response = fetch(api_url, headers, method="GET")
    return response

def get_page_feed(page, token):
    headers = {"Authorization": f"Bearer {token}"}
    # api_url = f"{BASE_URL}/api/feed/?ids={ids}"
    api_url = f"{BASE_URL}/api/feed/?page={page}"
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

def check_url_available(url):
    while True:
        # 每间隔一秒钟检查一次url文件大小
        file_size = get_file_size(url)
        if file_size >= 1024*1024:
            print(local_time() + f" ***check_url_available -> {url} 文件大小：{file_size} 大于1MB可访问到***\n")
            break
        print(local_time() + f" ***check_url_available -> {url} 文件大小：{file_size} 小于1MB继续检查***\n")
        time.sleep(1)

def get_file_size(url):
    try:
        requests.packages.urllib3.disable_warnings()
        resp = requests.head(url, verify=False)
        if resp.status_code == 200:
            file_size = resp.headers.get('Content-Length')
            if file_size:
                return int(file_size)
            else:
                return 0
        else:
            return 0
    except Exception as e:
        return 0

def get_random_style():
    genres = ["chinese pop","acoustic", "aggressive", "anthemic", "atmospheric", "bouncy", "chill", "dark", "dreamy", "electronic", "emotional", "epic", "experimental", "futuristic", "groovy", "heartfelt", "infectious", "melodic", "mellow", "powerful", "psychedelic", "romantic", "smooth", "syncopated", "uplifting"]
    vibes = ["afrobeat", "anime", "ballad", "bedroom pop", "bluegrass", "blues", "classical", "country", "cumbia", "dance", "dancepop", "delta blues", "electropop", "disco", "dream pop", "drum and bass", "edm", "emo", "folk", "funk", "future bass", "gospel", "grunge", "grime", "hip hop", "house", "indie", "j-pop", "jazz", "k-pop", "kids music", "metal", "new jack swing", "new wave", "opera", "pop", "punk", "raga", "rap", "reggae", "reggaeton", "rock", "rumba", "salsa", "samba", "sertanejo", "soul", "synthpop", "swing", "synthwave", "techno", "trap", "uk garage"]
    genres1 = random.choice(genres)
    vibes1 = random.choice(vibes)
    return genres1 + "," + vibes1

def get_random_lyrics(prompt, token):
    prompt = prompt.replace(",", " ")
    lid = generate_lyrics(prompt.replace(",", " "), token)
    print(local_time() + f" ***generate_lyrics lyrics -> {lid} ***\n")
    if 'id' in lid:
        print(local_time() + f" ***generate_lyrics  prompt -> {prompt} lid -> {lid['id']}***\n")
        while True:
            # 每间隔一秒钟检查一次歌词生成情况
            lyrics = get_lyrics(lid['id'], token)
            print(local_time() + f" ***get_lyrics lyrics -> {lyrics} ***\n")
            if 'status' in lyrics and lyrics['status'] == "complete":
                return lyrics
            time.sleep(1)
    return {'status': '', 'title': '', 'text':''}