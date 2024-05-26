
# -*- coding:utf-8 -*-

import streamlit as st
import time,json,os,ast

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
                   initial_sidebar_state="auto",
                   menu_items={
                       'Report a bug': "https://github.com/SunoApi/SunoApi/issues",
                       'About': "SunoAPI AI Music Generator is a free AI music generation software, calling the existing API interface to achieve AI music generation. If you have any questions, please visit our website url address: https://sunoapi.net\n\nDisclaimer: Users voluntarily input their account information that has not been recharged to generate music. Each account can generate five songs for free every day, and we will not use them for other purposes. Please rest assured to use them! If there are 10000 users, the system can generate 50000 songs for free every day. Please try to save usage, as each account can only generate five songs for free every day. If everyone generates more than five songs per day, it is still not enough. The ultimate goal is to keep them available for free generation at any time when needed.\n\n"
                   })

i18n_dir = os.path.join(root_dir, "../i18n")
# print(i18n_dir)
md_dir = os.path.join(root_dir, "../")
# print(md_dir)

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

hide_streamlit_style = """
<style>#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2rem;}</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.session_state["page"] = 1
st.session_state["click_image"] = False
st.session_state['disabled_state'] = False
st.session_state['prompt_input'] = ""
st.session_state['tags_input'] = ""
st.session_state['title_input'] = ""
st.session_state.DescPrompt = ""

with st.sidebar:
    selected = option_menu(None, [i18n("Music Song Create"), i18n("Music Share Square"), i18n("Music Project Readme"),i18n("Visit Official WebSite")],icons=['music-note', 'music-note-beamed', 'music-note-list'], menu_icon="cast", default_index=2)
    
    if selected == i18n("Music Song Create"):
        st.switch_page("main.py")
    elif selected == i18n("Music Share Square"):
        st.switch_page("pages/square.py")
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
st.sidebar.page_link("https://dusays.com/", label="杜老师说", icon="🌐")
st.sidebar.page_link("https://www.ewsyun.com/", label="E修工电子工单业务云平台", icon="🌐")
st.sidebar.page_link("https://h4ck.org.cn/", label="钟小姐baby@mars", icon="🌐")
st.sidebar.page_link("https://s2.chanyoo.net/", label="云通讯增值服务平台", icon="🌐")
st.sidebar.page_link("https://echeverra.cn/jaychou", label="周杰伦全部15张专辑178首音乐", icon="🌐")
st.sidebar.page_link("https://dujun.io/", label="杜郎俊赏", icon="🌐")
st.sidebar.page_link("https://nanwish.love/", label="墨点白|墨点白", icon="🌐")


md = ""
language = "ZH"
if st.session_state.Language == "EN":
    language = ""
else:
    language = "_" + st.session_state.Language

with open(os.path.join(md_dir, "README"+language+".md"), "r", encoding="utf-8") as f:
        md = f.read()

st.markdown(md, unsafe_allow_html=True)

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
hide_streamlit_style1 = """
<!-- CSS -->
<link href="https://sunoapi.net/dist/Artalk.css" rel="stylesheet" />
<!-- JS -->
<script src="https://sunoapi.net/dist/Artalk.js"></script>
<!-- Artalk -->
<div id="Comments"></div>
<script>
  Artalk.init({
  el:        '#Comments',
  pageKey:   '/readme',
  pageTitle: '本站项目说明',
  server:    'https://sunoapi.net',
  site:      'SunoAPI AI Music Generator',
  })
</script>
<div style="font-size: 12px;font-family: inherit; color: #697182;justify-content: center; align-items: center; word-break: break-word; text-align: center;padding-right: 15px;">本页浏览量 <span id="ArtalkPV">Loading...</span> 次</div>
"""
components.html(hide_streamlit_style1, height=940)

components.iframe("https://sunoapi.net/analytics.html", height=0)