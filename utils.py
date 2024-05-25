# -*- coding:utf-8 -*-

import json
import os
import time
import boto3
import requests,random,re

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
        if S3_WEB_SITE_URL is None or S3_WEB_SITE_URL == "https://cdn1.suno.ai":
            result = resp.text
        elif S3_WEB_SITE_URL is not None and S3_WEB_SITE_URL != "http://localhost:8501":
            result = resp.text.replace('https://cdn1.suno.ai/', f'{S3_WEB_SITE_URL}/files/')
        else:
            result = resp.text.replace('https://cdn1.suno.ai/', 'https://res.sunoapi.net/files/')
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

def generate_concat(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/concat/v2/"
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
    if S3_WEB_SITE_URL is None or S3_WEB_SITE_URL == "https://cdn1.suno.ai":
        pass
    elif S3_WEB_SITE_URL is not None and S3_WEB_SITE_URL != "http://localhost:8501":
        url = url.replace(f'{S3_WEB_SITE_URL}/files/', 'https://cdn1.suno.ai/')
    else:
        url = url.replace(f'https://res.sunoapi.net/files/', 'https://cdn1.suno.ai/')
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
    genres = ["• Bluegrass（草莓乐）","• Country（乡村音乐）","• Folk（民谣）","• Afro-Cuban（阿弗罗-古巴）","• Dance Pop（流行舞曲）","• Disco（迪斯科）","• Dubstep（配音步）","• Disco Funk（迪斯科放克）","• EDM（电子舞曲）","• Electro（电子）","• High-NRG（高能量）","• House（浩室音乐）","• Trance（迷幻舞曲）","• Ambient（环境音）","• Drum'n'bass（鼓与贝斯）","• Dubstep（配音步）","• Electronic（电子音乐）","• IDM（智能舞曲）","• Synthpop（合成流行）","• Synthwave（合成波）","• Techno（技术音乐）","• Trap（陷阱音乐）","• Bebop（比博普）","• Gospel（福音）","• Jazz（爵士）","• Latin Jazz（拉丁爵士）","• RnB（节奏蓝调）","• Soul（灵魂乐）","• Bossa Nova（波萨诺瓦）","• Latin Jazz（拉丁爵士）","• Forró（弗约罗）","• Salsa（萨尔萨舞）","• Tango（探戈）","• Dancehall（舞厅）","• Dub（配音）","• Reggae（雷鬼）","• Reggaeton（雷盖顿）","• Afrobeat（非洲节奏）","• Black Metal（黑金属）","• Deathcore（死亡核）","• Death Metal（死亡金属）","• Festive Heavy Metal（节日重金属）","• Heavy Metal（重金属）","• Nu Metal（新金属）","• Power Metal（力量金属）","• Metalcore（金属核）","• Pop（流行音乐）","• Chinese pop（中国流行音乐）","• Dance Pop（流行舞曲）","• Pop Rock（流行摇滚）","• Kpop（韩流音乐）","• Jpop（日流音乐）","• RnB（节奏蓝调）","• Synthpop（合成流行）","• Classic Rock（经典摇滚）","• Blues Rock（布鲁斯摇滚）","• Emo（情绪）","• Glam Rock（华丽摇滚）","• Indie（独立音乐）","• Industrial Rock（工业摇滚）","• Punk（朋克摇滚）","• Rock（摇滚）","• Skate Rock（滑板摇滚）","• Skatecore（滑板核）","• Funk（放克）","• HipHop（嘻哈）","• RnB（节奏蓝调）","• Phonk（酸音乐）","• Rap（说唱）","• Trap（陷阱音乐）"]
    vibes = ["• Disco（迪斯科）","• Syncopated（切分节奏）","• Groovy（悠扬）","• Tipsy（微醺）","• Dark（黑暗）","• Doom（末日）","• Dramatic（戏剧性）","• Sinister（阴险）","• Art（艺术）","• Nu（新流行）","• Progressive（进步）","• Aggressive（激进）","• Banger（热门曲目）","• Power（力量）","• Stadium（体育场）","• Stomp（重踏）","• Broadway（百老汇）","• Cabaret（歌舞表演）","• Lounge（酒吧歌手）","• Operatic（歌剧式的）","• Storytelling（讲故事）","• Torch-Lounge（酒吧歌曲）","• Theatrical（戏剧性的）","• Troubadour（吟游诗人）","• Vegas（拉斯维加斯风格）","• Ethereal（虚幻）","• Majestic（雄伟）","• Mysterious（神秘）","• Ambient（环境音乐）","• Cinematic（电影）","• Slow（缓慢）","• Sparse（稀疏）","• Glam（华丽）","• Glitter（闪耀）","• Groovy（悠扬）","• Grooveout（活力爆发）","• Ambient（环境音乐）","• Bedroom（卧室）","• Chillwave（轻松浪潮）","• Ethereal（虚幻）","• Intimate（亲密）","• Carnival（嘉年华）","• Haunted（鬼屋）","• Random（随机）","• Musicbox（音乐盒）","• Hollow（空洞）","• Arabian（阿拉伯）","• Bangra（班格拉舞）","• Calypso（卡利普索）","• Egyptian（埃及）","• Adhan（安讫）","• Jewish Music（犹太音乐）","• Klezmer（克莱兹默音乐）","• Middle East（中东）","• Polka（波尔卡）","• Russian Navy Song（俄罗斯海军歌曲）","• Suomipop（芬兰流行音乐）","• Tribal（部落）"]
    types = ["• Elevator（电梯音乐）","• Jingle（广告歌曲）","• Muzak（环境音乐）","• Call to Prayer（祈祷呼唤）","• Gregorian Chant（格里高利圣歌）","• Strut（趾高气昂地走）","• March（进行曲）","• I Want Song（渴望之歌）","• Children's（儿童的）","• Lullaby（摇篮曲）","• Sing-along（合唱歌曲）","• 1960s（1960年代）","• Barbershop（理发店四重唱）","• Big Band（大乐队）","• Classic（经典的）","• Doo Wop（一种节奏蓝调风格的音乐）","• Girl Group（女子组合）","• Swing（摇摆乐）","• Traditional（传统的）","• Barbershop（理发店四重唱）","• Christmas Carol（圣诞颂歌）","• Traditional（传统的）"]
    genres1 = random.choice(genres)
    vibes1 = random.choice(vibes)
    # types1 = random.choice(types)
    return genres1 + "," + vibes1

def remove_chinese(tags):
    # print(tags)
    result = None
    if '• ' in tags:
        result = re.search(r"• (.*?)（", tags)
    else:
        result = re.search(r"  (.*?)（", tags)
    try:
        result = result.group(1).lower()
    except:
        result = ""
    # print(result)
    return result

def get_new_tags(tags):
    # print(tags)
    tags_array = tags.split(",")
    new_tags = " ".join([f"{remove_chinese(i)}" for i in tags_array])
    # print(new_tags)
    return new_tags

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