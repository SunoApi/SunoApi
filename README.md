[简体中文](README_ZH.md) | [繁體中文](README_TC.md) | [한국어](README_KR.md)

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

![session](./images/session.png)

After filling in the setting information, it will automatically keep alive. You can fill in multiple account information.

![session1](./images/session1.png)

Enter and save the information. You can modify the account information if you enter identity.

![session2](./images/session2.png)

#### Done

Once the project is up and running, visit http://localhost:8501/ in your browser.

![docs](./images/index.png)


#### Questions

If the page keeps prompting: Please save the information first, and then refresh the page to use it normally! Please first add your own account information and save it, then delete other invalid account information in the sunoapi.db database, including the account information I tested, and then you can use it normally.


#### Contact

<img src="./images/wechat.jpg" width="382px" height="511px" />