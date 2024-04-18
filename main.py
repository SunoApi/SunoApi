# -*- coding:utf-8 -*-

import streamlit as st
import time,json,os

from datetime import datetime

import schemas
from cookie import suno_sqlite,get_suno_auth,new_suno_auth
from utils import generate_lyrics, generate_music, get_feed, get_page_feed, get_lyrics, check_url_available,local_time

from sqlite import SqliteTool

suno_sqlite = SqliteTool()

st.set_page_config(page_title="Suno API AI Music Generator",
                   page_icon="🎵",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   menu_items={
                       'Report a bug': "https://github.com/SunoApi/SunoApi/issues",
                       'About': "Suno API AI Music Generator is a free AI music generation software, calling the existing API interface to achieve AI music generation. If you have any questions, please visit our website url address: https://sunoapi.net\n\nDisclaimer: Users voluntarily input their account information that has not been recharged to generate music. Each account can generate five songs for free every day, and we will not use them for other purposes. Please rest assured to use them! If there are 10000 users, the system can generate 50000 songs for free every day. Please try to save usage, as each account can only generate five songs for free every day. If everyone generates more than five songs per day, it is still not enough. The ultimate goal is to keep them available for free generation at any time when needed.\n\n"
                   })

hide_streamlit_style = """
<style>#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2rem;}</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

root_dir = os.path.dirname(os.path.realpath(__file__))
# print(root_dir)
i18n_dir = os.path.join(root_dir, "i18n")
# print(i18n_dir)

def load_locales():
    locales = {}
    for root, dirs, files in os.walk(i18n_dir):
        for file in files:
            if file.endswith(".json"):
                lang = file.split(".")[0]
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    locales[lang] = json.loads(f.read())
    return locales

locales = load_locales()
display_languages = []
selected_index = 0
st.session_state.Language = "ZH"

for i, code in enumerate(locales.keys()):
    display_languages.append(f"{code} - {locales[code].get('Language')}")
    if code == st.session_state.Language:
        selected_index = i
        st.session_state.Language = code

col1, col2, col3 = st.columns(3)

selected_language = col2.selectbox("Language", options=display_languages, label_visibility='collapsed',
                                 index=selected_index)
if selected_language:
    code = selected_language.split(" - ")[0].strip()
    st.session_state.Language = code
    # print("code:" + code)

def i18n(key):
    loc = locales.get(st.session_state.Language, {})
    return loc.get("Translation", {}).get(key, key)

from streamlit_option_menu import option_menu
with st.sidebar:
    selected = option_menu("Suno AI Music", [i18n("Music Song Create"), i18n("Music Share Square"), i18n("Visit Official WebSite")],icons=['music-note', 'music-note-beamed', 'music-note-list'], menu_icon="cast", default_index=0)
    
    if selected == i18n("Music Share Square"):
        st.switch_page("pages/square.py")
    elif selected == i18n("Visit Official WebSite"):
        st.page_link("https://suno.com", label=i18n("Visit Official WebSite1"), icon="🌐")
        st.page_link("https://sunoapi.net", label=i18n("Visit Official WebSite2"), icon="🌐")
    # print(selected)

st.sidebar.image('https://sunoapi.net/images/wechat.jpg', caption=i18n("Join WeChat Group"))

col2.title(i18n("Page Title"))

col2.markdown(i18n("Page Header"))

container = col2.container(border=True)

st.session_state.Custom = False
Custom = container.toggle(i18n("Custom"))
if Custom:
    st.session_state.Custom = True
    # print(st.session_state.Custom)
    Title = container.text_input(label=i18n("Title"), value='', placeholder=i18n("Title Placeholder"), max_chars=100, help=i18n("Title Desc"))
    st.session_state.Title = Title
    # print(st.session_state.Title)
    Tags = container.text_area(label=i18n("Tags"), value='', placeholder=i18n("Tags Placeholder"), height=5, max_chars=200, help=i18n("Tags Desc"))
    st.session_state.Tags = Tags
    # print(st.session_state.Tags)
    Prompt = container.text_area(label=i18n("Prompt"), value='', placeholder=i18n("Prompt Placeholder"), height=150, max_chars=1000, help=i18n("Prompt Desc"))
    st.session_state.Prompt = Prompt
    # print(st.session_state.Prompt)
else:
    st.session_state.Custom = False
    # print(st.session_state.Custom)
    DescPrompt = container.text_area(label=i18n("Desc Prompt"), value='', placeholder=i18n("Desc Value"), height=150, max_chars=500, help=i18n("Desc Reamrk"))
    st.session_state.DescPrompt = DescPrompt
    # print(st.session_state.DescPrompt)

with container.container():
    cols = container.columns(3)

    st.session_state.Instrumental = False
    instrumental = cols[0].checkbox(i18n("Instrumental"), help=i18n("Instrumental Help"))
    if instrumental:
        st.session_state.Instrumental = True
        # print(st.session_state.Instrumental)
    else:
        st.session_state.Instrumental = False
        # print(st.session_state.Instrumental)


    st.session_state.Private = False
    private = cols[1].checkbox(i18n("Private"), help=i18n("Private Help"))
    if private:
        st.session_state.Private = True
        # print(st.session_state.Private)
    else:
        st.session_state.Private = False
        # print(st.session_state.Private)


container1 = col2.container(border=True)

st.session_state.Setting = False
Setting = container1.toggle(i18n("Setting"))

identity = ""
Session = ""
Cookie = ""

if Setting:
    st.session_state.Setting = True
    # print(st.session_state.Setting)

    if "Identity" not in st.session_state:
        pass
    else:
        identity = st.session_state.Identity

    result = suno_sqlite.query_one("select id,identity,[session],cookie from session where identity =?", (identity,))
    print(result)
    print("\n")
    if result:
        identity = result[1]
        Session = result[2]
        Cookie = result[3]
        
    Identity = container1.text_input(label="Identity：", value=identity, placeholder=i18n("Identity Placeholder"), max_chars=50, help=i18n("Identity Help"))
    st.session_state.Identity = Identity
    # print(st.session_state.Identity)
    Session = container1.text_input(label="Session：", value=Session, placeholder=i18n("Session Placeholder"),max_chars=50, help=i18n("Session Help"))
    st.session_state.Session = Session
    # print(st.session_state.Session)
    Cookie = container1.text_area(label="Cookie：", value=Cookie, placeholder=i18n("Cookie Placeholder"), height=150, max_chars=1500, help=i18n("Cookie Help"))
    st.session_state.Cookie = Cookie
    # print(st.session_state.Cookie)

    st.session_state.SaveInfo = False
    SaveInfo = container1.button(i18n("SaveInfo"))
    if SaveInfo:
        st.session_state.SaveInfo = True
        if Identity == "":
            col2.error(i18n("SaveInfo Identity Error"))
        elif Session == "":
            col2.error(i18n("SaveInfo Session Error"))
        elif Cookie == "":
            col2.error(i18n("SaveInfo Cookie Error"))
        else:
            result = suno_sqlite.query_one("select id,identity,[session],cookie from session where identity =?", (Identity,))
            print(result)
            print("\n")
            if result:
                result = suno_sqlite.operate_one("update session set identity=?, session=?, cookie=? where identity =?", (Identity, Session, Cookie, Identity))
            else:
                result = suno_sqlite.operate_one("insert into session (identity,session,cookie) values(?,?,?)", (Identity, Session, Cookie))

            if result:
                st.session_state.Identity = Identity
                new_suno_auth(Identity, Session, Cookie)
                # print(st.session_state.Identity)
                col2.success(i18n("SaveInfo Success"))
            else:
                col2.error(i18n("SaveInfo Error"))
            print(result)
            print("\n")
            # print(st.session_state.SaveInfo)
    else:
        st.session_state.SaveInfo = False
        # print(st.session_state.SaveInfo)

st.session_state.token = ""
st.session_state.suno_auth = None
while True:
    st.session_state.suno_auth = get_suno_auth()
    st.session_state.token = st.session_state.suno_auth.get_token()
    if st.session_state.token != "":
        print(local_time() + f" ***generate identity -> {st.session_state.suno_auth.get_identity()} session -> {st.session_state.suno_auth.get_session_id()} token -> {st.session_state.suno_auth.get_token()} ***\n")
        break
    else:
        col2.error(i18n("TokenAuth Error"))
        break

# @st.cache_data
def fetch_feed(aids: list):
    if len(aids) == 1 and len(aids[0].strip()) == 36:
        resp = get_feed(aids[0].strip(), st.session_state.token)
        print(resp)
        print("\n")
        status = resp["detail"] if "detail" in resp else resp[0]["status"]
        if status != "Unauthorized" and status != "Not found." and status != "error":
            result = suno_sqlite.query_one("select aid from music where aid =?", (aids[0].strip(),))
            print(result)
            print("\n")
            if result:
                result = suno_sqlite.operate_one("update music set data=?, updated=(datetime('now', 'localtime')), sid=?, name=?, image=?, title=?, tags=?, prompt=?, duration=?, status=? where aid =?", (str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], resp[0]["status"], aids[0].strip()))
            else:
                result = suno_sqlite.operate_one("insert into music (aid, data, sid, name, image, title, tags, prompt,duration, status, private) values(?,?,?,?,?,?,?,?,?,?,?)", (str(resp[0]["id"]), str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], resp[0]["status"], st.session_state.Private))
            print(result)
            print("\n")
            if status == "complete":
                st.balloons()
                col1.audio(resp[0]["audio_url"])
                col1.video(resp[0]["video_url"])
                # col1.image(resp[0]["image_large_url"])
                col2.success(i18n("FetchFeed Success") + resp[0]["id"])
            else:
                col2.error(i18n("FetchFeed Error") + (status if "metadata" not in resp else resp[0]['metadata']["error_message"]))
        else:
            col2.error(i18n("FetchFeed Error") + (status if "metadata" not in resp else resp[0]['metadata']["error_message"]))
    elif len(aids) == 2  and len(aids[0].strip()) == 36 and len(aids[1].strip()) == 36:
        resp = get_feed(aids[0].strip(), st.session_state.token)
        print(resp)
        print("\n")
        status = resp["detail"] if "detail" in resp else resp[0]["status"]
        if status != "Unauthorized" and status != "Not found." and status != "error":
            result = suno_sqlite.query_one("select aid from music where aid =?", (aids[0].strip(),))
            print(result)
            print("\n")
            if result:
                result = suno_sqlite.operate_one("update music set data=?, updated=(datetime('now', 'localtime')), sid=?, name=?, image=?, title=?, tags=?, prompt=?, duration=?, status=? where aid =?", (str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], resp[0]["status"], aids[0].strip()))
            else:
                result = suno_sqlite.operate_one("insert into music (aid, data, sid, name, image, title, tags, prompt,duration, status, private) values(?,?,?,?,?,?,?,?,?,?,?)", (str(resp[0]["id"]), str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], resp[0]["status"], st.session_state.Private))
            print(result)
            print("\n")
            if status == "complete":
                col1.audio(resp[0]["audio_url"])
                col1.video(resp[0]["video_url"])
                # col1.image(resp[0]["image_large_url"])
                col2.success(i18n("FetchFeed Success") + resp[0]["id"])
            else:
                col2.error(i18n("FetchFeed Error") + (status if "metadata" not in resp else resp[0]['metadata']["error_message"]))
        else:
            col2.error(i18n("FetchFeed Error") + (status if "metadata" not in resp else resp[0]['metadata']["error_message"]))

        resp = get_feed(aids[1].strip(), st.session_state.token)
        print(resp)
        print("\n")
        status = resp["detail"] if "detail" in resp else resp[0]["status"]
        if status != "Unauthorized" and status != "Not found." and status != "error":
            result = suno_sqlite.query_one("select aid from music where aid =?", (aids[1].strip(),))
            print(result)
            print("\n")
            if result:
                result = suno_sqlite.operate_one("update music set data=?, updated=(datetime('now', 'localtime')), sid=?, name=?, image=?, title=?, tags=?, prompt=?, duration=?, status=? where aid =?", (str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], resp[0]["status"], aids[1].strip()))
            else:
                result = suno_sqlite.operate_one("insert into music (aid, data, sid, name, image, title, tags, prompt,duration, status, private) values(?,?,?,?,?,?,?,?,?,?,?)", (str(resp[0]["id"]), str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], resp[0]["status"], st.session_state.Private))
            print(result)
            print("\n")
            if status == "complete":
                st.balloons()
                col3.audio(resp[0]["audio_url"])
                col3.video(resp[0]["video_url"])
                # col3.image(resp[0]["image_large_url"])
                col2.success(i18n("FetchFeed Success") + resp[0]["id"])
            else:
                col2.error(i18n("FetchFeed Error") + (status if "metadata" not in resp else resp[0]['metadata']["error_message"]))
        else:
            col2.error(i18n("FetchFeed Error") + (status if "metadata" not in resp else resp[0]['metadata']["error_message"]))
    else:
        # col2.error(i18n("FetchFeed Error") + i18n("FetchFeed FeedID Error"))
        resp = get_page_feed(aids, st.session_state.token)
        print(resp)
        print("\n")
        for row in resp:
            print(row)
            print("\n")
            result = suno_sqlite.query_one("select aid from music where aid =?", (row["id"],))
            print(result)
            print("\n")
            if result:
                result = suno_sqlite.operate_one("update music set data=?, updated=(datetime('now', 'localtime')), sid=?, name=?, image=?, title=?, tags=?, prompt=?, duration=?, status=? where aid =?", (str(row), row["user_id"], row["display_name"], row["image_url"], row["title"], row["metadata"]["tags"], row["metadata"]["gpt_description_prompt"], row["metadata"]["duration"], row["status"], row["id"]))
                print(local_time() + f" ***get_page_feed_update page -> {aids} ***\n")
            else:
                result = suno_sqlite.operate_one("insert into music (aid, data, sid, name, image, title, tags, prompt,duration, status, private) values(?,?,?,?,?,?,?,?,?,?,?)", (str(row["id"]), str(row), row["user_id"], row["display_name"], row["image_url"], row["title"], row["metadata"]["tags"], row["metadata"]["gpt_description_prompt"], row["metadata"]["duration"], row["status"], st.session_state.Private))
                print(local_time() + f" ***get_page_feed_insert page -> {aids} ***\n")
            print(result)
            print("\n")
            status = resp["detail"] if "detail" in resp else row["status"]
            if status == "complete":
                # st.balloons()
                # col1.audio(row["audio_url"])
                # col1.video(row["video_url"])
                # col1.image(row["image_large_url"])
                col2.success(i18n("FetchFeed Success") + row["id"])
            else:
                col2.error(i18n("FetchFeed Error") + (status if "metadata" not in resp else row['metadata']["error_message"]))


container2 = col2.container(border=True)

st.session_state.FetchFeed = False
FetchFeed = container2.toggle(i18n("FetchFeed"))

if FetchFeed:
    st.session_state.FetchFeed = True
    # print(st.session_state.FetchFeed)
        
    FeedID = container2.text_input(label=i18n("FeedID"), value="", placeholder=i18n("FeedID Placeholder"), max_chars=100, help=i18n("FeedID Help"))
    st.session_state.FeedID = FeedID
    # print(st.session_state.FeedID)
    
    st.session_state.FeedBtn = False
    FeedBtn = container2.button(i18n("FeedBtn"))
    if FeedBtn:
        # st.session_state.FeedBtn = True
        # if FeedID == "":
        #     col2.error(i18n("FetchFeed FeedID Empty"))
        # else:
        #    FeedIDs = FeedID.split(",")
        FeedIDs = FeedID*1
        fetch_feed(FeedIDs)
    else:
        st.session_state.FeedBtn = False
        # print(st.session_state.FeedBtn)


disabled_state = False
StartBtn = col2.button(i18n("Generate"), use_container_width=True, type="primary", disabled=disabled_state)

def generate(data: schemas.CustomModeGenerateParam):
    try:
        resp = generate_music(data, st.session_state.token)
        return resp
    except Exception as e:
        return {"detail":str(e)}

def generate_with_song_description(data: schemas.DescriptionModeGenerateParam):
    try:
        resp = generate_music(data, st.session_state.token)
        return resp
    except Exception as e:
        return {"detail":str(e)}



def fetch_status(aid: str):
    progress_text = i18n("Fetch Status Progress")
    my_bar = col2.progress(0, text=progress_text)
    percent_complete = 0
    my_bar.progress(percent_complete, text=progress_text)
    while True:
        resp = get_feed(aid, st.session_state.token)
        print(resp)
        print("\n")
        percent_complete = percent_complete + 1 if percent_complete >= 90 else percent_complete + 5
        if percent_complete >= 100:
            percent_complete = 100
        status = resp["detail"] if "detail" in resp else resp[0]["status"]
        if status == "running":
            progress_text = i18n("Fetch Status Running") + status
            my_bar.progress(percent_complete, text=progress_text)
        elif status == "submitted":
            progress_text = i18n("Fetch Status Running") + status
            my_bar.progress(percent_complete, text=progress_text)
        elif status == "complete":
            progress_text = i18n("Fetch Status Success") + status
            my_bar.progress(100, text=progress_text)
            # time.sleep(15) #等待图片音频视频生成完成再返回
            check_url_available(resp[0]["video_url"])
            my_bar.empty()
        elif status == "Unauthorized":
            while True:
                st.session_state.suno_auth = get_suno_auth()
                st.session_state.token = st.session_state.suno_auth.get_token()
                if st.session_state.token != "":
                    print(local_time() + f" ***fetch_status identity -> {st.session_state.suno_auth.get_identity()} session -> {st.session_state.suno_auth.get_session_id()} token -> {st.session_state.suno_auth.get_token()} ***\n")
                    break
            continue
        elif status == "Not found.":
            continue
        elif status == "error":
            my_bar.empty()
        else:
            progress_text = i18n("Fetch Status Running") + status
            my_bar.progress(percent_complete, text=progress_text)
        
        result = suno_sqlite.query_one("select aid from music where aid =?", (aid,))
        print(result)
        print("\n")
        if result:
            result = suno_sqlite.operate_one("update music set data=?, updated=(datetime('now', 'localtime')), sid=?, name=?, image=?, title=?, tags=?, prompt=?, duration=?, status=? where aid =?", (str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], status, aid))
            print(local_time() + f" ***fetch_status_update aid -> {aid} status -> {status} data -> {str(resp[0])} ***\n")
        else:
            result = suno_sqlite.operate_one("insert into music (aid, data, sid, name, image, title, tags, prompt,duration, status, private) values(?,?,?,?,?,?,?,?,?,?,?)", (str(resp[0]["id"]), str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], status, st.session_state.Private))
        print(result)
        print("\n")

        if status == "complete" or status == "error":
            break

        time.sleep(10)
    
    return resp

if StartBtn:
    if st.session_state.Custom:
        if st.session_state.Title == "":
            col2.error(i18n("Custom Title Error"))
        elif st.session_state.Tags == "":
            col2.error(i18n("Custom Tags Error"))
        elif st.session_state.Prompt == "":
            col2.error(i18n("Custom Prompt Error"))
        else:
            data = {}
            if st.session_state.Instrumental:
                data = {
                    "title": st.session_state.Title,
                    "tags": st.session_state.Tags,
                    "prompt": "",
                    "mv": "chirp-v3-0",
                    "continue_at": None,
                    "continue_clip_id": None
                }
            else:
                data = {
                    "title": st.session_state.Title,
                    "tags": st.session_state.Tags,
                    "prompt": st.session_state.Prompt,
                    "mv": "chirp-v3-0",
                    "continue_at": None,
                    "continue_clip_id": None
                }
            print(data)
            print("\n")
            resp = generate(data)
            print(resp)
            print("\n")
            status = resp["status"] if "status" in resp else resp["detail"]
            if status == "running":
                disabled_state = True
                result = suno_sqlite.operate_one("insert into music (aid, data, private) values(?,?,?)", (str(resp["clips"][0]["id"]), str(resp["clips"][0]), st.session_state.Private))
                resp0 = fetch_status(resp["clips"][0]["id"])
                if resp0[0]["status"] == "complete":
                    col1.audio(resp0[0]["audio_url"])
                    col1.video(resp0[0]["video_url"])
                    # col1.image(resp0[0]["image_large_url"])
                    col2.success(i18n("Generate Success") + resp0[0]["id"])
                else:
                    col2.error(i18n("Generate Status Error")  + (resp0[0]['status'] if resp0[0]['metadata']["error_message"] is None else resp0[0]['metadata']["error_message"]))
                
                result = suno_sqlite.operate_one("insert into music (aid, data, private) values(?,?,?)", (str(resp["clips"][1]["id"]), str(resp["clips"][1]), st.session_state.Private))
                resp1 = fetch_status(resp["clips"][1]["id"])
                if resp1[0]["status"] == "complete":
                    st.balloons()
                    col3.audio(resp1[0]["audio_url"])
                    col3.video(resp1[0]["video_url"])
                    # col3.image(resp1[0]["image_large_url"])
                    col2.success(i18n("Generate Success") + resp1[0]["id"])
                else:
                    col2.error(i18n("Generate Status Error")  + (resp1[0]['status'] if resp1[0]['metadata']["error_message"] is None else resp1[0]['metadata']["error_message"]))
                disabled_state = False
            else:
                col2.error(i18n("Generate Submit Error") + status)
    else:
        if st.session_state.DescPrompt == "":
            col2.error(i18n("DescPrompt Error"))
        else:
            data = {
                "gpt_description_prompt": st.session_state.DescPrompt,
                "make_instrumental": st.session_state.Instrumental,
                "mv": "chirp-v3-0",
                "prompt": ""
            }
            print(data)
            print("\n")
            resp = generate_with_song_description(data)
            print(resp)
            print("\n")
            status = resp["status"] if "status" in resp else resp["detail"]
            if status == "running":
                disabled_state = True
                result = suno_sqlite.operate_one("insert into music (aid, data, private) values(?,?,?)", (str(resp["clips"][0]["id"]), str(resp["clips"][0]), st.session_state.Private))
                resp0 = fetch_status(resp["clips"][0]["id"])
                if resp0[0]["status"] == "complete":
                    col1.audio(resp0[0]["audio_url"])
                    col1.video(resp0[0]["video_url"])
                    # col1.image(resp0[0]["image_large_url"])
                    col2.success(i18n("Generate Success") + resp0[0]["id"])
                else:
                    col2.error(i18n("Generate Status Error") + (resp0[0]['status'] if resp0[0]['metadata']["error_message"] is None else resp0[0]['metadata']["error_message"]))

                result = suno_sqlite.operate_one("insert into music (aid, data, private) values(?,?,?)", (str(resp["clips"][1]["id"]), str(resp["clips"][1]), st.session_state.Private))
                resp1 = fetch_status(resp["clips"][1]["id"])
                if resp1[0]["status"] == "complete":
                    st.balloons()
                    col3.audio(resp1[0]["audio_url"])
                    col3.video(resp1[0]["video_url"])
                    # col3.image(resp1[0]["image_large_url"])
                    col2.success(i18n("Generate Success") + resp1[0]["id"])
                else:
                    col2.error(i18n("Generate Status Error") + (resp1[0]['status'] if resp1[0]['metadata']["error_message"] is None else resp1[0]['metadata']["error_message"]))
                disabled_state = False
            else:
                col2.error(i18n("Generate Submit Error") + status)

    