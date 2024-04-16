
import streamlit as st
import time,json,os,ast

from streamlit_option_menu import option_menu
from streamlit_image_select import image_select

from streamlit_modal import Modal
import streamlit.components.v1 as components

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


root_dir = os.path.dirname(os.path.realpath(__file__))
# print(root_dir)
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


hide_streamlit_style = """
<style>#root > div:nth-child(1) > div > div > div > div > section > div > div > ul {display:'block';}</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Suno AI Music", [i18n("Music Song Create"), i18n("Music Share Square"), i18n("Visit Official WebSite")],icons=['music-note', 'music-note-beamed', 'music-note-list'], menu_icon="cast", default_index=1)
    
    if selected == i18n("Music Song Create"):
        st.switch_page("main.py")
    elif selected == i18n("Visit Official WebSite"):
        st.page_link("https://suno.com", label=i18n("Visit Official WebSite1"), icon="🌐")
        st.page_link("https://sunoapi.net", label=i18n("Visit Official WebSite2"), icon="🌐")
    print(selected)

st.sidebar.image('https://sunoapi.net/images/wechat.jpg', caption=i18n("Join WeChat Group"))


import streamlit_antd_components as sac

if 'page' not in st.session_state:
    st.session_state.page = 1
else:
    st.session_state.page = 1 if 'cmpage' not in st.session_state else st.session_state.cmpage

records_per_page = 40
result = suno_sqlite.query_one("select count(id) from music where private=0")
total_records = int(result[0])
total_pages = (total_records // records_per_page) + (1 if total_records % records_per_page else 0)
# col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
# page_number = col6.number_input("", min_value=1, max_value=total_pages, value=1)
page_number = st.session_state.page
offset = (page_number - 1) * records_per_page

result = suno_sqlite.query_many("select aid,data,created,updated,status,private from music where private=0 order by id desc LIMIT ? OFFSET ? ", (records_per_page, offset,))

images = []
captions = []
for row in result:
    # print(ast.literal_eval(row[1]))
    print("\n")
    captions.append(ast.literal_eval(row[1])['title'])
    images.append(ast.literal_eval(row[1])['image_url'])

index = image_select(
        label="",
        images= images if len(images) > 0 else ["https://sunoapi.net/images/wechat.jpg"],
        captions=captions if len(captions) > 0 else ["wechat"],
        use_container_width=False,
        return_value="index",
    )

open_modal = True

if 'index' not in st.session_state:
    open_modal = False
elif 'index' in st.session_state and st.session_state.index != index:
    open_modal = True
else:
    open_modal = False

st.session_state.index = index

sac.pagination(total=total_records, page_size=records_per_page, align='center', jump=True, show_total=True, key='cmpage')

if result:
    video_modal = Modal(title=ast.literal_eval(result[index][1])['title'], key="video_modal", padding=20, max_width=520)

# open_modal = st.button("查看")
if result and open_modal:
    video_modal.open()

if result and video_modal.is_open():
    with video_modal.container():
        st.session_state.index = index
        st.video(ast.literal_eval(result[index][1])['video_url'])