
# -*- coding:utf-8 -*-

import streamlit as st
import time,json,os,ast
from datetime import timezone
import dateutil.parser
from utils import generate_concat,get_feed,local_time,check_url_available
from cookie import get_random_token

from streamlit_option_menu import option_menu
from streamlit_modal import Modal
import streamlit.components.v1 as components
import streamlit_antd_components as sac

root_dir = os.path.dirname(os.path.realpath(__file__))
# print(root_dir)
import sys
sys.path.append(root_dir)
import site
site.addsitedir(root_dir)
from streamlit_image_select import image_select

from dotenv import load_dotenv
load_dotenv()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
S3_WEB_SITE_URL = os.getenv("S3_WEB_SITE_URL")
S3_ACCESSKEY_ID = os.getenv("S3_ACCESSKEY_ID")
S3_SECRETKEY_ID = os.getenv("S3_SECRETKEY_ID")

from sqlite import SqliteTool

suno_sqlite = SqliteTool()

st.set_page_config(page_title="SunoAPI AI Music Generator",
                   page_icon="🎵",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   menu_items={
                       'Report a bug': "https://github.com/SunoApi/SunoApi/issues",
                       'About': "SunoAPI AI Music Generator is a free AI music generation software, calling the existing API interface to achieve AI music generation. If you have any questions, please visit our website url address: https://sunoapi.net\n\nDisclaimer: Users voluntarily input their account information that has not been recharged to generate music. Each account can generate five songs for free every day, and we will not use them for other purposes. Please rest assured to use them! If there are 10000 users, the system can generate 50000 songs for free every day. Please try to save usage, as each account can only generate five songs for free every day. If everyone generates more than five songs per day, it is still not enough. The ultimate goal is to keep them available for free generation at any time when needed.\n\n"
                   })

hide_streamlit_style = """
<style>#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 5rem;}</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

i18n_dir = os.path.join(root_dir, "../i18n")
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

if 'Language' not in st.session_state:
    st.session_state.selected_index = 7
    st.session_state.Language = "ZH"


for i, code in enumerate(locales.keys()):
    display_languages.append(f"{code} - {locales[code].get('Language')}")
    if code == st.session_state.Language:
        st.session_state.selected_index = i
        st.session_state.Language = code

def change_language():
    # print("st.session_state.selectbox_value:" + st.session_state.selectbox_value)
    for item in display_languages:
        if item == st.session_state.selectbox_value:
            # print("item:" + item)
            st.session_state.selected_index = display_languages.index(item)
            st.session_state.Language = item.split(" - ")[0]
    # print("st.session_state.selected_index:" + str(st.session_state.selected_index))

col1, col2, col3 = st.columns(3)

# col2.selectbox(label="Language", options=display_languages, label_visibility='collapsed',index=st.session_state.selected_index, key="selectbox_value", on_change=change_language)

def i18n(key):
    loc = locales.get(st.session_state.Language, {})
    return loc.get("Translation", {}).get(key, key)

st.session_state["click_image"] = False
st.session_state['disabled_state'] = False
st.session_state['prompt_input'] = ""
st.session_state['tags_input'] = ""
st.session_state['title_input'] = ""
st.session_state.DescPrompt = ""

with st.sidebar:
    selected = option_menu(None, [i18n("Music Song Create"), i18n("Music Share Square"), i18n("Music Project Readme"),i18n("Visit Official WebSite")], icons=['music-note', 'music-note-beamed', 'music-note-list'], menu_icon="cast", default_index=3)
    
    if selected == i18n("Music Song Create"):
        st.switch_page("main.py")
    elif selected == i18n("Music Share Square"):
        st.switch_page("pages/square.py")
    elif selected == i18n("Music Project Readme"):
        st.switch_page("pages/readme.py")
    elif selected == i18n("Visit Official WebSite"):
        st.page_link("https://suno.com", label=i18n("Visit Official WebSite1"), icon="🌐")
        st.page_link("https://sunoapi.net", label=i18n("Visit Official WebSite2"), icon="🌐")
    # print(selected)

st.sidebar.image('https://sunoapi.net/images/wechat.jpg', caption=i18n("Join WeChat Group"))
# st.sidebar.image('https://sunoapi.net/images/donate.jpg', caption=i18n("Buy me a Coffee"))
st.sidebar.markdown(f'<div data-testid="stImageCaption" class="st-emotion-cache-1b0udgb e115fcil0" style="max-width: 100%;"> {i18n("Friendly Link")}</div>', unsafe_allow_html=True)
st.sidebar.page_link("http://www.ruanyifeng.com/blog/", label="阮一峰的网络日志-科技爱好者周刊", icon="🌐")
st.sidebar.page_link("https://chatplusapi.cn/", label="ChatPlus API 大模型集合服务平台", icon="🌐")
st.sidebar.page_link("https://echs.top/", label="二次寒树岁月蹉跎，初心依旧", icon="🌐")
st.sidebar.page_link("https://www.ewsyun.com/", label="E修工电子工单业务云平台", icon="🌐")
st.sidebar.page_link("https://h4ck.org.cn/", label="※呢喃/Msg※ &#8211; obaby@mars", icon="🌐")
st.sidebar.page_link("https://s2.chanyoo.net/", label="云通讯增值服务平台", icon="🌐")
st.sidebar.page_link("https://echeverra.cn/jaychou", label="周杰伦全部15张专辑178首音乐", icon="🌐")
st.sidebar.page_link("https://dujun.io/", label="杜郎俊赏", icon="🌐")
st.sidebar.page_link("https://nanwish.love/", label="墨点白|墨点白", icon="🌐")

def get_whole_song(data):
    try:
        resp = generate_concat(data, get_random_token())
        return resp
    except Exception as e:
        return {"detail":str(e)}

def fetch_status(aid: str, col2):
    progress_text = i18n("Fetch Status Progress")
    my_bar = col2.progress(0, text=progress_text)
    percent_complete = 0
    my_bar.progress(percent_complete, text=progress_text)
    while True:
        resp = get_feed(aid, get_random_token())
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
            check_url_available(resp[0]["video_url"], False)
            my_bar.empty()
        elif status == "Unauthorized":
            st.session_state.token = get_random_token()
            continue
        elif status == "Not found.":
            continue
        elif status == "error":
            my_bar.empty()
        else:
            progress_text = i18n("Fetch Status Running") + status
            status = "queued"
            my_bar.progress(percent_complete, text=progress_text)
        
        result = suno_sqlite.query_one("select aid from music where aid =?", (aid,))
        print(result)
        print("\n")
        if result:
            result = suno_sqlite.operate_one("update music set data=?, updated=(datetime('now', 'localtime')), sid=?, name=?, image=?, title=?, tags=?, prompt=?, duration=?, status=? where aid =?", (str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], status, aid))
            print(local_time() + f" ***fetch_status_update aid -> {aid} status -> {status} data -> {str(resp[0])} ***\n")
        else:
            result = suno_sqlite.operate_one("insert into music (aid, data, sid, name, image, title, tags, prompt,duration, status, private) values(?,?,?,?,?,?,?,?,?,?,?)", (str(resp[0]["id"]), str(resp[0]), resp[0]["user_id"], resp[0]["display_name"], resp[0]["image_url"], resp[0]["title"], resp[0]["metadata"]["tags"], resp[0]["metadata"]["gpt_description_prompt"], resp[0]["metadata"]["duration"], status, 0))
        print(result)
        print("\n")

        if status == "complete" or status == "error":
            break

        time.sleep(10)
    if S3_WEB_SITE_URL is not None and (S3_WEB_SITE_URL != "http://localhost:8501" or S3_WEB_SITE_URL != "https://cdn1.suno.ai"):
        resp[0]["audio_url"] = resp[0]["audio_url"].replace(S3_WEB_SITE_URL, 'https://res.sunoapi.net')
        resp[0]["video_url"] = resp[0]["video_url"].replace(S3_WEB_SITE_URL, 'https://res.sunoapi.net')
    return resp

def localdatetime(str):
    # 将字符串时间 转化为 datetime 对象
    dateObject = dateutil.parser.isoparse(str)
    # print(dateObject)  2021-09-03 20:56:35.450686+00:00
    # from zoneinfo import ZoneInfo
    # 根据时区 转化为 datetime 数据
    # localdt = dateObject.replace(tzinfo = timezone.utc).astimezone(ZoneInfo("Asia/Shanghai"))
    localdt = dateObject.replace(tzinfo = timezone.utc).astimezone(tz=None)
    # print(localdt)  # 2021-09-04 04:56:35.450686+08:00
    # 产生本地格式 字符串
    # print(localdt.strftime('%Y-%m-%d %H:%M:%S'))
    return localdt.strftime('%Y-%m-%d %H:%M:%S')

aid = ""
if 'aid' in st.session_state and len(st.session_state.aid) == 36:
    aid = st.session_state.aid
    # print(aid)
else:
    if 'aid' not in st.session_state and len(st.query_params.get_all("id")) == 0:
        # col2.error(i18n("FetchFeed FeedID Error"))
        st.switch_page("pages/square.py")
    elif st.query_params.id != "" and len(st.query_params.id) == 36:
        aid = st.query_params["id"]

if aid != "" and len(aid) == 36:
    # print(aid)
    # print("\n")
    result = suno_sqlite.query_one("select aid,data,created,updated,status,private from music where aid=?", (aid,))
    # print(result)
    # print("\n")
    if result is not None and len(result) > 0 and result[5] == 0:
        data = ast.literal_eval(result[1])
        print(data)
        print("\n")
        if data['status'] == "complete":
            container = col2.container(border=True)
            title = "None\n" if data['title'] is None or "" else data['title'].strip()
            container.markdown(f'''
                <h3>{title}</h3> 
                ''', unsafe_allow_html=True)
            cols = None
            if data['metadata']['audio_prompt_id'] is not None:
                cols = container.columns(4)
            else:
                cols = container.columns(3)

            # part_button = None
            if data['metadata']['history'] is not None:
                # cols[0].markdown(f'''
                # <h3>{i18n("Song Part")} {len(data['metadata']['history'])+1}</h3> 
                # ''', unsafe_allow_html=True)
                part_button = cols[0].button(f'''{i18n("Song Part")} {len(data['metadata']['history'])+1}''', type="secondary")
            elif data['metadata']['concat_history'] is not None:
                # cols[0].markdown(f'''
                # <h3>{i18n("Full Song")}</h3> 
                # ''', unsafe_allow_html=True)
                part_button = cols[0].button(f'''{i18n("Full Song")}''', type="secondary")
            else:
                # cols[0].markdown(f'''
                # <h3>{i18n("Song Part")} 1</h3> 
                # ''', unsafe_allow_html=True)
                part_button = cols[0].button(f'''{i18n("Song Part")} 1''', type="secondary")

            part_modal = Modal(title=title, key="part_modal", padding=20, max_width=550)
            if part_button and (data['metadata']['history'] is not None or data['metadata']['concat_history'] is not None):
                part_modal.open()
            if part_modal.is_open():
                with part_modal.container():
                    if data['metadata']['history'] is not None:
                        for index, item in enumerate(data['metadata']['history']):
                            st.write(f'''{i18n("Song Part")} {str(index+1)} /song?id={item['id']}''')
                    if data['metadata']['concat_history'] is not None:
                        for index, item in enumerate(data['metadata']['concat_history']):
                            st.write(f'''{i18n("Song Part")} {str(index+1)} /song?id={item['id']}''')

            reuse_button = cols[1].button(i18n("Reuse Prompt"), type="secondary")
            if reuse_button:
                st.session_state['title_input'] = title
                st.session_state['tags_input'] = ""
                st.session_state['prompt_input'] = "" if data['metadata']['prompt'] == "[Instrumental]" else data['metadata']['prompt']
                st.session_state["continue_at"] = ""
                st.session_state["continue_clip_id"] = ""
                st.switch_page("main.py")

            continue_button = cols[2].button(i18n("Continue Extend"), type="secondary")
            if continue_button:
                st.session_state['title_input'] = title
                st.session_state['tags_input'] = ""
                st.session_state['prompt_input'] = ""
                st.session_state["continue_at"] = str(data['metadata']['duration'])[0:6]
                st.session_state["continue_clip_id"] = aid
                st.switch_page("main.py")

            if data['metadata']['audio_prompt_id'] is not None:
                whole_button = cols[3].button(i18n("Get Whole Song"), type="secondary")
                if whole_button:
                    data1 = {
                        "clip_id": aid
                    }
                    # print(data1)
                    # print("\n")
                    resp = get_whole_song(data1)
                    print(resp)
                    print("\n")
                    status = resp["status"] if "status" in resp else resp["detail"]
                    if status == "queued" or status == "complete":
                        result = suno_sqlite.operate_one("insert into music (aid, data, private) values(?,?,?)", (str(resp["id"]), str(resp), 0))
                        resp0 = fetch_status(resp["id"], col2)
                        if resp0[0]["status"] == "complete":
                            col2.success(i18n("Generate Success") + resp0[0]["id"])
                            st.session_state.aid = resp0[0]["id"]
                            # print(st.session_state.aid)
                            st.switch_page("pages/song.py")
                        else:
                            col2.error(i18n("Generate Status Error")  + (resp0[0]['status'] if resp0[0]['metadata']["error_message"] is None else resp0[0]['metadata']["error_message"]))
                    else:
                        col2.error(i18n("Generate Submit Error") + status)
            
            container.write("https://sunoapi.net/song?id=" + aid + "\n\n" + i18n("Desc Prompt") + ("None\n" if data['metadata']['gpt_description_prompt'] is None or "" else data['metadata']['gpt_description_prompt']) + " \n\n" + i18n("Tags") +  ("None\n" if data['metadata']['tags'] is None or "" else data['metadata']['tags'] + "\n") + "&nbsp;&nbsp;" + i18n("Music Duration")  + ("None\n" if data['metadata']['duration'] is None or "" else str(int(data['metadata']['duration']/60)) + ":" + str("00" if int(data['metadata']['duration']%60) == 0 else ("0" + str(int(data['metadata']['duration']%60))  if int(data['metadata']['duration']%60) <10 else int(data['metadata']['duration']%60))) + " \n") + "\n\n" + i18n("Music Created At") + ("None\n" if data['created_at'] is None or "" else localdatetime(data['created_at'])) + "\n\n" + i18n("Music Prompt"))

            container.markdown("" if data['metadata']['prompt'] is None or "" else data['metadata']['prompt'].replace("\n", "\n\n"), unsafe_allow_html=True)

            title = data['title'].strip().replace("\n","")
            with col1:
                st.audio(data['audio_url'] + "?play=true")
                st.video(data['video_url'] + "?play=true")

            # Artalk评论初始化
            hide_streamlit_style1 = f"""
            <!-- CSS -->
            <link href="https://sunoapi.net/dist/Artalk.css" rel="stylesheet" />
            <!-- JS -->
            <script src="https://sunoapi.net/dist/Artalk.js"></script>
            <!-- Artalk -->
            <div id="Comments"></div>
            <script>
            Artalk.init({{
            el:        '#Comments',
            pageKey:   '/song?id={aid}',
            pageTitle: '{title}',
            server:    'https://sunoapi.net',
            site:      'SunoAPI AI Music Generator',
            }})
            </script>
            <div style="font-size: 12px;font-family: inherit; color: #697182;justify-content: center; align-items: center; word-break: break-word; text-align: center;padding-right: 15px;">本页浏览量 <span id="ArtalkPV">Loading...</span> 次</div>
            <style>
            .atk-list-no-comment {{font-size: 14px;}}
            </style>
            """
            
            with col3:
                st.components.v1.html(hide_streamlit_style1, height=940)
        else:
            col2.error(i18n("Generation Task Status") + data["status"])
    else:
        col2.error(i18n("FetchFeed FeedID Error"))


# 隐藏右边的菜单以及页脚
hide_streamlit_style = """
<style>
#MainMenu {display: none;}
footer {display: none;}
.eczjsme10 {display: none;}
.e1nzilvr5 {overflow-x: auto; overflow-y: auto; max-height: 650px;}
p {font-size: 15px;}
span {font-size: 20px;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

components.iframe("https://sunoapi.net/analytics.html", height=0)