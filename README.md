<div align="center">

[简体中文](https://github.com/SunoApi/SunoApi/blob/main/README_ZH.md) | [繁體中文](https://github.com/SunoApi/SunoApi/blob/main/README_TC.md) | [Русский](https://github.com/SunoApi/SunoApi/blob/main/README_RU.md) | [한국어](README_KR.md) | [日本語](https://github.com/SunoApi/SunoApi/blob/main/README_JP.md) | [Français](https://github.com/SunoApi/SunoApi/blob/main/README_FR.md) | [Deutsch](https://github.com/SunoApi/SunoApi/blob/main/README_DE.md)


[![GitHub release](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=black)](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=blue)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# SunoAPI is an unofficial Suno AI client

# Congratulations on this open source project's being selected for this week's weekly
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>



### Introduction

- This is an unofficial SunoAPI client based on Python and Streamlit currently supports functions such as generating music and obtaining music information. It comes with built-in maintenance and activation functions for tokens, so there is no need to worry about token expiration. You can set up multiple account information to be saved for use.

- GitHub sometimes cannot be accessed. If it cannot be accessed, please move to Gitee address: https://gitee.com/SunoApi/SunoApi

### Features

- Set account information and automatically maintain and keep the program active
- Multiple account information can be set to be saved and used
- Music Sharing Square showcases all publicly available songs
- Enter the music feed ID to directly obtain song information
- Support to upload pictures, according to the content of the image analysis to generate songs
- Support multiple languages such as Chinese, English, Korean, Japanese, etc

### Debug

#### Python locally debug running

- Clone source code

```bash
git clone https://github.com/SunoApi/SunoApi.git
```


- Installation dependencies

```bash
cd SunoApi
pip3 install -r requirements.txt
```

- . env environment variable file requires the use of the gpt-4o model for image recognition. The OpenAI interface can be used, or other commonly used interfaces can be used to replace it. Register a console.bitiful.com object storage account to obtain the S3_ACCESSKEY_ID，S3_SECRETKEY_ID parameter, which is used to upload images to the storage bucket you created. Fill in the external access domain name of your object storage account after creating the storage bucket in S3_WEB_SITE_URL. This way, the local environment can test image recognition.

```bash
OPENAI_BASE_URL = https://chatplusapi.cn
OPENAI_API_KEY = sk-xxxxxxxxxxxxxxxxxxxx
#S3_WEB_SITE_URL = https://cdn1.suno.ai
#S3_WEB_SITE_URL = http://localhost:8501
#S3_WEB_SITE_URL = http://123.45.67.8:8501
#S3_WEB_SITE_URL = https://sunoapi.s3.bitiful.net
S3_WEB_SITE_URL = https://res.sunoapi.net
S3_ACCESSKEY_ID = xxxxxxxxxxxxxxxxxxxx
S3_SECRETKEY_ID = xxxxxxxxxxxxxxxxxxxx
```


- Start the project, please refer to the Streamlit documentation for details on Streamlit

```bash
streamlit run main.py --server.maxUploadSize=3
```

### Deploy

#### Docker local one-click deployment

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  -v ./sunoapi.db:/app/sunoapi.db \
  -v ./images/upload:/app/images/upload \
  -v ./audios/upload:/app/audios/upload \
  -e OPENAI_BASE_URL=https://api.openai.com  \
  -e OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx \
  -e S3_WEB_SITE_URL=https://sunoapi.s3.bitiful.net  \
  -e S3_ACCESSKEY_ID=xxxxxxxxxxxxxxxxxxxx  \
  -e S3_SECRETKEY_ID=xxxxxxxxxxxxxxxxxxxx  \
  sunoapi/sunoapi:latest
```

##### Attention: It is necessary to https://sunoapi.s3.bitiful.net Replace with the actual address you can access, and the final uploaded image file will pass through http://xxxxxx.s3.bitiful.net/images/upload/xxxxxx.jpg The format can be accessed, otherwise OpenAI cannot access the image you uploaded and cannot recognize its content. Therefore, the function of uploading images to generate music will not be available.


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
CMD [ "nohup", "streamlit", "run", "main.py", "--server.maxUploadSize=3" ]
```

#### Docker pull image deployment

```bash
docker-compose pull && docker-compose up -d
```

#### docker-compose.yml

```docker
version: '3.2'

services:
  sunoapi:
    image: sunoapi/sunoapi:latest
    container_name: sunoapi
    ports:
      - "8501:8501"
    volumes:
      - ./sunoapi.db:/app/sunoapi.db
      - ./images/upload:/app/images/upload
      - ./audios/upload:/app/audios/upload
    environment:
      - TZ=Asia/Shanghai
      - OPENAI_BASE_URL=https://api.openai.com
      - OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
      - S3_WEB_SITE_URL=https://sunoapi.s3.bitiful.net
      - S3_ACCESSKEY_ID=xxxxxxxxxxxxxxxxxxxx
      - S3_SECRETKEY_ID=xxxxxxxxxxxxxxxxxxxx
    restart: always
```

##### Attention: To pull image deployment, you need to download sunoapi.db from the project and transfer it to your docker-compose.yml file directory. Otherwise, Docker startup will prompt that the file cannot be mounted.


#### Streamlit remote repositories deployment

- First, Fork a copy of SunoApi code to your Github repository
- Select Github authorization login: https://share.streamlit.io/
- Open the deployment page: https://share.streamlit.io/deploy
- Repository selection: SunoApi/SunoApi
- Branch input: main
- Main file path input: main.py
- Click Deploy!

#### Zeabur one-click deployment

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/ORTEGG)


#### Configuration

- First, retrieve your session and cookie from the browser page when logged in.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session.png" style="max-width: 100%;"/></a>

- After filling in the setting information, it will automatically keep alive. You can fill in multiple account information.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session1.png" style="max-width: 100%;"/></a>

- Enter and save the information. You can modify the account information if you enter identity.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session2.png" style="max-width: 100%;"/></a>

### Done

- Once the project is up and running, visit http://localhost:8501/ in your browser.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index1.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index2.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index3.png" style="max-width: 100%;"/></a>


### Questions

- If the page prompt the message: Please save the information first, and then refresh the page to use it normally! Please first add your own account information and save it, then delete other invalid account information in the sunoapi.db database, including the account information I tested, and then you can use it normally.
- If the page prompt the message: Suno AI music song generation submission failed: Unauthorized. This indicates that the account login status is not authorized. This situation is usually caused by multiple browser clients logging in to the account and forming a preemption. Exit other logged in browser clients, keep the account logged in on this SunoAPI AI music song generator client, and do not log in on other browser clients.
- If the page prompt the message: "Suno AI Music song generation failed to submit: Insufficient credits." Indicates that the credits of account information are insufficient, please add your account information to save, and then you can use it normally.
- If the page prompt an error: ModuleNotFoundError: No module named 'streamlit_image select', this is because a streamlit_image select component has been developed for the second time. After the second development, this component is placed in the pages directory where the program runs. When loading the streamlit_image select component for the first time in the program running directory, it is loaded from the site packages directory of Python 3. However, the newly developed component cannot directly use pip3 to install the program saved in the streamlit_image select location. Otherwise, the functionality of the second development cannot be used. The solution is to click After connecting to other pages in the menu on the left, it can be loaded and used normally.
- After the music generation task is successfully submitted, the queue status of the generation task is pulled. When the status is "complete", it returns successfully. At this time, it defaults to waiting for the official generation file for 15 seconds. The official interface service directly returns the URL address of media files, and most of the time the page can display these media files normally. Occasionally, the interface may have returned the Url address of the media file, but the actual file cannot be accessed from the Url address and needs to wait for a while. At this point, the media file may not be able to be loaded on the page. You can right-click on the media player and copy the media file address. Open the address separately in the browser to access it, or right-click to save as download and save. Or go to the music sharing square page list to view the generated records.
- Regarding the security issue of saving account session and cookie information, as long as your account is not recharged, there is no need to worry because you do not know your account password. The session and cookie information you fill in will become invalid if your account logs in to other activities or logs out of the official website, and the session and cookie information you fill in will change the next time you log in to the official website.


### Creation

- Professional lyric assistance tools: https://poe.com/SuperSunoMaster


### Contact

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/wechat.jpg?20240824" style="max-width: 100%;"/></a>


### Participate

- My personal strength is always limited, any form of contribution is welcome, including but not limited to contributing code, optimizing documents, submitting issues and PR. Due to limited time, we do not accept to submit bugs to developers in wechat or wechat group, please submit issues and PR if you have problems or optimization suggestions!

<a href="https://star-history.com/#SunoApi/SunoApi" target="_blank"><img src="https://api.star-history.com/svg?repos=SunoApi/SunoApi" style="max-width: 100%;"/></a>


### Reference

- Suno AI official website: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### Statement

- SunoAPI is an unofficial open source project for study and research only. Users voluntarily enter free account information to generate music. Each account generates five songs per day for free, and we don't use them for other purposes. Please feel free to use! If there are 10,000 users, the system can generate 50,000 songs per day for free. Please try to save your usage as you can only generate five songs per account per day for free. If everyone writes more than five songs a day, it's still not enough. The ultimate goal is to make it free to build whenever you need it.


### Buy Me a Coffee

<a href="https://www.buymeacoffee.com/SunoApi" target="_blank"><img src="https://sunoapi.net/images/donate.jpg" alt="Buy me a Coffee" style="max-width: 100%;"></a>


##### This project originated from GitHub, based on MIT protocol and free, without any form of payment behavior! If you think this project is helpful to you, please help me click "Star" and spread, thank you!