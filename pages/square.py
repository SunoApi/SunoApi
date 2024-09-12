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
<style>#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2rem;}</style>
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

st.session_state['disabled_state'] = False
st.session_state['prompt_input'] = ""
st.session_state['tags_input'] = ""
st.session_state['title_input'] = ""
st.session_state["continue_at"] = ""
st.session_state["continue_clip_id"] = ""
st.session_state.DescPrompt = ""

with st.sidebar:
    selected = option_menu(None, [i18n("Music Song Create"), i18n("Music Share Square"), i18n("Music Project Readme"),i18n("Visit Official WebSite")], icons=['music-note', 'music-note-beamed', 'music-note-list'], menu_icon="cast", default_index=1)
    
    if selected == i18n("Music Song Create"):
        st.switch_page("main.py")
    elif selected == i18n("Music Project Readme"):
        st.switch_page("pages/readme.py")
    elif selected == i18n("Visit Official WebSite"):
        st.page_link("https://suno.com", label=i18n("Visit Official WebSite1"), icon="🌐")
        st.page_link("https://sunoapi.net", label=i18n("Visit Official WebSite2"), icon="🌐")
    # print(selected)

st.sidebar.image('https://sunoapi.net/images/wechat.jpg', caption=i18n("Join WeChat Group"))
# st.sidebar.image('https://sunoapi.net/images/donate.jpg', caption=i18n("Buy me a Coffee"))
st.sidebar.markdown(f'<div data-testid="stImageCaption" class="st-emotion-cache-1b0udgb e115fcil0" style="max-width: 100%;"> {i18n("Friendly Link")}</div>', unsafe_allow_html=True)
result = suno_sqlite.query_many("select link,label,status from link where status=0 order by id")
# print(result)
# print("\n")
if result is not None and len(result) > 0:
    for row in result:
        st.sidebar.page_link(row[0], label=row[1], icon="🌐")


def change_page():
    # print("st.session_state.change_page:" + str(st.session_state.change_page))
    st.session_state.page = 1 if 'change_page' not in st.session_state else st.session_state.change_page


if 'page' not in st.session_state:
    st.session_state.page = 1
else:
    st.session_state.page = 1 if 'change_page' not in st.session_state else st.session_state.change_page


title = col2.text_input(" ", "", placeholder=i18n("Enter Search Keywords"))

records_per_page = 40
result = suno_sqlite.query_one("select count(id) from music where private=0")
if title != "":
    result = suno_sqlite.query_one("select count(id) from music where (LOWER(title) like ? or aid=?) and private=0", ("%"+ title +"%", title))
if result is not None:
    total_records = int(result[0])
    total_pages = (total_records // records_per_page) + (1 if total_records % records_per_page else 0)
    page_number = st.session_state.page
    offset = (page_number - 1) * records_per_page

result = suno_sqlite.query_many("select aid,data,created,updated,status,private from music where private=0 order by created desc LIMIT ? OFFSET ? ", (records_per_page, offset,))

if title != "":
    result = suno_sqlite.query_many("select aid,data,created,updated,status,private from music where (LOWER(title) like ? or aid=?) and private=0 order by created desc LIMIT ? OFFSET ? ", ("%"+ title +"%", title, records_per_page, offset,))


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

titles = []
images = []
captions = []
if result is not None and len(result) > 0:
    for row in result:
        # print(ast.literal_eval(row[1]))
        # print("\n")
        data = ast.literal_eval(row[1])
        # print("data['title']:" + data['title'])
        title = ""
        title += i18n("FeedID") + ("None\n" if data['id'] is None or "" else data['id'] + "\n")
        title += i18n("Title") + ("None\n" if data['title'] is None or "" else data['title'] + "\n")
        title += i18n("Desc Prompt") + ("None\n" if "gpt_description_prompt" not in data else data['metadata']['gpt_description_prompt'] + "\n")
        title += i18n("Tags") + ("None\n" if "tags" not in data['metadata'] else data['metadata']['tags'] + "  " + i18n("Music Duration")  + ("None\n" if "duration" not in data['metadata'] else str(int(data['metadata']['duration']/60)) + ":" + str("00" if int(data['metadata']['duration']%60) == 0 else ("0" + str(int(data['metadata']['duration']%60))  if int(data['metadata']['duration']%60) <10 else int(data['metadata']['duration']%60))) + " \n"))
        title += i18n("Music Created At")  + ("None\n" if data['created_at'] is None or "" else localdatetime(data['created_at'])) + "  " +  i18n("Select Model") + ("None\n" if data['model_name'] is None or "" else i18n("Upload Audio Type") + "\n\n" if data['metadata']['type'] == "upload" else data['model_name'] + "\n\n")
        title += i18n("Music Prompt")  + ("None\n" if data['metadata']['prompt'] is None or "" else data['metadata']['prompt'] + "\n")
        
        titles.append(title)
        captions.append("sunoai" if data['title'] is None or "" else f'<div style="justify-content: center; align-items: center; word-break: break-word; text-align: center;padding-right: 15px;"><a style="background: #fafafa; color: #666; text-decoration: none;" href="/song?id={data["id"]}" target="_blank" title="{data["title"]}">{data["title"] if len(data["title"])<=10 else data["title"][0:10]+"..."}</a></div>')
        images.append("https://sunoapi.net/images/sunoai.jpg" if data['image_url'] is None or "" else data['image_url'])

print("\n")

use_container_width = False

if len(images) > 0 and len(images)%40 == 0:
    use_container_width = True

index = image_select(
            label="",
            images=images if len(images) > 0 else ["https://sunoapi.net/images/sunoai.jpg"],
            captions=captions if len(captions) > 0 else [i18n("No Search Result")],
            titles=titles if len(titles) > 0 else [""],
            use_container_width=use_container_width,
            return_value="index"
        )

open_modal = True

if 'index' not in st.session_state:
    open_modal = False
elif 'index' in st.session_state and st.session_state.index != index:
    open_modal = True
else:
    open_modal = False

st.session_state.index = index


data = {}

if result:
    data = ast.literal_eval(result[index][1])
    video_modal = Modal(title=data['title'], key="video_modal", padding=20, max_width=520)

sac.pagination(total=total_records, index=page_number, page_size=records_per_page, align='center', jump=True, show_total=True, key='change_page', on_change=change_page)

if result and open_modal:
    video_modal.open()

if video_modal.is_open() and st.session_state.index != 0:
   st.session_state.index = 0
   st.session_state.aid = data['id']
   # print(st.session_state.aid)
   st.switch_page("pages/song.py")


# 隐藏右边的菜单以及页脚
hide_streamlit_style = """
<style>
#MainMenu {display: none;}
footer {display: none;}
.eczjsme10 {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Artalk评论初始化
hide_streamlit_style1 = f"""
<!-- CSS -->
<link href="https://sunoapi.net/dist/Artalk.css" rel="stylesheet" />
<!-- JS -->
<script src="https://sunoapi.net/dist/Artalk.js"></script>
<!-- Artalk -->
<div style="font-size: 12px;font-family: inherit; color: #697182;justify-content: center; align-items: center; word-break: break-word; text-align: center;padding-right: 15px;">本页浏览量 <span id="ArtalkPV">Loading...</span> 次</div>
<div id="Comments"></div>
<script>
Artalk.init({{
el:        '#Comments',
pageKey:   '/square',
pageTitle: '音乐分享广场',
server:    'https://sunoapi.net',
site:      'SunoAPI AI Music Generator',
}})
</script>
"""
components.html(hide_streamlit_style1, height=0)

components.iframe("https://sunoapi.net/analytics.html", height=0)