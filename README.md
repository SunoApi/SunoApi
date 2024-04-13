[简体中文](README_ZH.md) | [繁體中文](README_TC.md) | [한국어](README_KR.md) | [日本語](README_JP.md)

# Suno API is an unofficial Suno AI client

This is an unofficial Suno API client based on Python and Streamlit currently supports functions such as generating music and obtaining music information.
It comes with built-in maintenance and activation functions for tokens, so there is no need to worry about token expiration. You can set up multiple account information to be saved for use.

### Features

- Automatic maintenance and preservation of tokens
- Multiple account information can be set to be saved and used
- The code is simple, easy to maintain, and convenient for secondary development

### Usage

#### Run

Installation dependencies

```bash
pip3 install -r requirements.txt
```

Start the project, please refer to the Streamlit documentation for details on Streamlit

```bash
streamlit run main.py
```

#### Docker

```bash
docker compose build && docker compose up
```


#### Configuration

First, retrieve your session and cookie from the browser page when logged in.

![session](https://sunoapi.net/images/session.png)

After filling in the setting information, it will automatically keep alive. You can fill in multiple account information.

![session1](https://sunoapi.net/images/session1.png)

Enter and save the information. You can modify the account information if you enter identity.

![session2](https://sunoapi.net/images/session2.png)

#### Done

Once the project is up and running, visit http://localhost:8501/ in your browser.

![index](https://sunoapi.net/images/index.png)


#### Questions

- If the page keeps prompting: Please save the information first, and then refresh the page to use it normally! Please first add your own account information and save it, then delete other invalid account information in the sunoapi.db database, including the account information I tested, and then you can use it normally.
- After the music generation task is successfully submitted, the queue status of the generation task is pulled. When the status is "complete", it returns successfully. At this time, it defaults to waiting for the official generation file for 15 seconds. The official interface service directly returns the URL address of media files, and most of the time the page can display these media files normally. Occasionally, the interface may have returned the Url address of the media file, but the actual file cannot be accessed from the Url address and needs to wait for a while. At this point, the media file may not be able to be loaded on the page. You can right-click on the media player and copy the media file address. Open the address separately in the browser to access it, or right-click to save as download and save.
- Regarding the security issue of saving account session and cookie information, as long as your account is not recharged, there is no need to worry because you do not know your account password. The session and cookie information you fill in will become invalid if your account logs in to other activities or logs out of the official website, and the session and cookie information you fill in will change the next time you log in to the official website.


#### Creation

专业歌词辅助工具：https://poe.com/SuperSunoMaster


#### Contact

<img src="https://sunoapi.net/images/wechat.jpg" width="382px" height="511px" />

## Reference

- Suno AI official website: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


## Statement

SunoApi is an unofficial open source project for study and research only. Users voluntarily enter free account information to generate music. Each account generates five songs per day for free, and we don't use them for other purposes. Please feel free to use! If there are 10,000 users, the system can generate 50,000 songs per day for free. Please try to save your usage as you can only generate five songs per account per day for free. If everyone writes more than five songs a day, it's still not enough. The ultimate goal is to make it free to build whenever you need it.
