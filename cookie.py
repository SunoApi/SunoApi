# -*- coding:utf-8 -*-

import os,json,urllib
import time,threading
from http.cookies import SimpleCookie
from threading import Thread

import requests,random

from utils import COMMON_HEADERS,local_time,get_page_feed

from sqlite import SqliteTool

suno_sqlite = SqliteTool()

class SunoCookie:
    def __init__(self):
        self.cookie = SimpleCookie()
        self.identity = ""
        self.session_id = ""
        self.token = ""

    def load_cookie(self, cookie_str):
        self.cookie.load(cookie_str)

    def set_cookie(self, cookie_str):
        for cookie in cookie_str.split('; '):
            key, value = cookie.split('=', 1)
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass  # 如果不是有效的JSON，则保持原始字符串

            if key == "__client":
                # print("__client: " + value)
                value = urllib.parse.quote(value)
                # print("__client: " + value)

            self.cookie[key] = value

    def get_cookie(self):
        # print(local_time() + f" ***get_cookie output -> {self.cookie.output()} thread_id: {threading.get_ident()} ***\n")
        return  ";".join([f"{i}={self.cookie.get(i).value}" for i in self.cookie.keys()])

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

    if suno_cookie.get_token() == "401":
        return

    # print(local_time() + f" ***update_token identity -> {identity} session -> {session_id} headers -> {headers} thread_id: {threading.get_ident()} ***\n")

    requests.packages.urllib3.disable_warnings()
    resp = requests.post(
        # url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.70.5",
        # url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.71.4",
        url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.72.0-snapshot.vc141245",
        headers=headers,
        verify=False
    )

    if resp.status_code != 200:
        print(local_time() + f" ***update_token identity -> {identity} session -> {session_id} status_code -> {resp.status_code} thread_id: {threading.get_ident()} ***\n")
        suno_cookie.set_token("401")
    else:
        resp_headers = dict(resp.headers)
        set_cookie = resp_headers.get("Set-Cookie") if resp_headers.get("Set-Cookie") else suno_cookie.get_cookie()
        print(local_time() + f" ***update_session identity -> {identity} session -> {session_id}  set_cookie -> {set_cookie} ***")
        suno_cookie.load_cookie(set_cookie)
        token = resp.json().get("jwt") if resp.json().get("jwt") else ""
        suno_cookie.set_token(token)
        # print(f"*** token -> {token} ***")    

    result = suno_sqlite.operate_one("update session set updated=(datetime('now', 'localtime')), status=? where identity =?", (resp.status_code, identity))
    if result:
        print(local_time() + f" ***update_session identity -> {identity} session -> {session_id} status_code -> {resp.status_code} thread_id: {threading.get_ident()} ***\n")


def page_feed(suno_cookie: SunoCookie):
    token = suno_cookie.get_token()
    identity = suno_cookie.get_identity()
    session_id = suno_cookie.get_session_id()

    if token != "":
        resp = get_page_feed(0, token)
        # print(resp)
        # print("\n")
        for row in resp:
            # print(row)
            # print("\n")
            if 'id' in row:
                result = suno_sqlite.query_one("select aid from music where aid =?", (row["id"],))
                print(result)
                print("\n")
                if result:
                    result = suno_sqlite.operate_one("update music set data=?, updated=(datetime('now', 'localtime')), sid=?, name=?, image=?, title=?, tags=?, prompt=?, duration=?, status=? where aid =?", (str(row), row["user_id"], row["display_name"], row["image_url"], row["title"], row["metadata"]["tags"], row["metadata"]["gpt_description_prompt"], row["metadata"]["duration"], row["status"], row["id"]))
                else:
                    result = suno_sqlite.operate_one("insert into music (aid, data, sid, name, image, title, tags, prompt,duration, status, private) values(?,?,?,?,?,?,?,?,?,?,?)", (str(row["id"]), str(row), row["user_id"], row["display_name"], row["image_url"], row["title"], row["metadata"]["tags"], row["metadata"]["gpt_description_prompt"], row["metadata"]["duration"], row["status"], 0))
                print(result)
                print("\n")
                status = resp["detail"] if "detail" in resp else row["status"]
                if status == "complete":
                    print(local_time() + f" ***get_page_feed identity -> {identity} session -> {session_id} thread_id: {threading.get_ident()} row -> {row} ***\n")
                else:
                    status = status if "metadata" not in resp else row['metadata']["error_message"]
                    print(local_time() + f" ***get_page_feed identity -> {identity} session -> {session_id} status -> {status} thread_id: {threading.get_ident()} ***\n")


def keep_alive(suno_cookie: SunoCookie):
    while True:
        update_token(suno_cookie)
        time.sleep(50)

def get_page(suno_cookie: SunoCookie):
    while True:
        page_feed(suno_cookie)
        time.sleep(1800)

def clear_task():
    while True:
        result = suno_sqlite.delete_record("delete from music where status <> 'complete' and status <> 'streaming'")
        if result:
            print(local_time() + f" ***clear_task result -> {result} ***\n")
        time.sleep(3600)

suno_auths = []
def get_suno_auth():
    if len(suno_auths) > 0:
        suno_auth = random.choice(suno_auths)
        if suno_auth.get_token() == "401":
            suno_cookie = SunoCookie()
            return suno_cookie
        else:
            return suno_auth
    else:
        suno_cookie = SunoCookie()
        return suno_cookie


def new_suno_auth(identity, session, cookie):
    suno_cookie = SunoCookie()
    suno_cookie.set_identity(identity)
    suno_cookie.set_session_id(session)
    suno_cookie.set_cookie(cookie)
    suno_auths.append(suno_cookie)
    t = Thread(target=keep_alive, args=(suno_cookie,))
    t.start()

    t1 = Thread(target=get_page, args=(suno_cookie,))
    t1.start()
    print(local_time() + f" ***new_suno_auth identity -> {identity} session -> {session} set_cookie -> {cookie} ***\n")

def start_keep_alive():
    result = suno_sqlite.query_many("select id,identity,[session],cookie from session where status='200'")
    print(result)
    print("\n")
    if result:
        for row in result:
            suno_cookie = SunoCookie()
            suno_cookie.set_identity(row[1])
            suno_cookie.set_session_id(row[2])
            suno_cookie.set_cookie(row[3])
            suno_auths.append(suno_cookie)
            print(local_time() + f" ***start_keep_alive suno_cookie set_identity -> {row[1]} set_session_id -> {row[2]} set_cookie -> {row[3]} ***\n")
            t = Thread(target=keep_alive, args=(suno_cookie,))
            t.start()

            t1 = Thread(target=get_page, args=(suno_cookie,))
            t1.start()

        print(local_time() + f" ***start_keep_alive suno_auths -> {len(suno_auths)} ***\n")

    t2 = Thread(target=clear_task, args=())
    t2.start()

start_keep_alive()
