# -*- coding:utf-8 -*-

import os
import time
from http.cookies import SimpleCookie
from threading import Thread

import requests,random
from urllib import request

from sqlite import SqliteTool

from utils import COMMON_HEADERS,local_time

suno_sqlite = SqliteTool()

class SunoCookie:
    def __init__(self):
        self.cookie = SimpleCookie()
        self.identity = ""
        self.session_id = ""
        self.token = ""

    def load_cookie(self, cookie_str):
        self.cookie.load(cookie_str)

    def get_cookie(self):
        return ";".join([f"{i}={self.cookie.get(i).value}" for i in self.cookie.keys()])

    def set_identity(self, identity):
        self.identity = identity

    def get_identity(self):
        return self.identity

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_session_id(self):
        return self.session_id

    def get_token(self):
        return self.token

    def set_token(self, token: str):
        self.token = token


def update_token(suno_cookie: SunoCookie):
    headers = {"Cookie": suno_cookie.get_cookie()}
    headers.update(COMMON_HEADERS)
    session_id = suno_cookie.get_session_id()
    identity = suno_cookie.get_identity()

    resp = requests.post(
        # url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.70.5",
        # url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.71.4",
        url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.72.0-snapshot.vc141245",
        headers=headers,
    )

    #if resp.status_code != 200:
    print(local_time() + f" ***update_token identity -> {identity} session -> {session_id} status_code -> {resp.status_code} ***\n")
    
    resp_headers = dict(resp.headers)
    set_cookie = resp_headers.get("Set-Cookie") if resp_headers.get("Set-Cookie") else suno_cookie.get_cookie()
    # print(f"*** set_cookie -> {set_cookie} ***")
    suno_cookie.load_cookie(set_cookie)
    token = resp.json().get("jwt") if resp.json().get("jwt") else ""
    suno_cookie.set_token(token)
    # print(f"*** token -> {token} ***")

    # result = suno_sqlite.operate_one("update session set session=?, cookie=?, status=? where identity =?", (session_id, set_cookie, resp.status_code, identity))
    # print(result)


def keep_alive(suno_cookie: SunoCookie):
    while True:
        update_token(suno_cookie)
        time.sleep(50)

suno_auths = []
def get_suno_auth():
    return random.choice(suno_auths)

def new_suno_auth(identity, session, cookie):
    suno_cookie = SunoCookie()
    suno_cookie.set_identity(identity)
    suno_cookie.set_session_id(session)
    suno_cookie.load_cookie(cookie)
    suno_auths.append(suno_cookie)
    t = Thread(target=keep_alive, args=(suno_cookie,))
    t.start()
    print(local_time() + f" ***new_suno_auth identity -> {identity} session -> {session} token -> {cookie} ***\n")

def start_keep_alive():
    print("start_keep_alive")
    result = suno_sqlite.query_many("select id,identity,[session],cookie from session")
    print(result)
    print("\n")
    if result:
        for row in result:
            suno_cookie = SunoCookie()
            suno_cookie.set_identity(row[1])
            suno_cookie.set_session_id(row[2])
            suno_cookie.load_cookie(row[3])
            suno_auths.append(suno_cookie)
            t = Thread(target=keep_alive, args=(suno_cookie,))
            t.start()

        # print(len(suno_auths))

start_keep_alive()
