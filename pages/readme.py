
import streamlit as st
import time,json,os,ast

from streamlit_option_menu import option_menu
from streamlit_image_select import image_select

from streamlit_modal import Modal
import streamlit.components.v1 as components
import streamlit_antd_components as sac

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


root_dir = os.path.dirname(os.path.realpath(__file__))
# print(root_dir)
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
st.sidebar.image('https://sunoapi.net/images/donate.jpg', caption=i18n("Buy me a Coffee"))

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

components.iframe("https://sunoapi.net/analytics.html", height=0)