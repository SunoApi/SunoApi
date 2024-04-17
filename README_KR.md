<div align="center">

[简体中文](README_ZH.md) | [繁體中文](README_TC.md) | [Русский язык](README_RU.md) | [English](README.md) | [日本語](README_JP.md)


[![GitHub release](https://img.shields.io/static/v1?label=release&message=v1.0.0&color=blue)](https://www.github.com/novicezk/midjourney-proxy)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# Suno API 비공식 Suno AI 클라이언트

# 이번 주 Weekly 오픈 소스 프로젝트 선정 축하합니다.
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>



### 소개

- Python, Streamlit 기반의 비공식 Suno API 클라이언트로, 현재 음악 생성, 음악 정보 얻기 등의 기능을 지원하고 있다.자체 유지 관리 token 및 보존 기능을 가지고 있으며, token 만료 문제를 걱정할 필요가 없으며, 여러 계정의 정보를 설정하여 사용할 수 있도록 저장할 수 있다.

- GitHub에 액세스할 수 없는 경우가 있습니다. 액세스할 수 없으면 Gitee 주소로 이동하십시오.https://gitee.com/SunoApi/SunoApi

### 특징

- 계정 정보 작성 프로그램 자동 유지 보수 및 보존
- 여러 계정의 정보를 설정하여 저장하여 사용할 수 있음
- 음악나눔마당 공개곡 모두 전시
- 음악 번호를 입력하면 바로 노래 정보를 얻을 수 있습니다.

### 디 버그

#### Python 로컬 디버그 실행

- 설치 종속

```bash
pip3 install -r requirements.txt
```

- 프로젝트를 시작하고 Streamlit에 대해서는 Streamlit 설명서를 참조하십시오.

```bash
streamlit run main.py
```

### 배치

#### Docker 로컬 원클릭 배포

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  sunoapi/sunoapi:latest
```

#### Docker 로컬 컴파일 배치

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

#### Docker 미러 배포 끌어오기

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


#### Streamlit 원격 웨어하우스 배포

- 먼저 Fork에서 SunoApi 코드를 Github 창고로 보내
- Github 라이센스 로그인 선택:https://share.streamlit.io/
- 배포 페이지를 엽니다.https://share.streamlit.io/deploy
- Repository 선택: SunoApi/SunoApi
- Branch 입력: main
- ain file path 입력:main.py
- 디플로이 클릭!

#### Zeabur 로컬 원클릭 배포

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/5BLAEZ)


### 구성

- 먼저 브라우저 페이지에서 로그인한 상태에서 자신의 세션과 쿠키를 가져옵니다.

![session](https://sunoapi.net/images/session.png)

- 설정 정보를 기입하면 뒤에 자동으로 유지됩니다. 여러 계정 정보를 기입할 수 있습니다.

![session1](https://sunoapi.net/images/session1.png)

- 작성 후 정보를 저장하고 identity 를 입력하면 수정된 계정 정보를 변경할 수 있습니다.

![session2](https://sunoapi.net/images/session2.png)

### 완료

- 프로젝트 실행 후 브라우저 액세스 시작http://localhost:8501/바로 사용할 수 있습니다.

![index](https://sunoapi.net/images/index.png)

![index1](https://sunoapi.net/images/index1.png)

![index2](https://sunoapi.net/images/index2.png)

![index3](https://sunoapi.net/images/index3.png)


### 문제

- 페이지 프롬프트가 표시되는 경우: 정보를 저장하도록 설정한 다음 페이지를 새로 고쳐야 제대로 사용할 수 있습니다!먼저 자신의 계정 정보를 추가하여 저장한 다음 sunoapi.db 데이터베이스에 있는 다른 잘못된 계정 정보를 삭제하십시오. 여기에는 제가 테스트한 계정 정보가 포함되어 있습니다. 그리고 정상적으로 사용할 수 있습니다.
- 페이지 프롬프트가 표시되는 경우: Suno AI 음악 노래 생성 제출 실패: Insufficient credits. 계정 정보 credits 포인트가 부족함을 나타냅니다. 계정 정보를 추가하여 저장한 다음 정상적으로 사용할 수 있습니다.
- 음악 생성 작업을 제출한 후 생성 작업 대기열 상태를 끌어다가 "complete" 상태일 때 성공적으로 되돌려줍니다. 이 때 기본적으로 15초 동안 공식 생성 파일을 기다립니다.공식 인터페이스 서비스는 미디어 파일 Url 주소를 직접 반환하며 대부분의 경우 페이지에 이러한 미디어 파일이 정상적으로 표시됩니다.가끔 인터페이스가 미디어 파일 Url 주소를 반환했지만 실제 파일은 Url 주소에서 잠시 기다려야 할 때까지 액세스할 수 없습니다.이 경우 미디어 파일이 페이지에서 로드되지 않을 수 있습니다. 미디어 플레이어를 클릭하여 마우스 오른쪽 버튼으로 미디어 파일 주소를 복사할 수 있습니다. 브라우저로 이 주소를 단독으로 열면 액세스할 수 있거나 직접 오른쪽 버튼으로 다운로드로 저장할 수 있습니다.
- 계정 설정 세션 및 쿠키 정보 저장 보안 문제에 관하여, 당신의 계정이 충전되지 않는 한 걱정할 필요가 없습니다. 당신의 계정 비밀번호를 모르기 때문에, 당신이 기입한 세션과 쿠키 정보는 당신의 계정이 다른 곳에서 활동에 로그인하거나 공식 사이트에서 로그인을 환불하기만 하면, 기입한 세션과 쿠키는 무효가 됩니다. 또한 다음에 홈페이지에 로그인하면 세션과 쿠키가 모두 변경됩니다.


### 제작

- 전문 가사 보조 도구:https://poe.com/supersunomaster


### 커뮤니케이션

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<img src="https://sunoapi.net/images/wechat.jpg" width="382px" height="511px" />


### 참여

- 개인의 힘은 시종 제한되어 있고, 어떠한 형식의 공헌도 환영하며, 공헌 코드, 최적화 문서, Issue와 PR을 포함하되 이에 국한되지 않으며, 시간이 제한되어 있기 때문에 위챗이나 위챗 그룹에서 개발자에게 Bug를 제기하는 것을 받아들이지 않으며, 문제가 있거나 최적화 건의가 있으면 Issue와 PR을 제출하십시오!

[![Star History Chart](https://api.star-history.com/svg?repos=SunoApi/SunoApi&type=Timeline)](https://star-history.com/#SunoApi/SunoApi&Timeline)


### 참조

- Suno AI 공식 홈페이지: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### 선언

- SunoApi는 학습 및 연구에만 사용되는 비공식 오픈 소스 프로젝트입니다.사용자는 자발적으로 무료 계정 정보를 입력하여 음악을 생성한다.각 계정은 하루에 5 곡의 노래를 무료로 생성할 수 있으며 다른 목적으로 사용하지 않습니다.안심하고 사용하세요!10000명의 사용자가 있으면 매일 50000곡의 노래를 무료로 생성할 수 있다.계정당 하루 5곡만 무료로 생성할 수 있으므로 사용량을 최대한 절약하십시오.만약 한 사람이 매일 다섯 곡 이상의 노래를 창작한다면, 이것은 여전히 부족하다.최종 목표는 필요할 때 언제든지 무료로 생성할 수 있도록 하는 것이다.
