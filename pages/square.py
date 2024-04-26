
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

st.set_page_config(page_title="Suno API AI Music Generator",
                   page_icon="🎵",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   menu_items={
                       'Report a bug': "https://github.com/SunoApi/SunoApi/issues",
                       'About': "Suno API AI Music Generator is a free AI music generation software, calling the existing API interface to achieve AI music generation. If you have any questions, please visit our website url address: https://sunoapi.net\n\nDisclaimer: Users voluntarily input their account information that has not been recharged to generate music. Each account can generate five songs for free every day, and we will not use them for other purposes. Please rest assured to use them! If there are 10000 users, the system can generate 50000 songs for free every day. Please try to save usage, as each account can only generate five songs for free every day. If everyone generates more than five songs per day, it is still not enough. The ultimate goal is to keep them available for free generation at any time when needed.\n\n"
                   })

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


hide_streamlit_style = """
<style>#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2rem;}</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Suno AI Music", [i18n("Music Song Create"), i18n("Music Share Square"), i18n("Music Project Readme")],icons=['music-note', 'music-note-beamed', 'music-note-list'], menu_icon="cast", default_index=1)
    
    if selected == i18n("Music Song Create"):
        st.switch_page("main.py")
    elif selected == i18n("Music Project Readme"):
        st.switch_page("pages/readme.py")
    elif selected == i18n("Visit Official WebSite"):
        st.page_link("https://suno.com", label=i18n("Visit Official WebSite1"), icon="🌐")
        st.page_link("https://sunoapi.net", label=i18n("Visit Official WebSite2"), icon="🌐")
    # print(selected)

st.sidebar.image('https://sunoapi.net/images/wechat.jpg', caption=i18n("Join WeChat Group"))
st.sidebar.image('https://sunoapi.net/images/donate.jpg', caption=i18n("Buy me a Coffee"))

if 'page' not in st.session_state:
    st.session_state.page = 1
else:
    st.session_state.page = 1 if 'cmpage' not in st.session_state else st.session_state.cmpage

title = col2.text_input(" ", "", placeholder=i18n("Enter Search Keywords"))

records_per_page = 40
result = suno_sqlite.query_one("select count(id) from music where private=0")
if title != "":
    result = suno_sqlite.query_one("select count(id) from music where (LOWER(title) like ? or aid=?) and private=0", ("%"+ title +"%", title))
total_records = int(result[0])
total_pages = (total_records // records_per_page) + (1 if total_records % records_per_page else 0)
page_number = st.session_state.page
offset = (page_number - 1) * records_per_page

result = suno_sqlite.query_many("select aid,data,created,updated,status,private from music where private=0 order by id desc LIMIT ? OFFSET ? ", (records_per_page, offset,))

if title != "":
    result = suno_sqlite.query_many("select aid,data,created,updated,status,private from music where (LOWER(title) like ? or aid=?) and private=0 order by id desc LIMIT ? OFFSET ? ", ("%"+ title +"%", title, records_per_page, offset,))


def localdatetime(str):
    # 将字符串时间 转化为 datetime 对象
    dateObject = dateutil.parser.isoparse(str)
    # print(dateObject)  2021-09-03 20:56:35.450686+00:00
    # 根据时区 转化为 datetime 数据
    localdt = dateObject.replace(tzinfo = timezone.utc).astimezone(tz=None)
    # print(localdt)  # 2021-09-04 04:56:35.450686+08:00
    # 产生本地格式 字符串
    # print(localdt.strftime('%Y-%m-%d %H:%M:%S'))
    return localdt.strftime('%Y-%m-%d %H:%M:%S')


titles = []
images = []
captions = []
for row in result:
    # print(ast.literal_eval(row[1]))
    # print("\n")
    data = ast.literal_eval(row[1])
    title = ""
    title += "歌曲名称：" + ("无\n" if data['title'] is None or "" else data['title'] + "\n")
    title += "音乐风格：" + ("无\n" if data['metadata']['tags'] is None or "" else data['metadata']['tags'] + "\n")
    title += "歌曲描述：" + ("无\n" if data['metadata']['gpt_description_prompt'] is None or "" else data['metadata']['gpt_description_prompt'] + "\n")
    title += "歌曲时长：" + ("无\n" if data['metadata']['duration'] is None or "" else str(int(data['metadata']['duration']/60)) + "分" + str(int(data['metadata']['duration']%60))+ "秒\n")
    title += "生成时间：" + ("无\n" if data['created_at'] is None or "" else localdatetime(data['created_at']) + "\n\n")
    title += "生成歌词：\n" + ("无\n" if data['metadata']['prompt'] is None or "" else data['metadata']['prompt'] + "\n")
    
    titles.append(title)
    captions.append("sunoai" if data['title'] is None or "" else data['title'])
    images.append("https://sunoapi.net/images/sunoai.jpg" if data['image_url'] is None or "" else data['image_url'])

print("\n")

index = 0
use_container_width = False

if len(images) > 0:
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

sac.pagination(total=total_records, page_size=records_per_page, align='center', jump=True, show_total=True, key='cmpage')

if result and open_modal:
    video_modal.open()

if result and video_modal.is_open():
    with video_modal.container():
        if data['status'] == "complete":
            st.session_state.index = index
            st.video(data['video_url'])
        else:
            st.error(i18n("Generation Task Status") + data["status"])

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