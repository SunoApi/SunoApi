<div align="center">

[简体中文](README_ZH.md) | [繁體中文](README_TC.md) | [Русский язык](README_RU.md) | [한국어](README_KR.md) | [日本語](README_JP.md)


[![GitHub release](https://img.shields.io/static/v1?label=release&message=v1.0.0&color=blue)](https://www.github.com/novicezk/midjourney-proxy)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# Suno API is an unofficial Suno AI client

# Congratulations on this open source project's being selected for this week's weekly
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>



### Introduction

- This is an unofficial Suno API client based on Python and Streamlit currently supports functions such as generating music and obtaining music information. It comes with built-in maintenance and activation functions for tokens, so there is no need to worry about token expiration. You can set up multiple account information to be saved for use.

- GitHub sometimes cannot be accessed. If it cannot be accessed, please move to Gitee address: https://gitee.com/SunoApi/SunoApi

### Features

- Set account information and automatically maintain and keep the program active
- Multiple account information can be set to be saved and used
- Music Sharing Square showcases all publicly available songs
- Enter the music feed ID to directly obtain song information

### Debug

#### Python local debug running

- Installation dependencies

```bash
pip3 install -r requirements.txt
```

- Start the project, please refer to the Streamlit documentation for details on Streamlit

```bash
streamlit run main.py
```

### Deploy

#### Docker local one-click deployment

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  sunoapi/sunoapi:latest
```

#### Docker local compilation and deployment

```bash
docker compose build && docker compose up
```

#### Dockerfile

```docker
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8501
CMD [ "nohup", "streamlit", "run", "main.py" ]
```

#### Docker pull image deployment

```bash
docker-compose pull && docker-compose up -d
```

#### docker-compose.yml

```docker
version: '3.1'

services:
  sunoapi:
    image: sunoapi/sunoapi:latest
    container_name: sunoapi
    ports:
      - "8501:8501"
    volumes:
      - ./sunoapi.db:/app/sunoapi.db
    restart: always
```

#### Streamlit remote repositories deployment

- First, Fork a copy of SunoApi code to your Github repository
- Select Github authorization login: https://share.streamlit.io/
- Open the deployment page: https://share.streamlit.io/deploy
- Repository selection: SunoApi/SunoApi
- Branch input: main
- Main file path input: main.py
- Click Deploy!

#### Zeabur one-click deployment

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/5BLAEZ)


#### Configuration

- First, retrieve your session and cookie from the browser page when logged in.

![session](https://sunoapi.net/images/session.png)

- After filling in the setting information, it will automatically keep alive. You can fill in multiple account information.

![session1](https://sunoapi.net/images/session1.png)

- Enter and save the information. You can modify the account information if you enter identity.

![session2](https://sunoapi.net/images/session2.png)

### Done

- Once the project is up and running, visit http://localhost:8501/ in your browser.

![index](https://sunoapi.net/images/index.png)

![index1](https://sunoapi.net/images/index1.png)

![index2](https://sunoapi.net/images/index2.png)

![index3](https://sunoapi.net/images/index3.png)


### Questions

- If the page promp the message: Please save the information first, and then refresh the page to use it normally! Please first add your own account information and save it, then delete other invalid account information in the sunoapi.db database, including the account information I tested, and then you can use it normally.
- If the page promp the message: "Suno AI Music song generation failed to submit: Insufficient credits." Indicates that the credits of account information are insufficient, please add your account information to save, and then you can use it normally.
- After the music generation task is successfully submitted, the queue status of the generation task is pulled. When the status is "complete", it returns successfully. At this time, it defaults to waiting for the official generation file for 15 seconds. The official interface service directly returns the URL address of media files, and most of the time the page can display these media files normally. Occasionally, the interface may have returned the Url address of the media file, but the actual file cannot be accessed from the Url address and needs to wait for a while. At this point, the media file may not be able to be loaded on the page. You can right-click on the media player and copy the media file address. Open the address separately in the browser to access it, or right-click to save as download and save.
- Regarding the security issue of saving account session and cookie information, as long as your account is not recharged, there is no need to worry because you do not know your account password. The session and cookie information you fill in will become invalid if your account logs in to other activities or logs out of the official website, and the session and cookie information you fill in will change the next time you log in to the official website.


### Creation

- Professional lyric assistance tools: https://poe.com/SuperSunoMaster


### Contact

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<img src="https://sunoapi.net/images/wechat.jpg" width="382px" height="511px" />


### Participate

- My personal strength is always limited, any form of contribution is welcome, including but not limited to contributing code, optimizing documents, submitting issues and PR. Due to limited time, we do not accept to submit bugs to developers in wechat or wechat group, please submit issues and PR if you have problems or optimization suggestions!

[![Star History Chart](https://api.star-history.com/svg?repos=SunoApi/SunoApi&type=Timeline)](https://star-history.com/#SunoApi/SunoApi&Timeline)


### Reference

- Suno AI official website: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### Statement

- SunoApi is an unofficial open source project for study and research only. Users voluntarily enter free account information to generate music. Each account generates five songs per day for free, and we don't use them for other purposes. Please feel free to use! If there are 10,000 users, the system can generate 50,000 songs per day for free. Please try to save your usage as you can only generate five songs per account per day for free. If everyone writes more than five songs a day, it's still not enough. The ultimate goal is to make it free to build whenever you need it.
