[简体中文](README_ZH.md) | [繁體中文](README_TC.md) | [English](README.md)

# Suno API 비공식 Suno AI 클라이언트

파이썬, 스트림릿 기반의 이 비공식 Suno API 클라이언트는 현재 음악 생성, 음악 정보 얻기 등의 기능을 지원하고 있다.
자체 유지 관리 token 및 보존 기능을 가지고 있으며, token 만료 문제를 걱정할 필요가 없으며, 여러 계정의 정보를 설정하여 사용할 수 있도록 저장할 수 있다.

### 특징

- token 자동 유지 보수 및 서비스
- 여러 계정의 정보를 설정하여 저장하여 사용할 수 있음
- 간단한 코드, 간편한 유지 관리, 간편한 2차 개발

### 사용

#### 실행

설치 종속

```bash
pip3 install -r requirements.txt
```

프로젝트를 시작하고 Streamlit에 대해서는 Streamlit 설명서를 참조하십시오.

```bash
streamlit run main.py
```

#### Docker

```bash
docker compose build && docker compose up
```


#### 구성

먼저 브라우저 페이지에서 로그인한 상태에서 자신의 세션과 쿠키를 가져옵니다.

![session](./images/session.png)

설정 정보를 기입하면 뒤에 자동으로 유지됩니다. 여러 계정 정보를 기입할 수 있습니다.

![session1](./images/session1.png)

작성 후 정보를 저장하고 변경 아이덴티티를 입력하면 계정 정보를 수정할 수 있다.

![session2](./images/session2.png)

#### 완료

프로젝트 실행 후 브라우저 액세스 시작http://localhost:8501/바로 사용할 수 있습니다.

![docs](./images/index.png)


#### 문제

페이지가 계속 표시되는 경우: 정보를 저장하도록 설정한 다음 페이지를 새로 고쳐야 제대로 사용할 수 있습니다!먼저 자신의 계정 정보를 추가하여 저장한 다음 sunoapi.db 데이터베이스에 있는 다른 잘못된 계정 정보를 삭제하십시오. 여기에는 제가 테스트한 계정 정보가 포함되어 있습니다. 그리고 정상적으로 사용할 수 있습니다.


#### 커뮤니케이션

<img src="./images/wechat.jpg" width="382px" height="511px" />

<img src="./images/wechat1.png" width="382px" height="511px" />