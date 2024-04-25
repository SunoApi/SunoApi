<div align="center">

[繁體中文](https://github.com/SunoApi/SunoApi/blob/main/README_TC.md) | [Русский](https://github.com/SunoApi/SunoApi/blob/main/README_RU.md) | [English](https://github.com/SunoApi/SunoApi/blob/main/README.md) | [한국어](https://github.com/SunoApi/SunoApi/blob/main/README_KR.md) | [日本語](https://github.com/SunoApi/SunoApi/blob/main/README_JP.md) | [Français](https://github.com/SunoApi/SunoApi/blob/main/README_FR.md) | [Deutsch](https://github.com/SunoApi/SunoApi/blob/main/README_DE.md)

[![GitHub release](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=black)](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=blue)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# Suno API 非官方 Suno AI 客户端

# 祝贺本开源项目入选本周weekly
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>

- 谁在本地搭建项目生成歌曲用我测试的token，而且一直生成一首歌曲的主题叫黄总，每次五首歌曲都用完了搞的我都不能调试程序了。你能用自己的token生成歌曲吗？？？每天就五次好麻烦！！！大家如果有多的闲置不用的账号，可以添加进来这样就可以足够测试使用了。


### 介绍

- 这是一个基于Python、Streamlit的非官方Suno API客户端，目前支持生成音乐，获取音乐信息等功能。自带维护token与保活功能，无需担心token过期问题，可以设置多个账号的信息保存以便使用。

- GitHub有时候访问不到，如无法访问请移步Gitee地址：https://gitee.com/SunoApi/SunoApi

### 特点

- 填写账号信息程序自动维护与保活
- 可以设置多个账号的信息保存使用
- 音乐分享广场展示所有公开的歌曲
- 输入音乐编号可直接获取歌曲信息
- 支持中文英文韩语日语等多国语言

### 调试

#### Python本地调试运行

- 克隆源码

```bash
git clone https://github.com/SunoApi/SunoApi.git
```

- 安装依赖

```bash
pip3 install -r requirements.txt
```

- 启动项目，关于Streamlit请自行参考Streamlit文档

```bash
streamlit run main.py
```


### 部署

#### Docker 本地一键部署

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  sunoapi/sunoapi:latest
```


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
CMD [ "nohup", "streamlit", "run", "main.py" ]
```

#### Docker 拉取镜像部署

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

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/5BLAEZ)


### 配置

- 先从浏览器页面登录状态下中获取自己的session和cookie。

- <img src="https://sunoapi.net/images/session.png" width="1012px"/>

- 填写设置信息里面后面会自动保活，可以填写多个账号信息。

- <img src="https://sunoapi.net/images/session1.png" width="1012px"/>

- 填写后保存信息，输入identity可以更改修改账号信息。

- <img src="https://sunoapi.net/images/session2.png" width="1012px"/>

### 完成

- 启动运行项目后浏览器访问 http://localhost:8501/ 即可使用了。

- <img src="https://sunoapi.net/images/index.png" width="1012px"/>

- <img src="https://sunoapi.net/images/index1.png" width="1012px"/>

- <img src="https://sunoapi.net/images/index2.png" width="1012px"/>

- <img src="https://sunoapi.net/images/index3.png" width="1012px"/>


### 问题

- 如果页面提示信息：请先设置信息保存，然后再刷新页面才能正常使用！请先添加自己的账号信息保存，然后把sunoapi.db数据库里面其他无效的账号信息删除，其中包括我测试的账号信息，然后再就可以正常使用了。
- 如果页面提示信息：Suno AI 音乐歌曲生成提交失败：Insufficient credits.表示账号信息credits点数不足，请先添加自己的账号信息保存，然后再就可以正常使用了。
- 音乐生成任务提交成功后拉取生成任务队列状态，当状态为"complete"时成功返回，这个时候默认停留了15秒等待官方生成文件。官方接口服务直接返回了媒体文件Url地址，大部分时候页面能正常显示这些媒体文件。偶尔有时候接口已经返回了媒体文件Url地址，但是实际文件还不能从Url地址访问到要等一会。这个时候媒体文件在页面就可能无法加载到，可以点下媒体播放器鼠标右键复制媒体文件地址，用浏览器单独打开这个地址就可以访问到了或者直接右键另存为下载保存。
- 关于设置账号session和cookie信息保存安全性问题，只要你的账号不充值就没必要担心，因为不知道你的账号密码，你填写的session和cookie信息只要你的账号在其他地方登录活动，或者在官方网站退出登录，那么填写的session和cookie就无效了，并且下次登录官网session和cookie都会发生变化的。


### 创作

- 专业歌词辅助工具：https://poe.com/SuperSunoMaster


### 交流

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<img src="https://sunoapi.net/images/wechat.jpg?20240430" width="450px" height="538px"/>


### 参与

- 个人的力量始终有限，任何形式的贡献都是欢迎的，包括但不限于贡献代码，优化文档，提交Issue和PR，由于时间有限不接受在微信或者微信群给开发者提Bug，有问题或者优化建议请提交Issue和PR！

[![Star History Chart](https://api.star-history.com/svg?repos=SunoApi/SunoApi)](https://star-history.com/#SunoApi/SunoApi)


### 参考

- Suno AI 官网: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### 声明

- SunoApi 是一个非官方的开源项目，仅供学习和研究使用。用户自愿输入免费的账号信息生成音乐。每个帐户每天可以免费生成五首歌曲，我们不会将它们用于其他目的。请放心使用！如果有10000名用户，那么系统每天可以免费生成50000首歌曲。请尽量节省使用量，因为每个帐户每天只能免费生成五首歌曲。如果每个人每天创作五首以上的歌曲，这仍然不够。最终目标是让在需要的时候能随时免费生成。


### Buy me a Coffee

<a href="https://www.buymeacoffee.com/SunoApi" target="_blank"><img src="https://sunoapi.net/images/donate.jpg" alt="Buy me a Coffee" width="398px" height="398px"></a>


##### 此项目开源于GitHub ，基于MIT协议且免费，没有任何形式的付费行为！
##### 如果你觉得此项目对你有帮助，请帮我点个Star并转发扩散，在此感谢你！