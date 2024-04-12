[简体中文](README_ZH.md) | [English](README.md) | [한국어](README_KR.md)

# Suno API 非官方 Suno AI 用戶端

這是一個基於Python、Streamlit的非官方Suno API用戶端，現時支持生成音樂，獲取音樂資訊等功能。
自帶維護token與保活功能，無需擔心token過期問題，可以設定多個帳號的資訊保存以便使用。

### 特點

- token自動維護與保活
- 可以設定多個帳號的資訊保存使用
- 程式碼簡單，易於維護，方便二次開發

### 使用

#### 運行

安裝依賴

```bash
pip3 install -r requirements.txt
```

啟動項目，關於Streamlit請自行參攷Streamlit檔案

```bash
streamlit run main.py
```

#### Docker

```bash
docker compose build && docker compose up
```


#### 配寘

先從瀏覽器頁面登入狀態下中獲取自己的session和cookie。

![session](./images/session.png)

填寫設定資訊裡面後面會自動保活，可以填寫多個帳號資訊。

![session1](./images/session1.png)

填寫後保存資訊，更改輸入identity可以即可修改帳號資訊。

![session2](./images/session2.png)

#### 完成

啟動運行項目後瀏覽器訪問 http://localhost:8501/ 即可使用了。

![docs](./images/index.png)


#### 問題

如果頁面一直提示：請先設定資訊保存，然後再刷新頁面才能正常使用！ 請先添加自己的帳號資訊保存，然後把sunoapi.db資料庫裡面其他無效的帳號資訊删除，其中包括我測試的帳號資訊，然後再就可以正常使用了。


#### 交流

<img src="./images/wechat.jpg" width="382px" height="511px" />