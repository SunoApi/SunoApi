# -*- coding:utf-8 -*-

import json
import os
import time
import boto3
import requests,random

from dotenv import load_dotenv
load_dotenv()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
S3_WEB_SITE_URL = os.getenv("S3_WEB_SITE_URL")
S3_ACCESSKEY_ID = os.getenv("S3_ACCESSKEY_ID")
S3_SECRETKEY_ID = os.getenv("S3_SECRETKEY_ID")

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
        result = resp.text.replace('https://cdn1.suno.ai/', f'{S3_WEB_SITE_URL}/files/')
        result = result.replace('.png', '.png?fmt=webp&txt=SunoAPI&txt-size=0.35&txt-pos=0.5,*0.96&txt-alpha=0.30')
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

def check_url_available(url, twice=False):
    url = url.replace(f'{S3_WEB_SITE_URL}/files/', 'https://cdn1.suno.ai/')
    i = 0
    while not twice and i < 10:
        # 每间隔一秒钟检查一次url文件大小
        file_size = get_file_size(url)
        if file_size >= 1024*1024:
            print(local_time() + f" ***check_url_available -> {url} 文件大小：{file_size} 大于1MB可访问到***\n")
            break
        i += 1
        print(local_time() + f" ***check_url_available -> {url} 文件大小：{file_size} 小于1MB继续检查***\n")
        time.sleep(2)
    time.sleep(3)

def get_file_size(url):
    try:
        requests.packages.urllib3.disable_warnings()
        resp = requests.head(url, verify=False)
        if resp.status_code == 200:
            file_size = resp.headers.get('Content-Length')
            if file_size:
                return int(file_size)
            # else:
            #     return 0
            print(local_time() + f" ***check_url_available -> {url} file_size -> {file_size} ***\n")
        else:
            print(local_time() + f" ***check_url_available -> {url} status_code -> {resp.status_code} ***\n")
            return 0
    except Exception as e:
        print(local_time() + f" ***check_url_available -> {url} exception -> {str(e)} ***\n")
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
            elif 'status' in lyrics and lyrics['status'] == "running":
                continue
            else:
                return lyrics
            time.sleep(1)
    return {'status': '', 'title': '', 'text':''}

def get_upload_url(filename, s3accessKeyId, s3SecretKeyId):
    # Config
    s3endpoint = 'https://s3.bitiful.net' # 请填入控制台 “Bucket 设置” 页面底部的 “Endpoint” 标签中的信息
    s3region = 'cn-east-1'
    s3accessKeyId = s3accessKeyId # 请到控制台创建子账户，并为子账户创建相应 accessKey
    s3SecretKeyId = s3SecretKeyId # ！！切记，创建子账户时，需要手动为其分配具体权限！！

    # 连接 S3
    client = boto3.client(
        's3',
        aws_access_key_id = s3accessKeyId,
        aws_secret_access_key = s3SecretKeyId,
        endpoint_url = s3endpoint,
        region_name = s3region
    )
    url = client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': 'sunoapi',
            'Key': "images/upload/" + filename,
        },
        ExpiresIn=3600
    )
    return url

def put_upload_file(siteurl, filename, s3accessKeyId, s3SecretKeyId, data):
    upload_url = ""
    try:
        upload_url = get_upload_url(filename, s3accessKeyId, s3SecretKeyId)
        headers = {"Content-Type": "image/jpeg"}
        requests.packages.urllib3.disable_warnings()
        resp = requests.put(url=upload_url, headers=headers, data=data, verify=False)
        if resp.status_code == 200:
            return f"{siteurl}/images/upload/{filename}"
        else:
            return {"detail":str(resp.status_code)}
    except Exception as e:
        print(local_time() + f" ***put_upload_file -> {upload_url} exception -> {str(e)} ***\n")
        return {"detail":str(e)}