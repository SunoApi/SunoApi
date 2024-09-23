<div align="center">

[繁體中文](https://github.com/SunoApi/SunoApi/blob/main/README_TC.md) | [Русский](https://github.com/SunoApi/SunoApi/blob/main/README_RU.md) | [English](https://github.com/SunoApi/SunoApi/blob/main/README.md) | [한국어](https://github.com/SunoApi/SunoApi/blob/main/README_KR.md) | [日本語](https://github.com/SunoApi/SunoApi/blob/main/README_JP.md) | [Français](https://github.com/SunoApi/SunoApi/blob/main/README_FR.md) | [Deutsch](https://github.com/SunoApi/SunoApi/blob/main/README_DE.md)

[![GitHub release](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=black)](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=blue)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# SunoAPI 非官方 Suno AI 客户端

# 祝贺本开源项目入选本周weekly
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>


### 介绍

- 这是一个基于Python、Streamlit的非官方Suno API客户端，目前支持生成音乐，获取音乐信息等功能。自带维护token与保活功能，无需担心token过期问题，可以设置多个账号的信息保存以便使用。

- GitHub有时候访问不到，如无法访问请移步Gitee地址：https://gitee.com/SunoApi/SunoApi

### 特点

- 填写账号信息程序自动维护与保活
- 可以设置多个账号的信息保存使用
- 音乐分享广场展示所有公开的歌曲
- 输入音乐编号可直接获取歌曲信息
- 支持上传图片解析的内容生成歌曲
- 支持中文英文韩语日语等多国语言

### 调试

#### Python本地调试运行

- 克隆源码

```bash
git clone https://github.com/SunoApi/SunoApi.git
```

- 安装依赖

```bash
cd SunoApi
pip3 install -r requirements.txt
```


- .env 环境变量文件，图片识别需要用到gpt-4o的模型可以使用OpenAI的接口，也可以用其他的你自己常用的接口替换。注册console.bitiful.com对象存储账号获取S3_ACCESSKEY_ID，S3_SECRETKEY_ID参数用于图片上传到你创建的存储桶，S3_WEB_SITE_URL填写你的对象存储账号创建存储桶后的外部访问域名。这样本地环境就可以测试图片识别了。

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


- 启动项目，关于Streamlit请自行参考Streamlit文档

```bash
streamlit run main.py --server.maxUploadSize=3
```


### 部署

#### Docker 本地一键部署

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

##### 注意：需要把 https://sunoapi.s3.bitiful.net 替换成你自己的对象存储桶的外部访问域名，最终上传的图片文件能通过 http://xxxxxx.s3.bitiful.net/images/upload/xxxxxx.jpg 的形式能访问到，不然OpenAI访问不到这个你上传的图片就无法识别图片内容，那么上传图片生成音乐的功能将无法使用。


#### Docker 本地编译部署

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

#### Docker 拉取镜像部署

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

##### 注意：拉取镜像部署需要把项目里面的sunoapi.db下载传到你的docker-compose.yml文件目录，不然docker启动会提示挂载不到文件。


#### Streamlit 远程仓库部署

- 先Fork一份SunoApi代码到你的Github仓库里面
- 选择Github授权登录：https://share.streamlit.io/
- 打开部署页面：https://share.streamlit.io/deploy
- Repository 选择：SunoApi/SunoApi
- Branch 输入：main
- Main file path 输入：main.py
- 点击Deploy！

#### Zeabur 一键部署

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/ORTEGG)


### 配置

- 先从浏览器页面登录状态下中获取自己的session和cookie。

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session.png" style="max-width: 100%;"/></a>

- 填写设置信息里面后面会自动保活，可以填写多个账号信息。

- <a href="https://sunoapi.net" target="_blank"><a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session1.png" style="max-width: 100%;"/></a>

- 填写后保存信息，输入identity可以更改修改账号信息。

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session2.png" style="max-width: 100%;"/></a>

### 完成

- 启动运行项目后浏览器访问 http://localhost:8501/ 即可使用了。

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index1.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index2.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index3.png" style="max-width: 100%;"/></a>


### 问题

- 如果页面提示信息：请先设置信息保存，然后再刷新页面才能正常使用！请先添加自己的账号信息保存，然后把sunoapi.db数据库里面其他无效的账号信息删除，其中包括我测试的账号信息，然后再就可以正常使用了。
- 如果页面提示信息：Suno AI 音乐歌曲生成提交失败：Unauthorized.表示账号登录状态未授权，这种情况一般是多个浏览器客户端登录了账号形成了抢占，退出其他登录的浏览器客户端，保持账号在这个Suno API AI 音乐歌曲生成器客户端登录，不要在其他浏览器客户端登录就可以了。
- 如果页面提示信息：Suno AI 音乐歌曲生成提交失败：Insufficient credits.表示账号信息credits点数不足，请先添加自己的账号信息保存，然后再就可以正常使用了。
- 如果页面提示出错：ModuleNotFoundError: No module named 'streamlit_image_select' 这是因为二次开发了一个streamlit_image_select组件的功能，二次开发后这个组件放在程序运行的pages目录里面，在程序运行目录第一次加载streamlit_image_select组件是到Python3的site-packages目录加载的，但是二次开发了的组件不能直接用pip3 install streamlit_image_select位置保存的程序，不然二次开发的功能无法使用，解决办法就是点下左边菜单其他页面链接后就可以正常加载使用了。
- 音乐生成任务提交成功后拉取生成任务队列状态，当状态为"complete"时成功返回，这个时候默认停留了15秒等待官方生成文件。官方接口服务直接返回了媒体文件Url地址，大部分时候页面能正常显示这些媒体文件。偶尔有时候接口已经返回了媒体文件Url地址，但是实际文件还不能从Url地址访问到要等一会。这个时候媒体文件在页面就可能无法加载到，可以点下媒体播放器鼠标右键复制媒体文件地址，用浏览器单独打开这个地址就可以访问到了或者直接右键另存为下载保存。或者到音乐分享广场页面列表里面去查看生成的记录。
- 关于设置账号session和cookie信息保存安全性问题，只要你的账号不充值就没必要担心，因为不知道你的账号密码，你填写的session和cookie信息只要你的账号在其他地方登录活动，或者在官方网站退出登录，那么填写的session和cookie就无效了，并且下次登录官网session和cookie都会发生变化的。


### 创作

- 专业歌词辅助工具：https://poe.com/SuperSunoMaster


### 交流

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/wechat.jpg?20240923" style="max-width: 100%;"/></a>


### 参与

- 个人的力量始终有限，任何形式的贡献都是欢迎的，包括但不限于贡献代码，优化文档，提交Issue和PR，由于时间有限不接受在微信或者微信群给开发者提Bug，有问题或者优化建议请提交Issue和PR！

<a href="https://star-history.com/#SunoApi/SunoApi" target="_blank"><img src="https://api.star-history.com/svg?repos=SunoApi/SunoApi" style="max-width: 100%;"/></a>


### 参考

- Suno AI 官网: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### 声明

- SunoAPI是一个非官方的开源项目，仅供学习和研究使用。用户自愿输入免费的账号信息生成音乐。每个帐户每天可以免费生成五首歌曲，我们不会将它们用于其他目的。请放心使用！如果有10000名用户，那么系统每天可以免费生成50000首歌曲。请尽量节省使用量，因为每个帐户每天只能免费生成五首歌曲。如果每个人每天创作五首以上的歌曲，这仍然不够。最终目标是让在需要的时候能随时免费生成。


### Buy me a Coffee

<a href="https://www.buymeacoffee.com/SunoApi" target="_blank"><img src="https://sunoapi.net/images/donate.jpg" alt="Buy me a Coffee" style="max-width: 100%;"></a>


##### 此项目开源于GitHub ，基于MIT协议且免费，没有任何形式的付费行为！如果你觉得此项目对你有帮助，请帮我点个Star并转发扩散，在此感谢你！