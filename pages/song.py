
# -*- coding:utf-8 -*-

import streamlit as st
import time,json,os,ast
from datetime import timezone
import dateutil.parser

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
st.sidebar.image('https://sunoapi.net/images/donate.jpg', caption=i18n("Buy me a Coffee"))

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
        # print(data)
        # print("\n")
        if data['status'] == "complete":
            container = col2.container(border=True)
            container.title("None\n" if data['title'] is None or "" else data['title'])
            
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